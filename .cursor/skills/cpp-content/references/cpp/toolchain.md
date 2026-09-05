# 构建与工具链

> 速查：默认 WSL2 + g++/clang++/CMake · `-std=c++20 -Wall -Wextra` · `-fsanitize=address,undefined` 查内存与 UB · CMake 设 `CXX_STANDARD 20` · 头文件自给自足 + `#pragma once`

## 为什么重要

C++ 是"编译到机器码"的语言，**工具链的选择与编译参数直接决定你能否在开发期抓住 bug**。很多未定义行为（UB）、内存泄漏、数据竞争在 `-O2` 下才暴露，或只在某编译器下报错。现代 C++ 工程默认把警告当错误（`-Werror`）、用 sanitizer 在测试阶段兜底——这比上线后崩溃便宜得多。本备忘录以 Windows 上的 WSL2（GCC/Clang/CMake）为默认环境，MSVC 仅作对照。Windows 校验由 `wsl.exe` 按需启动默认 Ubuntu，不需要手动保持 WSL 会话。

工具链章节先保证一条最小成功路径：确认编译器存在，编译并运行一个程序，再引入 CMake 及其他工具。每组命令前说明目的，命令后说明成功判据；高级选项放到后续小节。

如果正文要求读者在 Ubuntu 中运行只读验证命令，先通过 `wsl bash -lc` 实际执行，再把命令和关键输出放入代码块。只保留判断工具是否可用所需的行，不虚构版本号、路径或成功结果。`apt install` 等会改变系统状态的命令只展示操作和后续验证，不在写作过程中重复执行。WSL 不可用时明确报告限制，不伪造输出。

安装工具和验证工具分开写：安装命令只说明操作，验证使用版本命令确认工具已经安装并可调用。源码、构建目标和运行输出必须同步核对，不能让示例代码与文档结果不一致。

## 核心规则

展示工具链命令时，一两条简单命令直接写进正文；连续安装、配置或验证步骤才使用代码块。版本检查直接使用 `g++ --version`、`cmake --version` 等完整命令，不为新手引入未解释的 `| head -n 1`。代码块中的关键命令在上一行使用简短的 Shell 注释，命令与输出演示使用 `text` 代码块，避免提示符、括号和版本号被错误拆成不同颜色。

- **编译器**（默认 WSL2）：`g++`（GCC）、`clang++`（Clang）；对照 MSVC（`cl`）。跨编译器验证可揪出非标准写法。
- **标准与选项统一**（C++20）：`-std=c++20`；MSVC 用 `/std:c++20`（`/std:c++latest` 追新特性）。
- **警告即错误**：入门示例统一使用 `-Wall -Wextra -Werror`；需要更严格检查时再加入 `-Wpedantic`，MSVC 用 `/W4`。
- **Sanitizer**（C++11 起普遍可用）：`-fsanitize=address,undefined`（ASan + UBSan）在开发/测试期检测泄漏、越界、UB；MSVC 用 `/fsanitize=address`。
- **优化/调试分级**：调试 `-O0 -g`，发布 `-O2`（或 `-O3` 谨慎）；不要把 sanitizer 与高优化混用。
- **格式化与静态检查**：排版与命名交给 clang-format / clang-tidy
  （配置源在 `.config/cpp/.clang-format` / `.config/cpp/.clang-tidy`，LLVM 排版 + Google 命名，见 `./code-style.md`）；
  校验用 `clang-format --dry-run -Werror`，
  clang-tidy 启用 `modernize-*` 与 `cppcoreguidelines-*` 子集。
- **CMake 最小骨架**（C++20）：`cmake_minimum_required(VERSION 3.31)`、`set(CMAKE_CXX_STANDARD 20)` 且 `REQUIRED ON`。
- **头文件规范**：每个头文件自给自足（能独立编译）；用 include guard 或 `#pragma once`；只包含所需头文件，减少编译依赖。

