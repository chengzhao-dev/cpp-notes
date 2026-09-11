"""向量路等价性回归：锁住「维度倒排 == 逐块 cosine」这条不能靠感觉相信的等式。

为什么需要这份断言：Layer 2 从全表扫改成倒排后，声明的是精确检索而不是 ANN
近似。这句话只有两种证明方式——逐块比对分数与名次，或者承认自己是近似。
这里做前者：同一份合成索引，暴力扫与倒排各自打分后逐个比对。

口径差异（刻意写明，不是漏洞）：暴力扫给每一块都打分，因此 0 分块也占名额；
倒排只给有非零维重叠的块打分，天然不产出 0 分。所以断言分成三段：
正分部分逐名次完全一致、倒排不得漏掉任何正分块、倒排多出的块分数必须非正。

用法：python .agents/skills/python-tools/scripts/test_vector_index_equivalence.py
退出码：0 = 断言全过；非 0 = 等价性又断了（AssertionError 直接给现场）。
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_common as kb  # noqa: E402
import indexer  # noqa: E402
import retriever  # noqa: E402

DOC = {"doc_id": "d1", "domain": "cpp_core", "subdomain": "t", "updated": "2026-09-08",
       "tags": ["pointer"], "levels": [0, 9]}

TEXTS = [
    "shared_ptr 的控制块把强引用计数和弱引用计数放在同一次分配里",
    "unique_ptr 只移动所有权，析构顺序是声明的逆序",
    "vector 扩容会让迭代器失效，这是缓存友好的代价",
    "list 的节点分散在堆上，遍历时缓存命中率下降",
    "内存对齐 alignas 改变的是布局而不是语义",
    "data race 与竞态条件不同，前者要求两个访问之间没有 happens-before",
    "memory_order_relaxed 只保证原子性，不保证顺序",
    "无锁栈的 ABA 问题来自 CAS 只看值不看版本",
    "字节是最小可寻址单位，一个字节等于八个位",
    "指针相减的类型是 ptrdiff_t，越界访问是未定义行为",
    "空指针解引用会被 AddressSanitizer 抓到",
    "智能指针的循环引用要靠 weak_ptr 打破",
]

QUERIES = [
    "shared_ptr 循环引用怎么打破",
    "无锁栈的 ABA 问题",
    "一个字节等于多少位",
    "vector 为什么比 list 缓存友好",
    "memory_order_relaxed 的含义",
    "指针越界",
    "完全不存在的符号 xyzzy 查询",
    "unique_ptr 声明顺序",
]

LIMIT = 200


def build_connection(rows: int) -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    indexer.connect(con)
    for index in range(rows):
        content = TEXTS[index % len(TEXTS)] + " 变体 " + str(index)
        cid = "c%04d" % index
        chunk = {"chunk_id": cid, "parent_id": None, "doc_id": DOC["doc_id"],
                 "kind": "child", "heading_path": cid, "content": content,
                 "content_hash": kb.content_hash(content),
                 "token_count": kb.estimate_tokens(content)}
        indexer.upsert(con, chunk, DOC, {})
    con.execute("INSERT INTO meta VALUES ('build_seq', '1') "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value")
    con.commit()
    return con


def brute_scores(con, query):
    """原实现口径：逐块 cosine，0 分块也在结果里。"""
    probe = indexer.embed(query)
    return {cid: indexer.cosine(probe, blob) for cid, blob in con.execute(
        "SELECT chunk_id, vector FROM chunks "
        "WHERE kind='child' AND status='live' AND vector IS NOT NULL")}


con = build_connection(6 * len(TEXTS))
checked = 0

for query in QUERIES:
    scores = brute_scores(con, query)
    expected = sorted(scores.items(), key=lambda row: (row[1], row[0]), reverse=True)
    positive = [cid for cid, score in expected if score > 0.0]
    got = retriever.vector_search(con, query, None, LIMIT)
    got_set = set(got)

    missing = [cid for cid in positive if cid not in got_set]
    assert not missing, "倒排漏掉正分块 " + str(missing[:3]) + " 查询=" + query

    head = [cid for cid in got if scores.get(cid, 0.0) > 0.0]
    assert head == positive, ("正分名次不一致 查询=" + query
                              + " 期望 " + str(positive[:3]) + " 实得 " + str(head[:3]))
    assert all(scores.get(cid) is not None for cid in got), "倒排召回了索引外的块"
    assert len(got) >= len(positive)
    checked += 1

# 预过滤：allow 之外的块一律不得放行，空集合不得放行任何块
allow_ids = {r for (r,) in con.execute("SELECT chunk_id FROM chunks LIMIT 7")}
narrowed = retriever.vector_search(con, QUERIES[0], allow_ids, LIMIT)
assert narrowed and set(narrowed) <= allow_ids, "allow 预过滤被绕过"
assert retriever.vector_search(con, QUERIES[0], set(), LIMIT) == []

# 缓存随 build_seq 失效：升序号后才允许看到 status 变化
gone = "c0000"
con.execute("UPDATE chunks SET status='deprecated' WHERE chunk_id=?", (gone,))
con.commit()
assert gone in set(retriever.vector_search(con, QUERIES[0], None, LIMIT)), (
    "序号未变时应当仍读旧分片，否则这条断言锁不住失效时机")
con.execute("INSERT INTO meta VALUES ('build_seq', '2') "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value")
con.commit()
assert gone not in set(retriever.vector_search(con, QUERIES[0], None, LIMIT)), (
    "升了 build_seq 仍召回 deprecated 块")
assert len(retriever.VECTOR_SHARDS) == 1, "分片缓存没有随构建序号收敛"

print("PASS  向量索引等价性  " + str(checked) + " 条查询的正分名次与逐块 cosine 完全一致，"
      "倒排只省略 0 分填充")
