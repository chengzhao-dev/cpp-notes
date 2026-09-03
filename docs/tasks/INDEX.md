# 任务总表

执行单任务：先 `python scripts/agent/run.py scope <part>/<chapter>` 取读写边界，再按任务单执行。
进度只改本表「状态」列（任务单文件本身不回改）。

## 基础设施（infra）

TASK-INFRA-001 ~ 007 已全部完成，逐条任务单已归档到 [infra/DONE.md](infra/DONE.md)。
新的基建任务直接在 `docs/tasks/infra/` 建文件并在此登记。

## 主题（theme）

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-THEME-001 | todo | quarto-theme | [theme/001-tokens.md](theme/001-tokens.md) | 006 |
| TASK-THEME-002 | todo | quarto-theme | [theme/002-nav-sidebar.md](theme/002-nav-sidebar.md) | 006 |
| TASK-THEME-003 | todo | quarto-theme | [theme/003-content-code.md](theme/003-content-code.md) | 006 |
| TASK-THEME-004 | todo | quarto-theme | [theme/004-callouts-landing.md](theme/004-callouts-landing.md) | 006 |
| TASK-THEME-005 | todo | quarto-theme | [theme/005-mermaid-includes.md](theme/005-mermaid-includes.md) | 006 |
| TASK-THEME-006 | todo | quarto-theme | [theme/006-layout-check.md](theme/006-layout-check.md) | 001–005 |

## 内容 · getting-started

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-ENV-001 | done | quarto-docs / cpp-content | [content/getting-started/setup-wsl2.md](content/getting-started/setup-wsl2.md) | 007 |
| TASK-ENV-002 | merged | quarto-docs / cpp-content | [content/getting-started/install-toolchain.md](content/getting-started/install-toolchain.md) | 001 |
| TASK-ENV-003 | done | quarto-docs / cpp-content | [content/getting-started/first-program.md](content/getting-started/first-program.md) | 001 |
| TASK-ENV-004 | todo | quarto-docs / cpp-content | [content/getting-started/cmake-intro.md](content/getting-started/cmake-intro.md) | 003 |

## 内容 · core

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-CORE-001 | todo | cpp-content / quarto-docs | [content/core/intro.md](content/core/intro.md) | ENV-003 |
| TASK-CORE-002 | todo | cpp-content / quarto-docs | [content/core/variables.md](content/core/variables.md) | 001 |
| TASK-CORE-003 | todo | cpp-content / quarto-docs | [content/core/operators.md](content/core/operators.md) | 002 |
| TASK-CORE-004 | todo | cpp-content / quarto-docs | [content/core/control-flow.md](content/core/control-flow.md) | 003 |
| TASK-CORE-005 | todo | cpp-content / quarto-docs | [content/core/functions.md](content/core/functions.md) | 004 |
| TASK-CORE-006 | todo | cpp-content / quarto-docs | [content/core/arrays-strings.md](content/core/arrays-strings.md) | 005 |
| TASK-CORE-007 | todo | cpp-content / quarto-docs | [content/core/structs-classes.md](content/core/structs-classes.md) | 006 |
| TASK-CORE-008 | todo | cpp-content / quarto-docs | [content/core/references.md](content/core/references.md) | 007 |

## 内容 · stl

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-STL-001 | todo | cpp-content / quarto-docs | [content/stl/intro-stl.md](content/stl/intro-stl.md) | CORE-005 |
| TASK-STL-002 | todo | cpp-content / quarto-docs | [content/stl/vector.md](content/stl/vector.md) | 001 |
| TASK-STL-003 | todo | cpp-content / quarto-docs | [content/stl/map-set.md](content/stl/map-set.md) | 002 |
| TASK-STL-004 | todo | cpp-content / quarto-docs | [content/stl/iterators.md](content/stl/iterators.md) | 002 |
| TASK-STL-005 | todo | cpp-content / quarto-docs | [content/stl/algorithms.md](content/stl/algorithms.md) | 004 |

## 内容 · memory

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-MEM-001 | todo | cpp-content / quarto-docs | [content/memory/stack-heap.md](content/memory/stack-heap.md) | CORE-007 |
| TASK-MEM-002 | todo | cpp-content / quarto-docs | [content/memory/raii.md](content/memory/raii.md) | 001 |
| TASK-MEM-003 | todo | cpp-content / quarto-docs | [content/memory/smart-pointers.md](content/memory/smart-pointers.md) | 002 |
| TASK-MEM-004 | todo | cpp-content / quarto-docs | [content/memory/move-semantics.md](content/memory/move-semantics.md) | 003 |

## 内容 · performance

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-PERF-001 | todo | cpp-content / quarto-docs | [content/performance/profiling.md](content/performance/profiling.md) | MEM-002 |
| TASK-PERF-002 | todo | cpp-content / quarto-docs | [content/performance/cache-locality.md](content/performance/cache-locality.md) | 001 |
| TASK-PERF-003 | todo | cpp-content / quarto-docs | [content/performance/rvo-nrvo.md](content/performance/rvo-nrvo.md) | MEM-004 |

## 内容 · debugging

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-DBG-001 | todo | cpp-content / quarto-docs | [content/debugging/gdb-basics.md](content/debugging/gdb-basics.md) | ENV-003 |
| TASK-DBG-002 | todo | cpp-content / quarto-docs | [content/debugging/sanitizers.md](content/debugging/sanitizers.md) | 001 |
| TASK-DBG-003 | todo | cpp-content / quarto-docs | [content/debugging/common-bugs.md](content/debugging/common-bugs.md) | 001 |

## 内容 · toolchain

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-TOOL-001 | todo | cpp-content / quarto-docs | [content/toolchain/cmake-targets.md](content/toolchain/cmake-targets.md) | ENV-004 |
| TASK-TOOL-002 | todo | cpp-content / quarto-docs | [content/toolchain/clang-tools.md](content/toolchain/clang-tools.md) | 001 |
| TASK-TOOL-003 | todo | cpp-content / quarto-docs | [content/toolchain/project-layout.md](content/toolchain/project-layout.md) | 001 |

## 内容 · cheatsheet

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-CS-001 | todo | cpp-content / quarto-docs | [content/cheatsheet/syntax-ref.md](content/cheatsheet/syntax-ref.md) | CORE-008 |
| TASK-CS-002 | todo | cpp-content / quarto-docs | [content/cheatsheet/stl-ref.md](content/cheatsheet/stl-ref.md) | STL-005 |
