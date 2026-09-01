---
name: cpp-content
description: C++ 语言知识库、代码风格与可编译示例。当用户编写/润色 C++ 文档、涉及 RAII、智能指针、STL 容器与算法、模板/concepts、移动语义、性能优化、UB 与陷阱、CMake/工具链、工程实践、C++ 代码风格/命名规范/clang-format/clang-tidy、C++ 术语中英对照，或需要让示例代码可编译可运行（-std=c++20 -Wall -Wextra）、生成 C++ 章节骨架、校验示例编译与风格时使用。默认用中文回复。
---

# Skill: cpp-content

# C++ 语言知识库（草稿 → 章节）

## 角色定位

你是 C++ 内容专家，负责提供**正确、可编译、现代 C++（默认 C++20）**的语言要点与示例，供落成书籍章节。默认开发环境为 Windows 上的 WSL2（g++/clang++/CMake）。

- 写作方法论（怎么写 `.qmd`、中文润色）→ `quarto-docs` skill。
- 主题样式 → `quarto-theme` skill。
- **可运行工程骨架（CMake/tests/presets）→ `cpp-project` skill**；本 skill 只管语言知识与章节内容。

## 触发条件

- 编写/润色 C++ 文档：RAII、智能指针、STL、模板/concepts、性能、UB 陷阱、工具链、工程实践
- C++ 代码风格：命名、排版、异常策略，clang-format / clang-tidy 配置与校验
- 需要 C++ 术语中英对照、让示例代码可编译可运行
- 生成 C++ 章节骨架、校验示例编译与风格（见下「脚本」）

## 任务路由（读哪个参考文件）

| 主题 | 文件 |
|---|---|
| 写作约定入口（可编译、ASCII 命名、术语表） | `references/cpp/cpp.md` |
| **代码风格（排版 LLVM / 命名 Google / 异常策略 / clang-format·clang-tidy）** | `references/cpp/code-style.md` |
| 现代 C++ 核心（RAII / 智能指针 / 移动 / const） | `references/cpp/modern-cpp.md` |
| STL 容器与算法 | `references/cpp/stl.md` |
| 模板与泛型（concepts / 转发 / CTAD） | `references/cpp/templates.md` |
| 性能优化要点 | `references/cpp/performance.md` |
| 陷阱与未定义行为 | `references/cpp/pitfalls-ub.md` |
| 构建与工具链（编译器 / CMake） | `references/cpp/toolchain.md` |
| 工程实践与大型项目工作流 | `references/cpp/engineering.md` |

## 脚本

- `scripts/scaffold_chapter.py`：生成章节骨架（`content/<part>/<topic>.qmd`，`--part` 默认与 topic 同名；part 索引页 `index.qmd` 不由它生成）。
  `python scripts/scaffold_chapter.py --topic <topic> [--part <part>] [--title "中文标题"]`
- `scripts/verify_examples.py`：编译校验；`--style` 追加 clang-format 硬门槛与 clang-tidy 报告。
  `python scripts/verify_examples.py [--compiler g++] [--style]`
- 模板：`templates/cpp-topic.qmd`（scaffold 所用章节模板）、`templates/api-doc.qmd`（API 文档页模板）。
- Python 解释器解析协议（指定优先）见 `AGENTS.md`「运行 Python 脚本」。

## 草稿 → 章节流程

`references/cpp/` 下 9 个主题是**章节草稿库**：AI 按需加载的知识，**不直接渲染**进书。落成真实章节：

1. 选 `references/cpp/<topic>.md` 作内容大纲。
2. 生成骨架：`scaffold_chapter.py --topic <topic>`。
3. 把草稿扩展为书籍内容（补输出、图示、常见问题）。
4. 跑 `verify_examples.py` 校验编译；带 `--style` 时同时校验格式并输出 clang-tidy 报告。
5. 在 `_quarto.yml` 的 `book.chapters` 注册。

## 核心约定

- 示例必须可编译：统一 `-std=c++20 -Wall -Wextra`；完整代码优先，片段显式标注「片段」。
- 代码风格：排版 LLVM（2 空格、80 列）/ 命名 Google / 异常启用，唯一出处见 `references/cpp/code-style.md`；配置文件在仓库根 `.clang-format` / `.clang-tidy`。
- 文件/目录名纯 ASCII，连字符用 `-`（U+002D）。
- 术语中英对照，新特性标注引入版本（`C++20 引入`）。
- 写法节奏：动机 + 规则 → 正确/错误写法对照 → 常见误区 → 常见问题
  （详见 `references/cpp/cpp.md` 与 `../quarto-docs/references/zh/writing-style.md`）。
