# language-basics 章节任务矩阵

本文件是 language-basics 章节任务的唯一权威记录：一行一章，读写边界与验收文件级统一，差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。

## 公共读写边界

- **必读**: `AGENTS.md`、本文件、`.agents/skills/writing-cpp/references/cpp/cpp.md`、`.agents/skills/writing-cpp/references/cpp/language-basics.md`、`.agents/skills/writing-quarto/references/quarto/authoring.md`、`.agents/skills/writing-quarto/references/zh/chapter-writing.md`
- **可写**: 本表「正文」与「示例」路径与 `_quarto.yml`（追加本章）
- **禁止**: `.agents/skills/designing-theme/assets/theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

示例是 `code/language-basics/<chapter>.cpp`，由分册根 `CMakeLists.txt` 收集；源码链接写进 `## 本章回顾`。骨架为任务序列、常见错误、自测与回顾。

## 统一验收

- [ ] 正文符合体量预算，`run.py check --profile fast` 与 `run.py render` 通过
- [ ] 示例经 `run.py verify --changed` 编译通过，正文承诺的输出与实测一致
- [ ] 本表「状态」列已更新为 `done`

## 任务矩阵

| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `TASK-LANG-001` | types-and-variables | done | `TASK-ENV-004` | `content/language-basics/types-and-variables.qmd` | `code/language-basics/types-and-variables.cpp` | —（文件级已含） | 基础类型、变量与全局/块作用域，不使用 `std::string` |
| `TASK-LANG-002` | initialization-and-type-inference | done | `TASK-LANG-001` | `content/language-basics/initialization-and-type-inference.qmd` | `code/language-basics/initialization-and-type-inference.cpp` | —（文件级已含） | 列表初始化、赋值、`auto` 与初始化列表推导 |
| `TASK-LANG-003` | const-variables | done | `TASK-LANG-002` | `content/language-basics/const-variables.qmd` | `code/language-basics/const-variables.cpp` | —（文件级已含） | 只讲 `const` 变量：初始化要求与 `k` 加大驼峰命名 |
| `TASK-LANG-004` | type-safety-and-numeric-bounds | done | `TASK-LANG-014` | `content/language-basics/type-safety-and-numeric-bounds.qmd` | `code/language-basics/type-safety-and-numeric-bounds.cpp` | `.agents/skills/writing-cpp/references/cpp/primitive-types-and-numeric-safety.md` | 范围、符号、溢出、转换、浮点、`bool` 与 `std::size_t` |
| `TASK-LANG-005` | operators | todo | `TASK-LANG-004` | `content/language-basics/operators.qmd` | `code/language-basics/operators.cpp` | — | 有示例之后才注册。排在数值边界之后、枚举之前 |
| `TASK-LANG-006` | control-flow | merged | `TASK-LANG-005` | —（不新建） | — | — | 已由 `branch-and-loop` 覆盖 |
| `TASK-LANG-007` | functions | done | `TASK-LANG-001` | `content/language-basics/functions.qmd` | `code/language-basics/functions.cpp` | —（文件级已含） | 按值传入并返回整数 |
| `TASK-LANG-008` | arrays-strings | todo | `TASK-LANG-007` | `content/language-basics/arrays-strings.qmd` | `code/language-basics/arrays-strings.cpp` | — | 用 string 与 vector |
| `TASK-LANG-009` | structs-classes | merged | `TASK-LANG-008` | —（不新建） | — | — | 已由 `structs-and-value-types` 与 `classes` 覆盖 |
| `TASK-LANG-010` | references | merged | `TASK-LANG-009` | —（不新建） | — | — | 已由 `reference-usage-scenarios` 覆盖 |
| `TASK-LANG-011` | enums | done | `TASK-LANG-004` | `content/language-basics/enums.qmd` | —（问题页只收片段） | —（文件级已含） | 普通 `enum` 的作用域泄漏与隐式转换，结尾链到 `TASK-LANG-018`；位掩码与 `using enum` 不讲 |
| `TASK-LANG-012` | structs-and-value-types | done | `TASK-LANG-011` | `content/language-basics/structs-and-value-types.qmd` | `code/language-basics/structs-and-value-types.cpp` | —（文件级已含） | 聚合初始化、成员默认值与值语义复制；成员函数与访问控制留给 `TASK-LANG-009` |
| `TASK-LANG-013` | constexpr | done | `TASK-LANG-003` | `content/language-basics/constexpr.qmd` | `code/language-basics/constexpr.cpp` | —（文件级已含） | 编译期规则、命名空间内 `inline constexpr` 共享与标准演化 |
| `TASK-LANG-014` | constant-keywords | done | `TASK-LANG-013` | `content/language-basics/constant-keywords.qmd` | —（对比页复用前两章示例） | —（文件级已含） | `const`、`constexpr`、`consteval`、`constinit` 与宏的对照和选型 |
| `TASK-LANG-015` | reference-usage-scenarios | done | `TASK-LANG-012` | `content/language-basics/reference-usage-scenarios.qmd` | `code/language-basics/reference-usage-scenarios.cpp` | —（文件级已含） | 按 Google「Inputs and Outputs」讲传参场景：按值、`const T&`、`T&` 与非空约定 |
| `TASK-LANG-016` | pointer-usage-scenarios | done | `TASK-LANG-015` | `content/language-basics/pointer-usage-scenarios.qmd` | `code/language-basics/pointer-usage-scenarios.cpp` | —（文件级已含） | 覆盖可空输入、可选输出与所有权入口，语法深挖留给内存分册 |
| `TASK-LANG-017` | pointers | todo | `TASK-LANG-010` | `content/language-basics/pointers.qmd` | `code/language-basics/pointers.cpp` | — | 取地址、解引用与指针运算边界，不重复 `TASK-LANG-016` 场景表，只回链 |
| `TASK-LANG-018` | enum-class | done | `TASK-LANG-011` | `content/language-basics/enum-class.qmd` | `code/language-basics/enum-class.cpp` | —（文件级已含） | `enum class` 限定名访问、显式转换、底层类型、成员注释与按值传参，不讲位掩码 |
| `TASK-LANG-019` | parameter-passing-guide | done | `TASK-LANG-016` | `content/language-basics/parameter-passing-guide.qmd` | —（速查页只收片段） | —（文件级已含） | ★ 速查：二级标题按机制（赋值、引用、指针），细节回链场景章 |
| `TASK-LANG-020` | return-value-guide | done | `TASK-LANG-019` | `content/language-basics/return-value-guide.qmd` | —（速查页只收片段） | —（文件级已含） | ★ 速查：二级标题按返回方式，结果类型表达成败而非异常 |
| `TASK-LANG-021` | const-member-functions | done | `TASK-LANG-012` | `content/language-basics/const-member-functions.qmd` | `code/language-basics/const-member-functions.cpp` | —（文件级已含） | 尾部 const 与参数、返回值、局部变量的 const 对照；成员函数语法只给最小上下文 |
| `TASK-LANG-022` | nodiscard | done | `TASK-LANG-020` | `content/language-basics/nodiscard.qmd` | `code/language-basics/nodiscard.cpp` | —（文件级已含） | `[[nodiscard]]` 采纳范围与 `static_cast<void>` 有意丢弃（`modernize-use-nodiscard`） |
| `TASK-LANG-023` | branch-and-loop | done | `TASK-LANG-007` | `content/language-basics/branch-and-loop.qmd` | `code/language-basics/branch-and-loop.cpp` | —（文件级已含） | `switch` 与 `for` |
| `TASK-LANG-024` | classes | done | `TASK-LANG-022` | `content/language-basics/classes.qmd` | `code/language-basics/classes.cpp` | —（文件级已含） | 数据放进类，查询带 `const` |
| `TASK-LANG-025` | namespaces | done | `TASK-LANG-018` | `content/language-basics/namespaces.qmd` | `code/language-basics/namespaces.cpp` | —（文件级已含） | 分组与限定名 |
| `TASK-LANG-026` | simple-project-design | done | `TASK-LANG-024` | `content/language-basics/simple-project-design.qmd` | `code/language-basics/simple-project-design.cpp` | `.agents/skills/writing-cpp/references/cpp/engineering.md` | 值类型、类与外层适配组织简单项目 |
