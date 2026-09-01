# C++ 文档写作约定（入口）

本文件是 cpp-content skill（`references/cpp/`）的入口，承载 **C++ 语言本身**的要点索引与 C++ 专属约定（可编译示例、ASCII 命名、术语表、代码风格）。中文措辞、文风见 `../../../quarto-docs/references/zh/writing-style.md`。

> 速查：示例必须可编译 · 文件名纯 ASCII · 术语中英对照统一 · 排版 LLVM / 命名 Google（见 `./code-style.md`）

## 为什么重要

文档的目标不是「把代码贴出来」，而是让读者**按正确的心智模型复用知识**。C++ 的多数坑（悬垂、UB、迭代器失效）源于心智模型偏差；写法模仿 *C++ Primer* / *A Tour of C++* 的教学节奏——先给动机与规则，再给正/反例对照，最后点误区。

## 核心写作约定

### 1. 代码示例必须可编译

- 统一编译选项：`-std=c++20 -Wall -Wextra`（WSL2 默认；MSVC 对照 `/std:c++20 /W4`）。
- 给**完整、可复制即运行**的代码；片段务必显式标注「片段」。
- 「错误写法 vs 正确写法」用 `callout-warning` 标坏写法并解释原因（可引用 `./pitfalls-ub.md`）。
- 代码块标语言 `cpp`；公开 API 用 Doxygen 风格 `///` 注释。

### 2. 文件 / 目录命名规范

- **一律纯 ASCII 字符**命名项目、目录、文件；不用全角字符或特殊连字符。
- 连字符一律普通 `-`（U+002D），**不要**用 U+2011（non-breaking hyphen）、U+2212（减号）等。
- 反例：目录名 `cpp‑memo`（U+2011）会让 `quarto render` 报 `recoverEncode: invalid argument`，
  见 `../../../quarto-docs/references/quarto/pitfalls.md`。
  可用 `../../../quarto-docs/scripts/check_ascii_names.py` 校验。
- C++ 源码文件的命名（小写下划线）与目录组织（`code/<主题>/`）见 `./code-style.md`。

### 3. 代码风格：排版 LLVM / 命名 Google（唯一出处）

- **排版与格式化**：clang-format，LLVM 基础风格（2 空格缩进、80 列）。
- **命名**：Google 命名规则（类型/函数 `CamelCase`、变量/参数 `snake_case`、常量 `k` 前缀等），经 clang-tidy `readability-identifier-naming` 落地。
- **异常**：启用异常（Google 风格指南的禁异常立场**不采纳**，只取其命名）。
- 完整命名总表、clang-format/clang-tidy 配置与用法、异常策略见 `./code-style.md`（唯一出处），本文件不重复。

### 4. 术语中英对照（全文统一）

| 英文 | 中文 | 备注 |
|---|---|---|
| RAII | 资源获取即初始化 | Resource Acquisition Is Initialization |
| UB | 未定义行为 | Undefined Behavior；后果不可预测 |
| RVO / NRVO | 返回值优化 / 具名返回值优化 | 省略拷贝的编译器优化 |
| SFINAE | 替换失败并非错误 | 模板重载决议机制 |
| CTAD | 类模板参数推导 | C++17 |
| SSO | 短字符串优化 | small string optimization |
| ODR | 单定义规则 | One Definition Rule |

新特性首次出现标注引入版本（如「概念（`C++20 引入`）」，见 `../../../quarto-docs/references/zh/writing-style.md`）。

## 本目录内容（按需读取）

| 文件 | 主题 |
|---|---|
| `./cpp.md` | 本文件：写作约定 + 术语表 + 命名规范 |
| `./code-style.md` | 代码风格：排版 LLVM / 命名 Google / 异常策略 / clang-format·clang-tidy |
| `./modern-cpp.md` | 现代 C++ 核心（RAII / 智能指针 / 移动 / const） |
| `./stl.md` | STL 容器与算法选择 |
| `./templates.md` | 模板与泛型（concepts / 转发 / CTAD） |
| `./performance.md` | 性能优化要点 |
| `./pitfalls-ub.md` | 陷阱与未定义行为 |
| `./toolchain.md` | 构建与工具链（编译器 / CMake） |
| `./engineering.md` | 工程实践与大型项目工作流 |

## 常见误区

- 把 `description:` 当成普通章节的可见引言（实际仅 `index.qmd` 封面可见）。
- 章节里再写顶层 `# H1`（会与 `title:` 重复渲染、章节编号错乱）。
- 把技术术语硬翻成中文导致检索困难——保留英文术语 + 中文释义。

## 后续语言扩展

新增语言时：在 `references/` 下新建与 `cpp/` 平级的 `<语言>/`（如 `python/`），内含该语言写作约定入口与要点文件；并在本 skill 的 `SKILL.md` 路由表加一行。
