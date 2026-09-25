# C++ 写作约定入口

> 速查：示例 `-std=c++20 -Wall -Wextra` · 完整代码带 `int main` · 片段标 `// 片段` · 文件/目录纯 ASCII

## 术语速查

| 英文 | 中文 |
|---|---|
| RAII | 资源获取即初始化 |
| UB | 未定义行为 |
| lvalue / rvalue | 左值 / 右值 |
| NRVO | 命名返回值优化 |

## 章节顺序入口

概念章和工程章的讲解顺序以 `teaching-method.md` 为唯一出处。本文件只保留 C++ 语言、标准库、版本和术语的特有限制，不复制章节骨架。

## 内容参考依据

| 来源 | 用作 |
|---|---|
| C++ Primer (5th ed.) | 主线讲解顺序与术语 |
| learncpp.com | 章节拆分粒度、渐进式披露 |
| zh.cppreference.com | 译名、标准措辞、复杂度（`## 深入` 引标准时以此为准） |
| CMake 官方文档 | 构建章节的 command/variable 语义与注释措辞 |
| Google C++ Style Guide | include 顺序、排版与常量命名 |
| Qt、WebKit Coding Style | 函数、变量、参数和成员使用小驼峰的依据 |

本项目以 Google 的 include 顺序和 `clang-format` 为排版基底，把函数、变量、参数和成员调整为
小驼峰，并保留 Google 的 `kPascalCase` 常量。**例外：本仓库启用异常**，不采用 Google
的异常限制。完整取舍见标识 `cpp-naming-format-v1`。

这些来源用于不同层次：Primer 和 LearnCpp 参考教学顺序，Stroustrup 参考语言整体观，Effective C++ 参考可执行规则，cppreference 负责标准精度，它们不是逐段翻译的材料。

## Callout

Callout 的语义选择与例外式使用边界见 `.agents/skills/quarto-docs/references/quarto/authoring.md`，这里只记录 C++ 章节不应把必经步骤或普通说明放进提示框。

## 核心主题索引

| 主题 | 参考 |
|---|---|
| 变量、类型、函数、类、术语与译名 | `language-basics.md`（章节顺序）；本文件（术语、版本与资料边界） |
| 现代 C++：RAII、移动语义、智能指针、模板与泛型 | `modern-cpp.md` |
| 容器、迭代器、算法 | `stl.md` |
| 性能优化与未定义行为陷阱 | `performance-and-pitfalls.md` |
| 工程、构建与项目布局 | `engineering.md` |

## 示例约定

- 源码：`code/<part>/<name>.cpp`，与 `content/<part>/` 对齐。
- 新建工程：`python .agents/skills/python-tools/scripts/scaffold/init_project.py --name <name> --dir code/<part>`。
- 校验：`& .agents/skills/agent-ops/scripts/run.ps1 verify`。

## 命名

仓库路径和目录使用纯 ASCII kebab-case。C++ 文件使用 snake_case。标识符见
`code-style.md`，目录与章节排序见标识 `cpp-agent-repository-navigation-v1`。

## C++ 标准术语与中文资料
本文件规定中文 C++ 教程如何处理标准术语、版本和中文资料，避免译名漂亮但语义不准确。

### 术语写法

首次出现时使用“中文名称（英文名称）”，必要时补充标准拼写。例如：资源获取即初始化（Resource Acquisition Is Initialization，RAII）、未定义行为（undefined behavior，UB）。后续固定使用一种中文名称，并保留英文术语作为检索入口。

普通概念不用反引号。命令、路径、文件名、关键字、API、配置键和代码字面量保留反引号。不要把整句说明或卡片标题包进反引号。

### 版本边界

涉及 C++20、C++23 或 C++26 的特性必须标注版本。正文说明读者当前需要的行为和用法，参考链接补充完整限制。不要把实验性或较新标准特性写成所有编译器都支持。

标准库内容至少核对：

- 参数和返回值的语义。
- 复杂度和异常保证。
- 生命周期、所有权和迭代器失效。
- 特性首次进入的标准版本。
- GCC、Clang 或 CMake 当前工具链的支持边界。

### 中文资料的使用层次

中文 cppreference 和 CMake 中文文档适合查找中文术语、页面结构和常见说明。它们与英文原版、ISO C++ 草案和工具官方文档交叉确认后，才作为正文事实依据。中文资料存在译名差异时，选择最容易理解且能链接到英文术语的表达。

不要为了追求“标准”把正文写成规范条文。先给使用场景和最小示例，再在“限制”或“深入”段落说明精确语义。

### 推荐校验入口

| 目标 | 入口 |
|---|---|
| 语言和标准库语义 | [cppreference](https://en.cppreference.com/w/cpp/language) / [中文站](https://zh.cppreference.com/w/cpp/language) |
| 标准草案原文 | [eel.is C++ draft](https://eel.is/c++draft/) |
| 设计与接口原则 | [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) |
| CMake 语义 | [CMake 官方文档](https://cmake.org/cmake/help/latest/) / [中文文档](https://cmake.com.cn/cmake/help/latest) |

资料入口用于继续查阅，不代替当前章节对结论、命令和成功判据的说明。
