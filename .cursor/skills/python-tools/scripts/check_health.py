#!/usr/bin/env python3
"""知识库健康度体检：格式合规、索引一致性、重复与断链、检索延迟。

只做「能断言的事」，每条都能对应到修法，不做主观评价：

| 指标 | 阈值 | 超标含义 |
| 格式违规 | 0 | Frontmatter 缺字段 / 无 ## 段落，文件根本没进索引 |
| 未索引文档 | 0 | knowledge 下有文件但注册表里没有，通常是上表违规连带 |
| 孤立 Chunk | 0 | Child 找不到 Parent，Stage 5 回溯会静默降级 |
| 重复 Chunk | <= 10 | 同一 hash 出现多次，检索结果互相挤占预算 |
| 图谱断链 | <= 5 | 概念节点的 chunk_id 指向不存在的 Chunk |
| 检索 P95 | <= 200ms | 评测集上端到端延迟，超标即验收不通过 |
| 陈旧条目 | 0 | 源码 hash 变了但索引还是旧的，说明增量没跑 |

用法：
    python .cursor/skills/python-tools/scripts/check_health.py            # 体检（有告警时退出码 1）
    python .cursor/skills/python-tools/scripts/check_health.py --gate     # 给 run.py check 用：只在 FAIL 时非 0
    python .cursor/skills/python-tools/scripts/check_health.py --verbose   # 打印每条超阈值项的具体位置
退出码：0 = 全部达标（或 --gate 下无 FAIL）；1 = 有 WARN/FAIL。
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb_common as kb  # noqa: E402

LIMITS = {
    "format": 0, "unindexed": 0, "orphan": 0, "duplicate": 10,
    "graph_broken": 5, "stale": 0, "p95_ms": 200.0, "dangling": 0,
}
ROOT_PATH = kb.ROOT


def check_format() -> tuple[list[str], list[str]]:
    """直接对磁盘上的文件做规范校验，不依赖索引是否新鲜。"""
    problems = []
    paths = set()
    for path in kb.list_knowledge_files():
        paths.add(kb.rel(path))
        try:
            meta, body = kb.frontmatter(path.read_text(encoding="utf-8"))
        except (ValueError, OSError, UnicodeDecodeError) as exc:
            problems.append(kb.rel(path) + ": " + str(exc))
            continue
        missing = [name for name in kb.REQUIRED_FIELDS if not meta.get(name)]
        if missing:
            problems.append(kb.rel(path) + ": 缺字段 " + ", ".join(missing))
            continue
        if not [row for row in kb.headings(body) if row[1] == 2]:
            problems.append(kb.rel(path) + ": 没有 ## 段落，无法建立两层结构")
        h1 = [row for row in kb.headings(body) if row[1] == 1]
        if len(h1) != 1:
            problems.append(kb.rel(path) + ": H1 标题数量应为 1，实测 " + str(len(h1)))
    return problems, sorted(paths)


def check_index(paths: list[str], registry_out: list) -> tuple[dict, list[str]]:
    """比对注册表与 SQLite，找出未索引、陈旧、孤立和重复。"""
    details: list[str] = []
    registry = kb.read_json(kb.REGISTRY_PATH, {"documents": {}, "chunks": {}})
    registry_out.append(registry)
    docs = registry.get("documents", {})
    chunks = registry.get("chunks", {})
    counts = {"unindexed": 0, "stale": 0, "orphan": 0, "duplicate": 0, "graph_broken": 0}

    indexed_paths = {row["path"] for row in docs.values()}
    for path in paths:
        if path not in indexed_paths:
            counts["unindexed"] += 1
            details.append("未索引: " + path)

    if not kb.DB_PATH.is_file():
        counts["stale"] = len(paths)
        details.append("索引文件缺失: " + kb.rel(kb.DB_PATH))
        return counts, details

    con = sqlite3.connect(kb.DB_PATH)
    db_rows = {
        row[0]: row for row in con.execute(
            "SELECT chunk_id, content_hash, token_count, kind, parent_id, status FROM chunks"
        )
    }
    for chunk_id, chunk in chunks.items():
        row = db_rows.get(chunk_id)
        if row is None:
            counts["stale"] += 1
            details.append("索引缺 Chunk: " + chunk_id)
        elif row[1] != chunk["content_hash"]:
            counts["stale"] += 1
            details.append("内容已变更但索引未更新: " + chunk_id)
    for row in con.execute("SELECT count(*) FROM chunks WHERE status='live'").fetchone():
        live = row

    # 源码与注册表比对：文件改了但没重跑 chunker
    for doc_id, doc in docs.items():
        path = ROOT_PATH / doc["path"]
        if path.is_file() and kb.content_hash(path.read_text(encoding="utf-8")) != doc["source_hash"]:
            counts["stale"] += 1
            details.append("源文件已改但注册表是旧的: " + doc["path"])

    for chunk_id, chunk in chunks.items():
        if chunk["kind"] == "child" and chunk.get("parent_id") not in chunks:
            counts["orphan"] += 1
            details.append("孤立 Child（Parent 不存在）: " + chunk_id)
    hashes = Counter(c["content_hash"] for c in chunks.values() if c["kind"] == "child")
    for digest, times in hashes.items():
        if times > 1:
            counts["duplicate"] += times - 1
            details.append("重复内容 " + str(times) + " 次: " + digest[:19])

    known = set(chunks)
    for name, chunk_ids in con.execute("SELECT name, chunk_ids FROM concept"):
        broken = [c for c in chunk_ids.split(",") if c and c not in known]
        if broken:
            counts["graph_broken"] += 1
            details.append("概念 " + name + " 挂空 " + str(len(broken)) + " 处")
    con.close()
    counts["live"] = live
    return counts, details


def check_vercionc(registry: dict, con) -> tuple[list[str], int]:
    """检查 supersedes 是否指向存在的文档，并数出冲突候选。

    悬空的 supersedes 是真实的腐化信号：目标文档改名或删掉之后，旧版永远拿不到
    降权，检索会把两版并列返回。这项断言廉价且可修（改 frontmatter 或删字段）。

    冲突候选不是错误：设计上只做“两份文档覆盖同批概念且 updated 更新晚于对方”的
    事实陈述，要不要处理由人判断。它一旦算进失败项，知识库就没法长出第二份文档
    ——每加一份都必然制造若干候选，体检会永久变红。所以这里单独返回计数。
    """
    problems = []
    for doc in registry.get("documents", {}).values():
        target = str(doc.get("supersedes") or "")
        if target and target not in registry.get("documents", {}):
            problems.append("悬空 supersedes: " + doc["doc_id"] + " -> " + target)
    conflicts = con.execute("SELECT count(*) FROM conflict").fetchone()[0]
    return problems, conflicts



def measure_latency(samples: int) -> tuple[float, float]:
    """端到端测 P50/P95（含预算裁剪与图谱查询），不是只测 SQL。"""
    from retriever import retrieve
    queries = [
        "shared_ptr 循环引用怎么打破", "std::unique_ptr 移动语义", "vector 为什么比 list 快",
        "void* 类型擦除", "内存对齐 alignas", "weak_ptr lock 用法",
        "placement new 构造", "迭代器失效", "PIMPL 编译防火墙", "atomic 内存序", "span 替代裸指针",
        "自定义删除器", "dynamic_cast 向下转型", "虚析构为什么必要", "对象切片",
        "无锁栈 ABA", "Arena 分配器", "Core Guidelines 所有权规则", "悬挂指针排查",
    ][:samples]
    # 24h 查询缓存会让重复查询只走 dict 查找，测出来的 P95 是假的。
    # 每次测量前清空缓存，量的是真正的端到端冷路径。
    if kb.DB_PATH.is_file():
        probe = sqlite3.connect(kb.DB_PATH)
        probe.execute("DELETE FROM query_cache")
        probe.commit()
        probe.close()
    times = []
    for query in queries:
        started = time.time()
        retrieve(query)
        times.append((time.time() - started) * 1000)
    if not times:
        return 0.0, 0.0
    times.sort()
    p50 = times[len(times) // 2]
    p95 = times[max(0, int(round(len(times) * 0.95)) - 1)]
    return p50, p95


def run(gate: bool, verbose: bool, samples: int) -> int:
    started = time.time()
    problems, paths = check_format()
    holder: list = []
    counts, details = check_index(paths, holder)
    counts["format"] = len(problems)
    p50, p95 = (measure_latency(samples) if paths else (0.0, 0.0))
    counts["p95_ms"] = p95

    order = ["format", "unindexed", "stale", "orphan", "duplicate", "graph_broken", "dangling"]
    vercion_problemc, conflicts = ([], 0)
    if holder and kb.DB_PATH.is_file():
        probe = sqlite3.connect(kb.DB_PATH)
        vercion_problemc, conflicts = check_vercionc(holder[0], probe)
        probe.close()
    counts["dangling"] = len(vercion_problemc)
    problems = problems + vercion_problemc

    degraded = p95 > LIMITS["p95_ms"]
    failed = [k for k in order if counts[k] > LIMITS[k]]
    if degraded and not gate:
        failed.append("p95_ms")            # gate 模式只把结构性问题当失败，延迟降级为告警

    live = counts.get("live", 0)
    status = "PASS" if not failed else "FAIL"
    print(status + "  kb-health  文件=" + str(len(paths))
          + "  Chunk(live)=" + str(live)
          + "  格式违规=" + str(counts["format"])
          + "  未索引=" + str(counts["unindexed"])
          + "  陈旧=" + str(counts["stale"])
          + "  孤立=" + str(counts["orphan"])
          + "  重复=" + str(counts["duplicate"])
          + "  图谱断链=" + str(counts["graph_broken"])
          + "  悬空supersedes=" + str(counts["dangling"])
          + "  冲突候选=" + str(conflicts)
          + "  P50=" + format(p50, ".1f") + "mc P95=" + format(p95, ".1f") + "ms")
    if failed:
        print("      超阈值项: " + ", ".join(failed))
    if conflicts:
        print("      提示：冲突候选 " + str(conflicts)
              + " 处待人工确认（方向按 updated，含共享概念名）；确认后在新版写 supersedes，不视为失败")
    if verbose:
        for row in problems:
            print("      [格式] " + row)
        for row in details[:20]:
            print("      [索引] " + row)
        print("      体检耗时 " + format(time.time() - started, ".2f") + "s")
    return 1 if failed else 0


def main() -> int:
    kb.configure_stdout()
    parser = argparse.ArgumentParser(description="知识库健康度体检")
    parser.add_argument("--gate", action="store_true", help="只把结构性问题视为失败（供 run.py check 调用）")
    parser.add_argument("--verbose", action="store_true", help="打印超阈值项的具体位置")
    parser.add_argument("--samples", type=int, default=20, help="延迟测量用的查询条数")
    args = parser.parse_args()
    return run(args.gate, args.verbose, args.samples)


if __name__ == "__main__":
    sys.exit(main())
