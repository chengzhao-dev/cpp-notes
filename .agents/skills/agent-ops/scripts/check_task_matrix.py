#!/usr/bin/env python3
"""任务矩阵一致性体检：把「矩阵声称的」与「磁盘实际的」对齐。

为什么需要它：`references/tasks/<part>.md` 是 scope 的唯一路由表。状态列、前置 id 或
reference 路径一旦与磁盘脱节，agent 就会按失效路由去读不存在的文件，或重复写已合并掉的
章节。这类漂移 markdown 链接检查抓不到——表格里是纯文本路径，`—（不新建）` 之类的占位
更不是链接，所以单独断言。

检查项（任一不满足即 FAIL）：
  1. 骨架：8 个 part 矩阵齐备，表头与 scope.py 的解析契约一致。
  2. ID：前缀与 part 匹配、同 part 内连续编号、全局唯一。
  3. 前置：依赖的 id 必须真实存在（不允许幽灵依赖）。
  4. 读取项：公共必读与本章专项必读指向的文件必须存在于磁盘。
  5. 正文：列内容必须是 `content/<part>/<chapter>.qmd`，done 必须存在且已在 `_quarto.yml`
     注册，todo 与 merged 必须不存在。
  6. 示例：merged 不留路径，done 指向的示例必须存在。
  7. 生成脚本：`generate_tasks.py` 的章节表与磁盘逐字节一致（防再次脱节）。
  8. 可路由：每章都能被 `scope.py` 解析，且 `all_units` 数量与矩阵行数相同。

用法：python check_task_matrix.py [--verbose]
退出码：0 = 一致，1 = 存在漂移。
"""

import argparse
import importlib.util
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TASKS = ROOT / ".agents" / "skills" / "cpp-content" / "references" / "tasks"
GEN = ROOT / ".agents" / "skills" / "python-tools" / "scripts" / "maintenance" / "generate_tasks.py"
SCOPE = ROOT / ".agents" / "skills" / "agent-ops" / "scripts" / "scope.py"
HEADER = "| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |"
PREFIX = {
    "ENV": "getting-started", "LANG": "language-basics", "STD": "standard-library",
    "MEM": "memory", "PERF": "performance", "DBG": "debugging", "TOOL": "toolchain",
    "REF": "reference",
}
ID_RE = re.compile(r"^\| `(TASK-([A-Z]+)-(\d{3}))` ")
PATH_RE = re.compile(r"`([^`]+)`")
BUILD_DIRS = ("build", ".cache")


def load(name, path):
    """按路径加载脚本为模块（这些脚本不是包，不能直接 import）。"""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def text(path):
    return io.open(path, encoding="utf-8").read()


def paths_in(cell):
    """取单元格里的仓库路径，去掉占位与产物目录。"""
    out = []
    for cand in PATH_RE.findall(cell):
        cand = cand.strip().rstrip("/")
        if cand.startswith(("content/", "code/", ".agents/", "knowledge/")) and "build/" not in cand:
            out.append(cand)
    return out


