# 工具链章节的写作约定

> 速查：本章只规定「怎么写」；「为什么这样配」的唯一出处是知识库
> `knowledge/domains/tooling/01_build_toolchain/cpp-build-toolchain.md`，取用方式见文末。

## 硬约束

- 编译口径：示例统一 `-std=c++20 -Wall -Wextra`，入门示例追加 `-Werror`；MSVC 对应 `/std:c++20` 与 `/W4`。
- 默认环境是 Windows 上的 WSL2（GCC/Clang/CMake），MSVC 仅作对照，不假设读者有 MSVC。
- 先最小成功路径：确认编译器存在 → 编译并运行一个程序 → 再引入 CMake 与其他工具。每组命令前说明目的，之后说明成功判据。
- 安装与验证分开写：安装只说明动作，是否可用由版本查询单独确认；不逐项铺陈 `--version` 预检。
- 只读验证命令先经 `wsl bash -lc` 实测，再把命令与关键输出写入代码块；不虚构版本号、路径或成功结果。WSL 不可用时如实报告限制。
- `apt install` 等改变系统状态的命令只展示操作与后续验证，不在写作过程中重复执行。
- 源码、构建目标与运行输出必须同步核对，不能让示例代码与文档结果不一致。
- `cmake` 围栏只放配置文件内容；执行 CMake 的命令属于 shell，不放 `cmake` 块。
- 每个代码块标注语言，逻辑段之间留一个空行；相邻代码块之间必须空一行。

## 命令块格式

Linux/WSL 命令使用 `bash` 围栏，用户输入行以 `$ ` 开头，Shell 注释用 `#`；命令与输出放同一个代码块，输出前用注释标出「预期输出」或「实测输出」，不再另开紧邻的输出块。PowerShell 使用 `powershell` 围栏且不加提示符。完整口径由 `quarto-docs` skill 承载：按环境选围栏语言见 `.cursor/skills/quarto-docs/references/quarto/authoring.md`，实测输出见 `.cursor/skills/quarto-docs/references/quarto/terminal-validation.md`，本文件不重复。

示例骨架：

```cmake
add_executable(main main.cpp)
target_compile_options(main PRIVATE -Wall -Wextra -Werror)
```

```bash
# 配置：生成 Ninja 构建文件，指定 Debug 构建
$ cmake -G Ninja -B build -DCMAKE_BUILD_TYPE=Debug

# 构建并运行
$ cmake --build build
$ ./build/bin/main
```

## 校验入口

修改示例后运行 `python .cursor/tools/run.py verify`；只验证一章运行 `python .cursor/tools/run.py build <part>/<chapter>`。两个入口默认压缩成功输出，排查失败才用 `--verbose`。

## 取用领域结论

需要「为什么用 ASan+UBSan、为什么 `-Werror`、为什么不能长期只教裸命令行」这类依据时，检索知识库而不是在本文件里找：

```powershell
python .cursor/tools/run.py kb-search "sanitizer 选择"
python .cursor/tools/run.py kb-search --domain tooling --toc "工具链"
```

参考分工：`./code-style.md`（clang-format 与命名规则唯一出处）、`./engineering.md`（工程流程与审查）、`./pitfalls-ub.md`（UB 检测）、`./cmake-teaching.md`（CMake 教学顺序）。
