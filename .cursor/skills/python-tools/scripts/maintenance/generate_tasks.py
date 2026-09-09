#!/usr/bin/env python3
"""由单一章节表生成 8 个 part 任务矩阵（`cpp-content/references/tasks/<part>.md`）。

为什么需要它：矩阵是 `scope.py` 的唯一路由表，也是章节状态的权威记录。手工维护 8 个文件
容易写歪表头、漏掉「公共必读」交集、或让 scope 解析不到刚登记的章节；本脚本把这些规则
固化成一次生成，并用 --check 与磁盘比对，防止脚本与内容再次脱节。

数据契约（与 scope.py 的解析规则一一对应，改格式必须两处同改）：
  - 每行一章，列顺序固定：ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注
  - 行以 "| `TASK-" 开头，且至少 8 格；`—` 表示空；正文/示例只写第一个反引号路径
  - 「公共必读」行由本 part 全部章节的必读交集推导（scope.py 把该行作为通用 READ）

用法：
  python generate_tasks.py --check   # 只比对，报告漂移；退出码 1 = 磁盘与表不一致（默认）
  python generate_tasks.py --write   # 用表覆盖重写 8 个矩阵
退出码：0 = 一致 / 写入成功；1 = 存在漂移（check 模式）。
"""

import argparse
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TASKS = ROOT / ".cursor" / "skills" / "cpp-content" / "references" / "tasks"
SKILL_REFS = ".cursor/skills/"

# 所有 part 共用的写作规范必读（专项 ref 之外的最小公共集）
COMMON_BASE = [
    SKILL_REFS + "quarto-docs/references/quarto/authoring.md",
    SKILL_REFS + "quarto-docs/references/zh/writing-style-core.md",
]
PREFIX = {
    "getting-started": "ENV", "core": "CORE", "stl": "STL", "memory": "MEM",
    "performance": "PERF", "debugging": "DBG", "toolchain": "TOOL", "cheatsheet": "CS",
}
ORDER = ["getting-started", "core", "stl", "memory", "performance", "debugging", "toolchain", "cheatsheet"]


def cpp(name):
    """cpp-content 的专项 reference 路径。"""
    return SKILL_REFS + f"cpp-content/references/cpp/{name}"


# 一行一章：(part, chapter, status, dep, spec, code, note)
#   status: todo | done | merged
#   dep:    前置任务完整 ID，无前置写 None
#   spec:   专项必读（reference 文件名），无差异写 None —— 与公共集相同即无专项
#   code:   示例路径覆盖；None 表示按默认单文件 code/<part>/<chapter>.cpp
CHAPTERS = [
    ("getting-started", "setup-wsl2", "done", None, "engineering.md", "—（本章无示例）", "—"),
    ("getting-started", "install-toolchain", "merged", "TASK-ENV-001", None, None,
     "已并入 ENV-001 的「安装 C++ 构建工具链」一节，勿再新建同名 qmd"),
    ("getting-started", "first-program", "done", "TASK-ENV-001", "cpp.md",
     "code/getting-started/first-program/", "先 g++ 直编，再最小 CMakeLists；多文件与目标留给 cmake-intro"),
    ("getting-started", "cmake-intro", "todo", "TASK-ENV-003", "engineering.md", None, "—"),
    ("core", "intro", "todo", "TASK-ENV-003", "cpp.md", None, "—"),
    ("core", "variables", "todo", "TASK-CORE-001", "cpp.md", None, "—"),
    ("core", "operators", "todo", "TASK-CORE-002", "cpp.md", None, "—"),
    ("core", "control-flow", "todo", "TASK-CORE-003", "cpp.md", None, "—"),
    ("core", "functions", "todo", "TASK-CORE-004", "cpp.md", None, "—"),
    ("core", "arrays-strings", "todo", "TASK-CORE-005", "cpp.md", None, "—"),
    ("core", "structs-classes", "todo", "TASK-CORE-006", "cpp.md", None, "—"),
    ("core", "references", "todo", "TASK-CORE-007", "cpp.md", None, "—"),
    ("stl", "intro-stl", "todo", "TASK-CORE-005", "stl.md", None, "—"),
    ("stl", "vector", "todo", "TASK-STL-001", "stl.md", None, "—"),
    ("stl", "map-set", "todo", "TASK-STL-002", "stl.md", None, "—"),
    ("stl", "iterators", "todo", "TASK-STL-002", "stl.md", None, "—"),
    ("stl", "algorithms", "todo", "TASK-STL-004", "stl.md", None, "—"),
    ("memory", "stack-heap", "todo", "TASK-CORE-007", "modern-cpp.md", None, "—"),
    ("memory", "raii", "todo", "TASK-MEM-001", "modern-cpp.md", None, "—"),
    ("memory", "smart-pointers", "todo", "TASK-MEM-002", "modern-cpp.md", None, "—"),
    ("memory", "move-semantics", "todo", "TASK-MEM-003", "modern-cpp.md", None, "—"),
    ("performance", "profiling", "todo", "TASK-MEM-002", "performance-and-pitfalls.md", None, "—"),
    ("performance", "cache-locality", "todo", "TASK-PERF-001", "performance-and-pitfalls.md", None, "—"),
    ("performance", "rvo-nrvo", "todo", "TASK-MEM-004", "performance-and-pitfalls.md", None, "—"),
    ("debugging", "gdb-basics", "todo", "TASK-ENV-003", "performance-and-pitfalls.md", None, "—"),
    ("debugging", "sanitizers", "todo", "TASK-DBG-001", "performance-and-pitfalls.md", None, "—"),
    ("debugging", "common-bugs", "todo", "TASK-DBG-001", "performance-and-pitfalls.md", None, "—"),
    ("toolchain", "cmake-targets", "todo", "TASK-ENV-004", "engineering.md", None, "—"),
    ("toolchain", "clang-tools", "todo", "TASK-TOOL-001", "code-style.md", None, "—"),
    ("toolchain", "project-layout", "todo", "TASK-TOOL-001", "engineering.md", None, "—"),
    ("cheatsheet", "syntax-ref", "todo", "TASK-CORE-008", "cpp.md", None, "—"),
    ("cheatsheet", "stl-ref", "todo", "TASK-STL-005", "stl.md", None, "—"),
]


