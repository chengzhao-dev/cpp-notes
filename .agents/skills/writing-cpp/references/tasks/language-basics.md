# language-basics 章节任务矩阵

本文件是 language-basics 全部章节任务的唯一权威记录：一行一章，读写边界与验收在文件级统一，只有差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。

## 公共读写边界

- **必读**: `AGENTS.md`、本文件、`.agents/skills/cpp-content/references/cpp/cpp.md`、`.agents/skills/cpp-content/references/cpp/language-basics.md`、`.agents/skills/quarto-docs/references/quarto/authoring.md`、`.agents/skills/quarto-docs/references/zh/chapter-writing.md`
- **可写**: 本行「正文」与「示例」所列路径，以及 `_quarto.yml`（追加本章）
- **禁止**: `.agents/skills/quarto-theme/assets/theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

示例默认单文件 `code/<part>/<chapter>.cpp`，需要构建工程时优先使用同名子目录。语言基础示例保持扁平单文件 `code/language-basics/<chapter>.cpp`，由分册根 `code/language-basics/CMakeLists.txt` 收集成同名可执行文件。正文不单设“示例源码与构建”小节，源码链接、构建入口和观察重点合并成 `## 本章回顾` 的一句正文，不重复配置与构建命令，也不写 `## 验证结果` 小节。章节骨架固定为“任务序列 → `## 常见错误` → `## 自测问题` → `## 本章回顾`”。

## 统一验收（每章完成时逐项确认）

- [ ] 正文符合体量预算，`run.py check --profile fast` 与 `run.py render` 通过
- [ ] 示例经 `run.py verify --changed` 编译通过，正文承诺的输出与实测一致
- [ ] 本文件「状态」列已更新为 `done`

## 任务矩阵

| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `TASK-LANG-001` | types-and-variables | done | `TASK-ENV-004` | `content/language-basics/types-and-variables.qmd` | `code/language-basics/types-and-variables.cpp` | `.agents/skills/cpp-content/references/cpp/language-basics.md` | 只讲基础类型、变量、全局/块作用域，不使用 `std::string` |
| `TASK-LANG-002` | initialization-and-type-inference | done | `TASK-LANG-001` | `content/language-basics/initialization-and-type-inference.qmd` | `code/language-basics/initialization-and-type-inference.cpp` | `.agents/skills/cpp-content/references/cpp/language-basics.md` | 列表初始化、赋值、`auto` 与初始化列表推导 |
| `TASK-LANG-003` | constants | done | `TASK-LANG-002` | `content/language-basics/constants.qmd` | `code/language-basics/constants.cpp` | `.agents/skills/cpp-content/references/cpp/language-basics.md` | 讲 `const`、`constexpr` 与领域中性的阈值和比例 |
| `TASK-LANG-004` | type-safety-and-numeric-bounds | done | `TASK-LANG-003` | `content/language-basics/type-safety-and-numeric-bounds.qmd` | `code/language-basics/type-safety-and-numeric-bounds.cpp` | `.agents/skills/cpp-content/references/cpp/primitive-types-and-numeric-safety.md` | 类型范围、符号、溢出、转换、浮点、`bool` 与 `std::size_t` |
| `TASK-LANG-005` | operators | todo | `TASK-LANG-004` | `content/language-basics/operators.qmd` | `code/language-basics/operators.cpp` | — | — |
| `TASK-LANG-006` | control-flow | todo | `TASK-LANG-005` | `content/language-basics/control-flow.qmd` | `code/language-basics/control-flow.cpp` | — | — |
| `TASK-LANG-007` | functions | todo | `TASK-LANG-006` | `content/language-basics/functions.qmd` | `code/language-basics/functions.cpp` | — | — |
| `TASK-LANG-008` | arrays-strings | todo | `TASK-LANG-007` | `content/language-basics/arrays-strings.qmd` | `code/language-basics/arrays-strings.cpp` | — | — |
| `TASK-LANG-009` | structs-classes | todo | `TASK-LANG-008` | `content/language-basics/structs-classes.qmd` | `code/language-basics/structs-classes.cpp` | — | — |
| `TASK-LANG-010` | references | todo | `TASK-LANG-009` | `content/language-basics/references.qmd` | `code/language-basics/references.cpp` | — | — |