::: {.callout-important}
## 关键概念
工具链的核心心智模型是**"把 bug 尽量挡在开发期"**：编译选项（警告当错误、`-std=c++20`）与 sanitizer（ASan/UBSan）是比"上线后崩溃"便宜得多的兜底网，且跨编译器/优化级别验证能揪出只在 `-O2` 或某编译器下暴露的 UB 与数据竞争。
:::

## 正例 ✓ vs 反例 ✗

✓ 标准 CMake 工程 + 警告当错误：

```cmake
cmake_minimum_required(VERSION 3.31)
project(cpp_memo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(main main.cpp)
target_compile_options(main PRIVATE -Wall -Wextra -Werror)
```

构建与运行（WSL2）：

```bash
cmake -S . -B build
cmake --build build
./build/main
```

修改示例后的推荐校验方式是运行 `python scripts/agent/run.py verify`；只验证一个章节时运行 `python scripts/agent/run.py build <part>/<chapter>`。这两个入口默认压缩成功输出，只有排查失败时才使用 `--verbose`。

✗ 无警告、无标准约束，UB/泄漏悄然溜过编译：

```cmake
cmake_minimum_required(VERSION 3.0)
project(cpp_memo)
add_executable(main main.cpp)   # 没设 C++ 标准、没开 -Wall
```

对应命令行（反模式）：`g++ main.cpp -o main` —— 没开警告、没开 sanitizer，越界访问与内存泄漏都"静默通过"。

对照说明：正例用 `CMAKE_CXX_STANDARD_REQUIRED ON` 把标准固定为 C++20，避免误用旧标准特性；`-Werror` 把"警告"升级为"必须修"。反例放任编译器默认（往往 C++14 且无警告），UB 与可疑写法在开发期完全不可见，代价是线上崩溃更难定位。

## 常见误区

- 只在 `-O0` 下测试，发布 `-O2` 才暴露 UB/数据竞争——应在 sanitizer 下覆盖测试。
- 认为"能编译通过就是对的"——没开 `-Wall` 会漏掉未初始化、签名不匹配等隐患。
- 在 MSVC 上用 `-std=c++20`（gcc/clang 风格），应改为 `/std:c++20`。
- 头文件互相包含却不加 include guard，导致重定义。
- 把 sanitizer 编进发布产物——sanitizer 有显著运行时开销，仅用于开发/测试。

## 小结
- 统一标准与警告：入门示例使用 `-std=c++20 -Wall -Wextra -Werror`；更严格的检查再加入 `-Wpedantic`，MSVC 对应 `/std:c++20` 与 `/W4`。
- 开发/测试期用 `-fsanitize=address,undefined`（ASan+UBSan）兜底内存与 UB，但切勿编入发布产物（显著运行时开销）。
- CMake 用 `CXX_STANDARD 20` + `REQUIRED ON` 固定标准；头文件需自给自足并加 include guard/`#pragma once`，减少重定义与编译依赖。
- 排版（clang-format：LLVM、2 空格、80 列）与命名（Google 规则）交给工具链兜底，不手工对齐；规则唯一出处见 `./code-style.md`。

## 延伸阅读

- C++ Core Guidelines：[P.1–P.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-philosophy)（工程哲学）、编译器/构建相关章节
- CMake 官方文档：[cmake-buildsystem(7)](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html)
- GCC/Clang Sanitizer 手册：`-fsanitize=address,undefined`
- 本备忘录：`./engineering.md`（工程流程与审查）、`./pitfalls-ub.md`（UB 检测）、`./cpp.md`（写作约定与编译选项）
## 终端命令与输出

一两条无需区分用途的短命令直接写入正文。连续命令或需要说明用途的命令使用代码块，并把简短的 Bash 或 PowerShell 注释放在对应命令上方。命令输出使用 `text` 代码块，不让 `$`、括号和版本号参与语言高亮。

代码块和 `text` 输出块都左对齐，并继承站点的 GitHub Light / GitHub Dark 代码字体、背景、边框和间距。代码块不使用 Markdown 粗体、斜体或长篇解释。
