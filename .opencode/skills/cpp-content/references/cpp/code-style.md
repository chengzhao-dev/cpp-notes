# C++ 代码风格（排版 LLVM / 命名 Google）

> 速查：排版 clang-format（LLVM，2 空格、80 列） · 命名 Google（类型/函数大驼峰、变量小写下划线） · 异常启用 · 检查 clang-tidy（modernize + Core Guidelines 子集） · 本文件是风格唯一出处

## 为什么重要

代码风格的价值不在「好看」，而在**降低读者的认知负担**：统一的排版让读者把注意力放在语义上，统一的命名让标识符自解释（类型像类型、变量像变量），静态检查把「过时写法」「可疑模式」挡在编码期。本仓库取三方之长——**LLVM 的排版工具、Google 的命名规则、C++ Core Guidelines 的规则层**，并明确启用异常。

## 三方分工（立场声明）

| 来源 | 取什么 | 不取什么 |
|---|---|---|
| LLVM | 排版基线（`.clang-format` `BasedOnStyle: LLVM`：2 空格缩进、80 列） | LLVM 项目自身的 `-fno-exceptions` 编译立场 |
| Google | 命名规则（下表，经 clang-tidy `readability-identifier-naming` 落地） | Google 风格指南的**禁异常**立场——本仓库**异常保持启用** |
| C++ Core Guidelines | 规则层（clang-tidy `cppcoreguidelines-*` 检查集；资源、错误处理、const 等） | 无 |

## 命名总表（唯一出处）

| 实体 | 规则 | 示例 |
|---|---|---|
| 类型（类 / 结构体 / 枚举 / 类型别名） | 大驼峰（PascalCase） | `UrlTable`、`HttpRequest` |
| 概念（`C++20 引入`）/ 模板参数 | 大驼峰 | `Integral`、`T` |
| 函数 | 大驼峰，动词开头 | `AddTableEntry()`、`MakeBig()` |
| 变量 / 函数参数 | 小写下划线（snake_case） | `table_name`、`entry_count` |
| 类私有数据成员 | snake_case + 尾缀 `_` | `width_` |
| 结构体 / 类公开数据成员 | snake_case，无尾缀 | `row_count` |
| 常量 / `constexpr` / 枚举值 | `k` 前缀 + 大驼峰 | `kMaxRetries`、`kDaysInWeek` |
| 宏 | 全大写下划线（尽量少用） | `MAX_LEN` |
| 命名空间 | 小写下划线 | `cpp_memo` |
| C++ 源码文件 | 小写下划线 | `url_table.cpp` |

## 排版与格式化（clang-format）

- 仓库根 `.clang-format`：`BasedOnStyle: LLVM` + `Standard: Latest` + `ColumnLimit: 80` + `IndentWidth: 2`。
- **80 列**同时适配 860px 正文栏的代码块（不折行）与 LLVM 工具链习惯。
- 提交/落章前先过格式化检查（见下「工具用法」），不要手工对齐空格。

## 静态检查（clang-tidy）

- 仓库根 `.clang-tidy`：
  - `modernize-*`：把旧写法升级为当前标准写法（新语法主力）；
  - `cppcoreguidelines-*` + `bugprone-*` + `performance-*` + `portability-*` + `readability-*`：Core Guidelines 规则与常见缺陷兜底；
  - 已豁免的高噪声项：`-bugprone-easily-swappable-parameters`、`-modernize-use-trailing-return-type`（Google 用前置返回类型）、`-readability-identifier-length`、`-readability-magic-numbers` 等；
  - **未启用任何禁异常的检查集**（如 `fuchsia-*`）。
- clang-tidy 输出是**建议**（warnings）；
  clang-format 的 `--dry-run -Werror` 才是硬门槛（见 `verify_examples.py` 的 `--style`）。

## 异常策略（启用异常）

- **默认启用异常**：不写 `-fno-exceptions`（Google/LLVM 项目源码的禁异常立场均不采纳）。
- 错误处理分工（与 `./engineering.md` 一致）：
  - 构造函数无法建立不变量 → 抛异常（资源已由 RAII 持有，不泄漏）；
  - 可恢复、预期中的失败（查找未命中、解析失败）→ `std::optional` / `std::expected`（`C++23 引入`）；
  - 违反不变量 / 程序员错误 → `assert` / 直接终止，不用异常当流程控制。
- **不在析构函数、`noexcept` 函数中抛异常**；移动构造标 `noexcept`（见 `./modern-cpp.md`）。
- 异常安全靠 RAII：栈展开自动释放资源，禁止异常路径手写 `delete`。

## 版本基线

- 语言标准：**C++20**（`-std=c++20`；MSVC 对照 `/std:c++20`）。
- 新特性照常使用（concepts、`if constexpr`、`string_view`、结构化绑定等），首次出现标注引入版本（见 `./cpp.md` 术语表）。
- clang-tidy 的 `modernize-*` 会主动提示可升级的旧写法（如 `NULL` → `nullptr`、typedef → using）。

## 工具用法（WSL2）

安装（Ubuntu 22.04 起包名直接可用；版本建议 clang-15+，concepts 相关检查更完整）：

```bash
sudo apt install clang-format clang-tidy
```

检查与修复（在仓库根执行）：

```bash
$ clang-format --version
Ubuntu clang-format version 18.1.3
$ clang-format --dry-run -Werror code/hello/hello.cpp
$ clang-format -i code/hello/hello.cpp
$ clang-tidy code/hello/hello.cpp -- -std=c++20
```

一键校验（编译 + 格式化 + 静态检查）：

```powershell
python .opencode/skills/cpp-content/scripts/verify_examples.py --style
```

工具未安装时 `--style` 降级为警告并跳过，编译仍是硬门槛。

## 书籍示例适配

- **缩进 2 空格、行宽 ≤ 80**：与 `.clang-format` 一致，正文代码块不折行。
- **注释用中文**，与正文标点约定一致；标识符一律 ASCII。
- 完整示例带 `int main`（可被 `verify_examples.py` 自动编译）；片段首行标注「`// 片段`」。
- 示例文件放 `code/<主题>/<小写下划线>.cpp`，`<主题>` 目录与 `content/` 章节主题同名（如 `content/environment/` ↔ `code/environment/`）。
- 单个完整示例尽量 ≤ 40 行；需要长示例时拆成多块渐进展示。

## 常见误区

- 把「Google 风格」当成整套采用——本仓库只取其**命名**，异常立场明确不采纳。
- 手工排版后忘记跑 clang-format——以 `--dry-run -Werror` 的结果为准，不要肉眼对齐。
- 给常量写 `const int MAX_RETRIES`——常量应 `kMaxRetries`；全大写只留给宏。
- 类成员忽加忽减尾缀 `_`——只有类私有成员带 `_`，结构体与公开成员不带。
- clang-tidy 报警告就改 `WarningsAsErrors` 一刀切——先判断是规则问题（进 `.clang-tidy` 豁免清单并写明理由）还是代码问题。

## 延伸阅读

- LLVM Coding Standards（排版基线来源）
- Google C++ Style Guide（命名规则来源；其异常立场见其 Design 区说明，本仓库不采纳）
- C++ Core Guidelines：[NL](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-naming)（命名与布局）
- C++ Core Guidelines：[E](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-errors)（错误处理）
- 本备忘录：`./cpp.md`（写作约定入口）、`./toolchain.md`（编译选项与 sanitizer）、`./engineering.md`（错误处理与所有权）
