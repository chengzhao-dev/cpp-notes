# CMake 章节教学流程

CMake 章节先让目标运行，再逐步把命令行参数固化为目标属性。不要从完整工程模板或所有变量开始。

## 推荐顺序

```text
源码 → 可执行目标 → 最小 CMakeLists.txt
→ 配置 → 构建 → 运行 → 编译数据库
→ 多文件或库 → 测试与安装
```

每一步承接前一步的文件和生成结果。命令前说明它要完成什么，命令后说明成功时应看到什么。读者未使用的缓存和内部文件不放进目录树。

## 默认构建参数

示例工程与脚手架统一使用 `cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++` 配置，再用 `cmake --build build` 编译目标。`-G Ninja` 选择 Ninja 生成器，显式指定编译器可避免 CMake 选择其他 C++ 驱动，`CMakeLists.txt` 保持生成器无关。构建仍通过 `cmake --build` 进入，因而读者不必把项目命令改成后端专用命令。Debug 给构建加上 `-g` 且不启用优化，便于 lldb 打断点和查看变量。`CMAKE_EXPORT_COMPILE_COMMANDS` 保持开启，让 clangd 读到与实际构建一致的编译参数。发布构建在同一目录改用 `-DCMAKE_BUILD_TYPE=Release` 即可，入门章节不展开。

## 目标导向

使用 `add_executable`、`add_library`、`target_sources`、`target_include_directories` 和 `target_compile_features` 表达目标关系。优先设置 target 属性，不用全局变量掩盖依赖关系。

## 编译数据库

配置阶段生成 `compile_commands.json` 时，说明它记录每个源文件的真实编译参数，供 clangd、脚本和编辑器使用。它是构建结果，不是手写配置。删除后可通过重新配置生成。

## Clang/LLVM 工具链一致性

编译、语言服务和调试统一使用 Clang/LLVM 工具链。CMake 显式选择 `clang++`，目标同时用 `-stdlib=libc++` 配置编译与链接，`.clangd` 的兜底参数也选择 libc++。这样 clangd 读取的编译数据库与真实构建使用同一驱动和标准库，不依赖 GCC 专用参数过滤。

旧构建目录可能缓存过其他编译器。切换编译器或标准库时应在新的构建目录重新配置，不能只运行 `cmake --build`。项目不保留 GCC 编译器作为后备路径。

## 章节落点

先验证单目标，再引入多文件、库、测试和安装。每个新增概念都应有对应源码、构建命令、生成结果和验证步骤。