def parse_matrix(path):
    """返回 (公共必读, 行列表)。行字段与 scope.parse_matrix 同源，另存原始单元格。"""
    common, rows = [], []
    for ln in text(path).splitlines():
        if ln.lstrip().startswith("- **必读**") and not common:
            common = paths_in(ln)
        m = ID_RE.match(ln)
        if not m:
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append({
            "tid": m.group(1), "prefix": m.group(2), "num": int(m.group(3)),
            "chapter": cells[1], "status": cells[2], "dep": cells[3].strip("`"),
            "body": cells[4], "example": cells[5], "spec": cells[6], "cells": cells,
        })
    return common, rows


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="任务矩阵一致性体检")
    ap.add_argument("--verbose", action="store_true", help="打印每个矩阵的行数与状态分布")
    args = ap.parse_args()

    bad = []
    yml = text(ROOT / "_quarto.yml")
    matrices = sorted(TASKS.glob("*.md"))
    if len(matrices) != len(set(PREFIX.values())):
        bad.append(f"part 矩阵数量 {len(matrices)}，应为 {len(set(PREFIX.values()))}")

    seen_ids, rows_by_part = {}, {}
    for path in matrices:
        part = path.stem
        body = text(path)
        if HEADER not in body:
            bad.append(f"{path.name}: 缺标准表头，scope 无法解析")
        common, rows = parse_matrix(path)
        if not common:
            bad.append(f"{path.name}: 缺 `- **必读**` 公共必读行")
        if not rows:
            bad.append(f"{path.name}: 解析到 0 行任务")
        for ref in common:
            if not (ROOT / ref).is_file():
                bad.append(f"{path.name}: 公共必读不存在 {ref}")

        for index, row in enumerate(rows, 1):
            where = f"{path.name}:{row['tid']}"
            if PREFIX.get(row["prefix"]) != part:
                bad.append(f"{where}: ID 前缀与 part 不匹配")
            if row["num"] != index:
                bad.append(f"{where}: 编号不连续（期望 {index:03d}）")
            if row["tid"] in seen_ids:
                bad.append(f"{where}: ID 与 {seen_ids[row['tid']]} 重复")
            seen_ids[row["tid"]] = part
            if row["status"] not in ("todo", "done") and not row["status"].startswith("merged"):
                bad.append(f"{where}: 状态取值非法 {row['status']}")
            for ref in paths_in(row["spec"]):
                if not (ROOT / ref).is_file():
                    bad.append(f"{where}: 专项必读不存在 {ref}")

            expect_body = f"`content/{part}/{row['chapter']}.qmd`"
            merged = row["status"].startswith("merged")
            if merged:
                if "不新建" not in row["body"]:
                    bad.append(f"{where}: merged 章正文列应写「—（不新建）」，实际 {row['body']}")
            elif row["body"] != expect_body:
                bad.append(f"{where}: 正文列应为 {expect_body}，实际 {row['body']}")

            qmd = ROOT / "content" / part / f"{row['chapter']}.qmd"
            if row["status"] == "done":
                if not qmd.is_file():
                    bad.append(f"{where}: 标记 done 但正文缺失")
                elif f"content/{part}/{row['chapter']}.qmd" not in yml:
                    bad.append(f"{where}: 正文未在 `_quarto.yml` 注册")
            elif qmd.is_file():
                bad.append(f"{where}: 状态 {row['status']} 但正文已存在，未更新状态列")

            if not merged:
                for ref in paths_in(row["example"]):
                    target = ROOT / ref
                    if row["status"] == "done" and not target.exists():
                        bad.append(f"{where}: 示例路径不存在 {ref}")
                    elif (
                        row["status"] == "done"
                        and target.is_dir()
                        and any(path.suffix == ".cpp" for path in target.rglob("*.cpp"))
                        and not (target / "build-and-run.sh").is_file()
                    ):
                        bad.append(f"{where}: 可编译示例缺少一键脚本 {ref}/build-and-run.sh")
        rows_by_part[part] = rows
        if args.verbose:
            done = sum(1 for r in rows if r["status"] == "done")
            merged_n = sum(1 for r in rows if r["status"].startswith("merged"))
            print(f"      {path.name}: {len(rows)} 行（done {done}、merged {merged_n}、"
                  f"todo {len(rows) - done - merged_n}）")

    for path_part, rows in rows_by_part.items():
        for row in rows:
            if row["dep"] and row["dep"] not in ("—", "-") and row["dep"] not in seen_ids:
                bad.append(f"{path_part}:{row['tid']} 依赖不存在的前置 {row['dep']}")

    total = sum(len(v) for v in rows_by_part.values())
    try:
        scope = load("scope", SCOPE)
        for part, rows in rows_by_part.items():
            for row in rows:
                if scope.find_chapter(f"{part}/{row['chapter']}", ROOT) is None:
                    bad.append(f"{part}:{row['tid']} scope 无法解析 {part}/{row['chapter']}")
        units = scope.all_units(ROOT)
        if len(units) != total:
            bad.append(f"scope --list 单元数 {len(units)} 与矩阵行数 {total} 不一致")
    except Exception as exc:
        bad.append(f"scope 校验不可用：{exc}")

    try:
        gen = load("generate_tasks", GEN)
        for part, expected in gen.build().items():
            disk = TASKS / f"{part}.md"
            if not disk.is_file() or text(disk) != expected:
                bad.append(f"{part}.md 与 generate_tasks.py 章节表不一致（跑 --write 或修 CHAPTERS）")
    except Exception as exc:
        bad.append(f"生成脚本比对不可用：{exc}")

    if bad:
        print(f"FAIL  tasks 矩阵漂移 {len(bad)} 处：")
        for item in bad:
            print(f"      {item}")
        return 1
    print(f"PASS  tasks 矩阵一致：{len(matrices)} 个 part / {total} 章，"
          "无幽灵依赖、无失效读取项、与生成脚本同步")
    return 0


if __name__ == "__main__":
    sys.exit(main())
