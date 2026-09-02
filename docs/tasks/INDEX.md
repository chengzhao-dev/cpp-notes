# 任务总表

执行单任务：`@docs/tasks/<path>.md` + 「执行 TASK-xxx」。进度只改本表「状态」列。

## 基础设施（infra）

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-INFRA-001 | done | quarto-docs / cpp-content | [infra/001-skill-migrate.md](infra/001-skill-migrate.md) | — |
| TASK-INFRA-002 | done | github-ops | [infra/002-delete-opencode.md](infra/002-delete-opencode.md) | 001 |
| TASK-INFRA-003 | done | quarto-docs | [infra/003-docs-framework.md](infra/003-docs-framework.md) | — |
| TASK-INFRA-004 | done | cpp-content | [infra/004-script-cleanup.md](infra/004-script-cleanup.md) | 002 |
| TASK-INFRA-004b | done | quarto-docs | [infra/004b-python-style.md](infra/004b-python-style.md) | 004 |
| TASK-INFRA-005 | done | github-ops | [infra/005-ci-verify.md](infra/005-ci-verify.md) | 004 |
| TASK-INFRA-006 | done | quarto-docs / quarto-theme | [infra/006-prune-merge.md](infra/006-prune-merge.md) | 004b |
| TASK-INFRA-007 | done | quarto-docs / cpp-content | [infra/007-slim-content.md](infra/007-slim-content.md) | 006 |

## 主题（theme）

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-THEME-001 | todo | quarto-theme | [theme/001-tokens.md](theme/001-tokens.md) | 006 |
| TASK-THEME-002 | todo | quarto-theme | [theme/002-nav-sidebar.md](theme/002-nav-sidebar.md) | 006 |
| TASK-THEME-003 | todo | quarto-theme | [theme/003-content-code.md](theme/003-content-code.md) | 006 |
| TASK-THEME-004 | todo | quarto-theme | [theme/004-callouts-landing.md](theme/004-callouts-landing.md) | 006 |
| TASK-THEME-005 | todo | quarto-theme | [theme/005-mermaid-includes.md](theme/005-mermaid-includes.md) | 006 |
| TASK-THEME-006 | todo | quarto-theme | [theme/006-layout-check.md](theme/006-layout-check.md) | 001–005 |

## 内容 · environment

| ID | 状态 | Skill | 任务文件 | 依赖 |
|---|---|---|---|---|
| TASK-ENV-001 | done | quarto-docs / cpp-content | [content/environment/setup-wsl2.md](content/environment/setup-wsl2.md) | 007 |
| TASK-ENV-002 | todo | quarto-docs / cpp-content | [content/environment/install-toolchain.md](content/environment/install-toolchain.md) | 001 |
| TASK-ENV-003 | todo | quarto-docs / cpp-content | [content/environment/first-program.md](content/environment/first-program.md) | 002 |
| TASK-ENV-004 | todo | quarto-docs / cpp-content | [content/environment/cmake-intro.md](content/environment/cmake-intro.md) | 003 |

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
