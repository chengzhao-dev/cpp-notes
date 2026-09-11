#!/usr/bin/env python3
"""规模基准：证明或推翻「三层索引能撑到 100MB–1GB」这条硬要求（goal 3.2）。

为什么需要它：3.1 的延迟指标只能在真实体量上验证。当前库只有千级 Chunk，
kb-check 的 P95 好看不代表十万级仍然好看，因为向量路的打分次数仍随块数增长。
本脚本用真实知识文件派生合成 Chunk，按 1k/10k/50k/100k 逐级测量召回侧耗时，
给出可复现的曲线和「当前实现开始破线的拐点」，不改生产索引。

口径：测的是稳态检索。向量路的「维度 到 块」倒排分片在首次调用时才构建，
那是秒级的一次性成本，所以计时前先做一轮不计时预热，建分片开销另计打印。

合成语料按 domain 均匀铺开（每域固定约 DOMAIN_CHUNKS 块，域数随体量增长），
这样才能分开回答两件事：不限域的全库向量路是否仍随 N 线性，以及限定
单域（命中分片）后候选规模是否脱钩。门禁只卡全库路径，不拿域内数字替代它。

用法：
    python .agents/skills/python-tools/scripts/benchmark_scale.py                # 默认 1k/10k/50k/100k
    python .agents/skills/python-tools/scripts/benchmark_scale.py --sizes 1000,10000 --repeats 5
退出码：0 = 全部级别 P95 < 200ms；1 = 有级别超标（即需要换 ANN 的证据）。
拐点口径：报告第一个破线的 Chunk 数，作为「当前实现能撑到多大」的可复现证据。
"""

from __future__ import annotations

import argparse
import random
import shutil
import re
import sqlite3
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_common as kb  # noqa: E402
import indexer  # noqa: E402
import retriever  # noqa: E402
from temp_paths import temp_dir  # noqa: E402

