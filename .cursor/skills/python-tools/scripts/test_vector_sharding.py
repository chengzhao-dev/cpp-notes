"""§3.2 分片回归：锁住「按 domain 切库不得改变结果」和「淘汰后重建必须一致」。

为什么需要这份断言：热/温/冷驻留和分片都是「函数上看得出去没问题、
实际上靠写死缓存 key 和淘汰顺序」的代码。只要 key 少了一段、或某个
分片把另一个块的 rowid 乘了进去，打分就会静默错误。这里用同一份合成库
把两种口径逐名比对，并且主动把分片池打爆一次，确认 cold 分片重建后结果不变。

用法：python .cursor/skills/python-tools/scripts/test_vector_sharding.py
退出码：0 = 断言全过；非 0 = 分片语义又被改坏了。
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_common as kb  # noqa: E402
import indexer  # noqa: E402
import retriever  # noqa: E402

TEXTS = [
    "shared_ptr 的控制块把强引用计数和弱引用计数放在同一次分配里",
    "unique_ptr 只移动所有权，析构顺序是声明的逆序",
    "vector 扩容会让迭代器失效，这是缓存友好的代价",
    "内存对齐 alignas 改变的是布局而不是语义",
    "data race 与竞态条件不同，前者要求两个访问之间没有 happens-before",
    "字节是最小可寻址单位，一个字节等于八个位",
]

DOMAINS = ["cpp_core", "std_lib", "concurrency"]
QUERIES = [
    "shared_ptr 循环引用怎么打破",
    "一个字节等于多少位",
    "vector 为什么比 list 快",
    "不存在的符号 xyzzy",
]
LIMIT = 200


def build() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    indexer.connect(con)
    index = 0
    for domain in DOMAINS:
        doc = {"doc_id": "d-" + domain, "domain": domain, "subdomain": "t",
               "updated": "2026-09-08", "tags": ["pointer"], "levels": [0, 9]}
        for text in TEXTS:
            for repeat in range(2):
                content = text + " 变体 " + str(index)
                cid = "%s__c%04d" % (domain, index)
                chunk = {"chunk_id": cid, "parent_id": None, "doc_id": doc["doc_id"],
                         "kind": "child", "heading_path": cid, "content": content,
                         "content_hash": kb.content_hash(content),
                         "token_count": kb.estimate_tokens(content)}
                indexer.upsert(con, chunk, doc, {})
                index += 1
    con.execute("INSERT INTO meta VALUES ('build_seq', '1') "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value")
    con.commit()
    return con


def doc_domain(con, chunk_id: str) -> str:
    return con.execute("SELECT domain FROM chunks WHERE chunk_id=?",
                       (chunk_id,)).fetchone()[0]


retriever.VECTOR_SHARDS.clear()
con = build()
total = con.execute("SELECT count(*) FROM chunks").fetchone()[0]
assert total == len(DOMAINS) * len(TEXTS) * 2, "synthetic library size drifted"

# 1) 分片不得改变结果：带 domain 的分片 vs 全库分片再按 domain 过滤
checked = 0
for domain in DOMAINS:
    allow = {r for (r,) in con.execute("SELECT chunk_id FROM chunks WHERE domain=?",
                                      (domain,))}
    for query in QUERIES:
        expected = [c for c in retriever.vector_search(con, query, None, LIMIT)
                    if c in allow]
        got = retriever.vector_search(con, query, allow, LIMIT, domain)
        assert got == expected, ("domain 分片改变了名次 域=" + domain
                                 + " 查询=" + query
                                 + " 期望 " + str(expected[:3])
                                 + " 实得 " + str(got[:3]))
        assert all(doc_domain(con, c) == domain for c in got), "分片串域"
        checked += 1
    # 分片只读自己的块：该域内的块数必须等于分片里的 ids
    shard = retriever.vector_shard(con, domain)
    assert shard["chunks"] == len(allow), (
        domain + " 分片含 " + str(shard["chunks"]) + " 块，应为 "
        + str(len(allow)) + "（分片条件漏了或多了）")

# 2) 跨域查询不得被分片抢公：全库分片与逐块 cosine 同序
whole = retriever.vector_search(con, QUERIES[0], None, LIMIT)
probe = indexer.embed(QUERIES[0])
brute = {cid: indexer.cosine(probe, blob) for cid, blob in con.execute(
    "SELECT chunk_id, vector FROM chunks "
    "WHERE kind='child' AND status='live' AND vector IS NOT NULL")}
expected = [cid for cid, score in
            sorted(brute.items(), key=lambda row: (row[1], row[0]), reverse=True)
            if score > 0.0]
head = [cid for cid in whole if brute.get(cid, 0.0) > 0.0]
assert head == expected, ("全库分片与逐块 cosine 不同序 "
                          + str(head[:3]) + " vs " + str(expected[:3]))
assert all(brute.get(cid, 0.0) <= 0.0 for cid in whole[len(head):]), (
    "非正分块挤进了正分块前面")

# 3) 热/温/冷：驻留数不得超上限，淘汰后重建必须同结果
# 上限是生产取值（RESIDENT_SHARD_LIMIT=6），这里把它调小才能看见淘汰；
# 取值本身不是被验证的对象，被验证的是 LRU 语义与 cold 重建的一致性。
limit = retriever.RESIDENT_SHARD_LIMIT
retriever.RESIDENT_SHARD_LIMIT = 2
try:
    before = retriever.VECTOR_SHARD_BUILDS
    for _round in range(3):
        for domain in DOMAINS:
            retriever.vector_shard(con, domain)
        retriever.vector_shard(con, "")
    assert len(retriever.VECTOR_SHARDS) <= retriever.RESIDENT_SHARD_LIMIT, (
        "驻留分片数超过上限：" + str(len(retriever.VECTOR_SHARDS)))
    assert retriever.VECTOR_SHARD_BUILDS > before, "分片被淘汰后没重建"
    # 队尾 = 最近用过（hot），队首 = 最久未用（下一个被淘汰）
    assert list(retriever.VECTOR_SHARDS)[-1] == (id(con), "1", ""), (
        "刚用过的全库分片不在队尾")
    assert all(key[1] == "1" for key in retriever.VECTOR_SHARDS), "注入了别的序号"
finally:
    retriever.RESIDENT_SHARD_LIMIT = limit

warm = retriever.vector_search(con, QUERIES[1], None, LIMIT, "cpp_core")
retriever.VECTOR_SHARDS.clear()              # 模拟全部变 cold
assert retriever.vector_search(con, QUERIES[1], None, LIMIT, "cpp_core") == warm, (
    "cold 分片重建后结果不一致")

# 4) 重建索引后旧序号的分片全部作废，不得残留在驻留池里
con.execute("UPDATE chunks SET status='deprecated' WHERE domain='cpp_core'")
con.commit()
con.execute("INSERT INTO meta VALUES ('build_seq', '2') "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value")
con.commit()
assert retriever.vector_search(con, QUERIES[0], None, LIMIT, "cpp_core") == [], (
    "升了 build_seq 仍读到 cpp_core 的旧分片")
assert not [k for k in retriever.VECTOR_SHARDS if k[1] == "1"], (
    "旧序号的分片没被清掉，会慢性占用内存")

print("PASS  向量分片  " + str(checked) + " 条域内查询与全库口径逐名一致"
      + "，驻留上限=" + str(retriever.RESIDENT_SHARD_LIMIT)
      + " 且 cold 重建同结果")
