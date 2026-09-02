#!/usr/bin/env python3
"""生成 docs/tasks 下的任务单文件。"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASKS = ROOT / "docs" / "tasks"

TEMPLATE = """# {task_id} · {title}

- **状态**: {status}
- **Skill**: {skill}
- **依赖**: {deps}

## 读写边界

- **必读**: [`AGENTS.md`](../../AGENTS.md)；本文件{extra_read}
- **可写**: {writable}
- **禁止**: {forbidden}

## 验收

{acceptance}

## Cursor 提示词

> 执行 {task_id}。只读「读写边界」所列文件；完成验收清单。
"""


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def infra():
    items = [
        ("001-skill-migrate", "TASK-INFRA-001", "Skill 迁移", "done",
         "quarto-docs / cpp-content", "—",
         "`.cursor/skills/**`", "`content/`、`theme/`",
         "- [x] cpp/quarto/github 参考补齐\n- [x] cases 合并为 4 文件\n- [x] writing-style-core.md"),
        ("002-delete-opencode", "TASK-INFRA-002", "删除 opencode", "done",
         "github-ops", "001",
         "根文档", "`.opencode/`（已删）",
         "- [x] 无 `.opencode/` 引用"),
        ("003-docs-framework", "TASK-INFRA-003", "docs 框架", "done",
         "quarto-docs", "—",
         "`docs/**`、瘦身 `AGENTS.md`", "—",
         "- [x] structure.md、tasks/INDEX.md、agent/"),
        ("004-script-cleanup", "TASK-INFRA-004", "脚本收尾", "done",
         "cpp-content", "002",
         "`scripts/**`", "—",
         "- [x] init_cpp_project bare/simple\n- [x] 无 cpp-project skill"),
        ("004b-python-style", "TASK-INFRA-004b", "Python 规范", "done",
         "quarto-docs", "004",
          "`.py`、`scripts/pyproject.toml`、`docs/agent/python-scripts.md`", "—",
         "- [x] Black + 中文注释约定"),
        ("005-ci-verify", "TASK-INFRA-005", "CI 校验", "done",
         "github-ops", "004",
         "`.github/workflows/*`", "—",
         "- [x] render-check 跑 verify_examples.py"),
        ("006-prune-merge", "TASK-INFRA-006", "精简合并", "done",
         "quarto-docs / quarto-theme", "004b",
         "见计划 §八", "—",
         "- [x] 删 assets、full 模板\n- [x] misc.css→base.css"),
        ("007-slim-content", "TASK-INFRA-007", "内容精简", "done",
         "quarto-docs / cpp-content", "006",
         "skills 参考、现有 qmd", "—",
         "- [x] writing-style-core\n- [x] setup-wsl2 ≤180 行"),
    ]
    for fname, tid, title, status, skill, deps, writable, forbidden, acc in items:
        write(TASKS / "infra" / f"{fname}.md", TEMPLATE.format(
            task_id=tid, title=title, status=status, skill=skill, deps=deps,
            extra_read="", writable=writable, forbidden=forbidden, acceptance=acc))


def theme():
    items = [
        ("001-tokens", "TASK-THEME-001", "tokens + SCSS", "todo",
         "`theme/css/tokens.css`、`theme/scss/*`", "`content/`"),
        ("002-nav-sidebar", "TASK-THEME-002", "导航与侧栏", "todo",
         "`theme/css/nav.css`、`sidebar.css`", "`content/`"),
        ("003-content-code", "TASK-THEME-003", "正文与代码块", "todo",
         "`theme/css/content.css`、`code.css`", "`content/`"),
        ("004-callouts-landing", "TASK-THEME-004", "Callout 与首页", "todo",
         "`theme/css/callouts.css`、`landing.css`", "`content/`"),
        ("005-mermaid-includes", "TASK-THEME-005", "Mermaid 与 includes", "todo",
         "`theme/css/mermaid.css`、`theme/includes/`", "`content/`"),
        ("006-layout-check", "TASK-THEME-006", "布局验收", "todo",
         "跑 check_layout.py", "`content/`"),
    ]
    for fname, tid, title, status, writable, forbidden in items:
        write(TASKS / "theme" / f"{fname}.md", TEMPLATE.format(
            task_id=tid, title=title, status=status, skill="quarto-theme",
            deps="TASK-INFRA-006", extra_read="；`design-tokens.md`",
            writable=writable, forbidden=forbidden,
            acceptance="- [ ] 改后 quarto render\n- [ ] check_layout 通过"))


def content():
    chapters = [
        ("environment", "setup-wsl2", "TASK-ENV-001", "搭建 WSL2 环境", "done", "007", "toolchain.md"),
        ("environment", "install-toolchain", "TASK-ENV-002", "安装工具链", "todo", "001", "toolchain.md"),
        ("environment", "first-program", "TASK-ENV-003", "第一个程序", "todo", "002", "cpp.md"),
        ("environment", "cmake-intro", "TASK-ENV-004", "CMake 入门", "todo", "003", "toolchain.md"),
        ("core", "intro", "TASK-CORE-001", "C++ 简介", "todo", "ENV-003", "cpp.md"),
        ("core", "variables", "TASK-CORE-002", "变量与类型", "todo", "001", "cpp.md"),
        ("core", "operators", "TASK-CORE-003", "运算符", "todo", "002", "cpp.md"),
        ("core", "control-flow", "TASK-CORE-004", "控制流", "todo", "003", "cpp.md"),
        ("core", "functions", "TASK-CORE-005", "函数", "todo", "004", "cpp.md"),
        ("core", "arrays-strings", "TASK-CORE-006", "数组与字符串", "todo", "005", "cpp.md"),
        ("core", "structs-classes", "TASK-CORE-007", "结构体与类", "todo", "006", "cpp.md"),
        ("core", "references", "TASK-CORE-008", "引用", "todo", "007", "cpp.md"),
        ("stl", "intro-stl", "TASK-STL-001", "STL 简介", "todo", "CORE-005", "stl.md"),
        ("stl", "vector", "TASK-STL-002", "vector", "todo", "001", "stl.md"),
        ("stl", "map-set", "TASK-STL-003", "map 与 set", "todo", "002", "stl.md"),
        ("stl", "iterators", "TASK-STL-004", "迭代器", "todo", "002", "stl.md"),
        ("stl", "algorithms", "TASK-STL-005", "算法", "todo", "004", "stl.md"),
        ("memory", "stack-heap", "TASK-MEM-001", "栈与堆", "todo", "CORE-007", "modern-cpp.md"),
        ("memory", "raii", "TASK-MEM-002", "RAII", "todo", "001", "modern-cpp.md"),
        ("memory", "smart-pointers", "TASK-MEM-003", "智能指针", "todo", "002", "modern-cpp.md"),
        ("memory", "move-semantics", "TASK-MEM-004", "移动语义", "todo", "003", "modern-cpp.md"),
        ("performance", "profiling", "TASK-PERF-001", "性能分析", "todo", "MEM-002", "performance.md"),
        ("performance", "cache-locality", "TASK-PERF-002", "缓存局部性", "todo", "001", "performance.md"),
        ("performance", "rvo-nrvo", "TASK-PERF-003", "RVO/NRVO", "todo", "MEM-004", "performance.md"),
        ("debugging", "gdb-basics", "TASK-DBG-001", "GDB 基础", "todo", "ENV-003", "pitfalls-ub.md"),
        ("debugging", "sanitizers", "TASK-DBG-002", "Sanitizer", "todo", "001", "pitfalls-ub.md"),
        ("debugging", "common-bugs", "TASK-DBG-003", "常见 bug", "todo", "001", "pitfalls-ub.md"),
        ("toolchain", "cmake-targets", "TASK-TOOL-001", "CMake 目标", "todo", "ENV-004", "engineering.md"),
        ("toolchain", "clang-tools", "TASK-TOOL-002", "Clang 工具", "todo", "001", "code-style.md"),
        ("toolchain", "project-layout", "TASK-TOOL-003", "项目布局", "todo", "001", "engineering.md"),
        ("cheatsheet", "syntax-ref", "TASK-CS-001", "语法速查", "todo", "CORE-008", "cpp.md"),
        ("cheatsheet", "stl-ref", "TASK-CS-002", "STL 速查", "todo", "STL-005", "stl.md"),
    ]
    for part, chapter, tid, title, status, dep, ref in chapters:
        extra = (
            f"；`.cursor/skills/quarto-docs/references/quarto/authoring.md`；"
            f"`.cursor/skills/quarto-docs/references/zh/writing-style-core.md`；"
            f"`.cursor/skills/cpp-content/references/cpp/{ref}`"
        )
        writable = (
            f"`content/{part}/{chapter}.qmd`；`code/{part}/{chapter}*.cpp`；"
            f"`_quarto.yml`（追加本章）"
        )
        acc = (
            "- [ ] qmd 符合体量预算\n"
            "- [ ] verify_examples.py 通过\n"
            "- [ ] quarto render 通过\n"
            "- [ ] INDEX.md 更新为 done"
        )
        if status == "done":
            acc = acc.replace("- [ ]", "- [x]", 1).replace("- [ ]", "- [x]", 1)
        write(TASKS / "content" / part / f"{chapter}.md", TEMPLATE.format(
            task_id=tid, title=title, status=status,
            skill="cpp-content + quarto-docs", deps=f"TASK-{dep}" if not dep.startswith("TASK") else dep,
            extra_read=extra, writable=writable, forbidden=f"`theme/`、`content/<其他 part>/`",
            acceptance=acc))


if __name__ == "__main__":
    infra()
    theme()
    content()
    print("Generated task files.")