P95_LIMIT_MS = 200.0
DOMAIN_CHUNKS = 1024      # 合成库里每个 domain 固定多少块（§3.2 域内口径）
DOCS_PER_DOMAIN = max(1, DOMAIN_CHUNKS // 12)   # seed_chunks 是每 12 块开一个 doc
NL = chr(10)


def real_paragraphs() -> list[str]:
    """从真实知识文件取段落，作为合成 Chunk 的内容来源（保持词分布接近真实）。"""
    paras: list[str] = []
    for path in kb.list_knowledge_files():
        text = path.read_text(encoding="utf-8")
        body = text.split("---" + NL, 2)[-1]
        for block in re.split(NL + NL + "+", body):
            block = block.strip()
            if len(block) >= 120:
                paras.append(block)
    if len(paras) < 40:
        raise SystemExit("FAIL  scale  真实段落不足，先确认 knowledge/ 已入库")
    return paras


def seed_chunks(target: int, paras: list[str]) -> tuple[dict, dict]:
    """造 target 个 Child Chunk（含 Parent），内容在真实段落里轮转并注入编号保证唯一。"""
    documents: dict[str, dict] = {}
    chunks: dict[str, dict] = {}
    index = 0
    shard = 0
    while index < target:
        doc_id = "synth-doc-%05d" % (index // 12 + 1)
        if doc_id not in documents:
            documents[doc_id] = {
                "doc_id": doc_id, "path": "synthetic/%s.md" % doc_id,
                "domain": "dom%04d" % (index // 12 // DOCS_PER_DOMAIN),
                "subdomain": "scale", "updated": "2026-09-08",
                "tags": ["pointer", "memory"], "levels": [0, 9], "source_hash": "",
            }
        parent_id = doc_id + "__P__sec"
        chunks.setdefault(parent_id, {
            "chunk_id": parent_id, "parent_id": None, "doc_id": doc_id, "kind": "parent",
            "heading_path": "合成章节", "content": documents[doc_id]["doc_id"],
            "content_hash": kb.content_hash(parent_id), "token_count": kb.estimate_tokens(parent_id),
            "order": index,
        })
        content = paras[index % len(paras)] + " SYN" + str(index)
        chunk_id = parent_id + "__C__%06d" % index
        chunks[chunk_id] = {
            "chunk_id": chunk_id, "parent_id": parent_id, "doc_id": doc_id, "kind": "child",
            "heading_path": "合成章节 > 合成小节 " + str(index), "content": content,
            "content_hash": kb.content_hash(content),
            "token_count": kb.estimate_tokens(content), "order": index,
        }
        index += 1
        shard += 1
    return documents, chunks


def build(con: sqlite3.Connection, documents: dict, chunks: dict) -> float:
    started = time.time()
    previous: dict[str, dict] = {}
    for chunk_id, chunk in chunks.items():
        indexer.upsert(con, chunk, documents[chunk["doc_id"]], previous)
    con.commit()
    return time.time() - started


def biggest_domain(con: sqlite3.Connection) -> str:
    """取合成库里最大的 domain，作为域内口径的被测分片。"""
    row = con.execute("SELECT domain, count(*) FROM chunks WHERE status='live' "
                      "GROUP BY domain ORDER BY count(*) DESC LIMIT 1").fetchone()
    return row[0] if row and row[0] else ""


def measure(con: sqlite3.Connection, queries: list[str], repeats: int) -> dict:
    # 预热：让向量分片在计时外构建完，否则首次调用的建分片秒级开销会混进 P95。
    domain = biggest_domain(con)
    started = time.time()
    for query in queries:
        retriever.bm25_search(con, query, None, 20)
        retriever.vector_search(con, query, None, 20)
        retriever.vector_search(con, query, None, 20, domain)
    warmup_s = time.time() - started
    bm25_ms, vector_ms, both_ms, sharded_ms = [], [], [], []
    for _ in range(repeats):
        for query in queries:
            started = time.time()
            retriever.bm25_search(con, query, None, 20)
            one_b = (time.time() - started) * 1000.0
            started = time.time()
            retriever.vector_search(con, query, None, 20)
            one_v = (time.time() - started) * 1000.0
            started = time.time()
            retriever.vector_search(con, query, None, 20, domain)
            sharded_ms.append((time.time() - started) * 1000.0)
            bm25_ms.append(one_b)
            vector_ms.append(one_v)
            both_ms.append(one_b + one_v)
    def p95(rows: list[float]) -> float:
        rows = sorted(rows)
        return rows[min(len(rows) - 1, int(len(rows) * 0.95))]
    return {
        "warmup_s": warmup_s,
        "bm25_p95": p95(bm25_ms),
        "vector_p95": p95(vector_ms),
        "both_p95": p95(both_ms),
        "vector_avg": statistics.fmean(vector_ms),
        "domain": domain,
        "sharded_p95": p95(sharded_ms),
        "sharded_avg": statistics.fmean(sharded_ms),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="知识库规模基准")
    parser.add_argument("--sizes", default="1000,10000,50000,100000", help="逗号分隔的 Chunk 数")
    parser.add_argument("--repeats", type=int, default=3, help="每级重复次数")
    parser.add_argument("--queries", type=int, default=8, help="每级使用的查询数")
    parser.add_argument("--verbose", action="store_true", help="打印每级明细")
    args = parser.parse_args()

    sizes = [int(s) for s in args.sizes.split(",") if s.strip()]
    paras = real_paragraphs()
    rng = random.Random(20260908)
    probes = [
        "shared_ptr 循环引用怎么打破",
        "侵入式数据结构",
        "对象切片",
        "为什么不开行号",
        "unique_ptr 移动语义",
        "内存对齐 alignas",
        "无锁队列 ABA",
        "目录默认收录几级标题",
    ][: max(1, args.queries)]

    print("规模基准  真实段落=" + str(len(paras)) + "  探针查询=" + str(len(probes))
          + "  重复=" + str(args.repeats) + "  上限 P95=" + format(P95_LIMIT_MS, "g") + "ms")
    failures: list[str] = []
    previous_rows: list[tuple[int, dict]] = []
    for target in sizes:
        documents, chunks = seed_chunks(target, paras)
        tmp = temp_dir("benchmarks") / ("kbscale-%d" % target)
        tmp.mkdir(parents=True, exist_ok=True)
        db_path = tmp / ("scale-%d.sqlite" % target)
        con = sqlite3.connect(db_path)
        indexer.connect(con)
        build_s = build(con, documents, chunks)
        stats = measure(con, probes, args.repeats)
        # 预热的实际构成：这一轮里向量分片才建好，单独打印出来供核对口径。
        warm_c = stats["warmup_s"]
        bytes_per_row = db_path.stat().ct_cize // max(1, len(chunks))
        print("  Chunk=" + str(len(chunks)).rjust(7)
              + "  索引=" + format(build_s, "6.2f") + "c"
              + "  BM25 P95=" + format(stats["bm25_p95"], "8.1f") + "mc"
              + "  向量 P95=" + format(stats["vector_p95"], "9.1f") + "mc"
              + "  双路合计 P95=" + format(stats["both_p95"], "9.1f") + "mc"
              + "  库=" + format(db_path.stat().ct_cize / 1048576.0, "7.1f") + "MB"
              + "  每块=" + str(bytes_per_row) + "B"
              + "  预热(含建分片)=" + format(warm_c, "6.2f") + "c"
              + "  域内 P95=" + format(stats["sharded_p95"], "7.1f") + "ms")
        if args.verbose:
            print("        索引字节=" + str(db_path) + "  向量均值="
                  + format(stats["vector_avg"], ".1f") + "ms")
        con.close()
        # WAL 附属文件（-wal / -shm）在 close 前可能仍占句柄，退避后重试一次。
        for _ in range(20):
            shutil.rmtree(tmp, ignore_errors=True)
            if not tmp.exists():
                break
            time.sleep(0.05)
        previous_rows.append((target, stats))
        if stats["both_p95"] >= P95_LIMIT_MS:
            failures.append("Chunk=" + str(len(chunks)) + " 双路 P95 "
                            + format(stats["both_p95"], ".1f") + "ms 超过 "
                            + format(P95_LIMIT_MS, "g") + "ms")
    if previous_rows:
        knee = next((t for t, st in previous_rows if st["both_p95"] >= P95_LIMIT_MS), None)
        last = previous_rows[-1]
        print("      拐点=" + (str(knee) + " Chunk" if knee else "未出现（末级 " + str(last[0]) + " Chunk 仍达标）")
              + "  末级向量均值=" + format(last[1]["vector_avg"], ".1f") + "ms")
    if failures:
        print("FAIL  scale  全库召回侧在下列体量已破 P95")
        for row in failures:
            print("      " + row)
        sharded = next((t for t, st in previous_rows
                        if st["both_p95"] >= P95_LIMIT_MS), None)
        if sharded:
            row = next(ct for t, st in previous_rows if t == sharded)
            print("      同一体量限定单域（命中分片）P95="
                  + format(row["sharded_p95"], ".1f") + "ms 域=" + str(row["domain"])
                  + "；即域内查询不受全库规模影响")
        return 1
    print("PASS  scale  全部级别双路 P95 低于 " + format(P95_LIMIT_MS, "g") + "ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