def task_id(part, chapter):
    """按 part 前缀与章节在表中的序号生成任务 ID（顺序即矩阵里的编号）。"""
    rows = [c for c in CHAPTERS if c[0] == part]
    index = [c[1] for c in rows].index(chapter) + 1
    return f"TASK-{PREFIX[part]}-{index:03d}"


def render(part, rows):
    """渲染一个 part 的矩阵文本。rows 已按 ID 升序。"""
    reqs = [COMMON_BASE + ([cpp(spec)] if spec and not _is_merged(status) else [])
            for part_, chapter, status, dep, spec, code, note in rows]
    commons = sorted(set.intersection(*[set(r) for r in reqs]))
    lines = [
        f"# {part} 章节任务矩阵", "",
        f"本文件是 {part} 全部章节任务的唯一权威记录：一行一章，读写边界与验收在文件级统一，"
        "只有差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。", "",
        "## 公共读写边界", "",
        "- **必读**: `AGENTS.md`；本文件；" + "；".join(f"`{p}`" for p in commons),
        "- **可写**: 本行「正文」与「示例」所列路径，以及 `_quarto.yml`（追加本章）",
        "- **禁止**: `.cursor/skills/quarto-theme/assets/theme/`、`content/<其他 part>/`、"
        "示例目录下的 `build/`（CMake 产物）", "",
        "示例默认单文件 `code/<part>/<chapter>.cpp`；需要构建工程时改用同名子目录，产物落其 `build/`。", "",
        "## 统一验收（每章完成时逐项确认）", "",
        "- [ ] 正文符合体量预算，`run.py check` 与 `run.py render` 通过",
        "- [ ] 示例经 `run.py verify --changed` 编译通过，正文承诺的输出与实测一致",
        "- [ ] 本文件「状态」列已更新为 `done`", "",
        "## 任务矩阵", "",
        "| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for (part_, chapter, status, dep, spec, code, note), required in zip(rows, reqs):
        tid = task_id(part_, chapter)
        extra = sorted(set(required) - set(commons))
        if _is_merged(status):
            body, example, spec_cell = "—（不新建）", "—", "—"
        else:
            body = f"`content/{part_}/{chapter}.qmd`"
            example = (f"`code/{part_}/{chapter}.cpp`" if code is None
                       else code if code.startswith("—") else f"`{code}`")
            spec_cell = "；".join(f"`{p}`" for p in extra) or "—"
        lines.append("| `{}` | {} | {} | {} | {} | {} | {} | {} |".format(
            tid, chapter, status, f"`{dep}`" if dep else "—", body, example, spec_cell, note))
    return "\n".join(lines) + "\n"


def _is_merged(status):
    return status.startswith("merged")


def build():
    """返回 {part: 矩阵文本}。"""
    out = {}
    for part in ORDER:
        rows = sorted((c for c in CHAPTERS if c[0] == part), key=lambda c: task_id(c[0], c[1]))
        out[part] = render(part, rows)
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="生成任务矩阵")
    ap.add_argument("--write", action="store_true", help="覆盖写入矩阵（默认只比对）")
    ap.add_argument("--check", action="store_true", help="只比对磁盘，报告漂移")
    args = ap.parse_args()

    drift = []
    for part, text in build().items():
        path = TASKS / f"{part}.md"
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current == text:
            continue
        drift.append(part)
        if args.write:
            io.open(path, "w", encoding="utf-8", newline="\n").write(text)

    if args.write:
        print(f"已写入 {len(ORDER)} 个矩阵，其中 {len(drift)} 个发生变化。")
        return 0
    if drift:
        print(f"DRIFT: {len(drift)} 个矩阵与章节表不一致：{', '.join(drift)}")
        print("确认以脚本为准时运行 generate_tasks.py --write；否则先修 CHAPTERS。")
        return 1
    print(f"OK: {len(ORDER)} 个矩阵与章节表一致，共 {len(CHAPTERS)} 章。")
    return 0


if __name__ == "__main__":
    sys.exit(main())