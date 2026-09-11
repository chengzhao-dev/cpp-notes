#!/usr/bin/env bash
# 一键配置、构建并运行当前 CMake 示例。
# 用法：在项目目录中运行 bash build-and-run.sh。
#
# 脚本按顺序执行三步：
#   1. cmake -G Ninja -B build -DCMAKE_BUILD_TYPE=Debug
#      配置阶段：-G 选定底层构建工具 Ninja，-B 指定存放生成物的 build/ 目录，
#      -D 写入缓存变量，CMAKE_BUILD_TYPE=Debug 给构建加上 -g 且不启用优化，
#      便于 gdb 打断点和查看变量。
#   2. cmake --build build
#      构建阶段：进入 build/ 调用 Ninja 按依赖关系编译并链接目标。
#      它会跳过没有变化的目标，只重建受影响的部分。
#   3. build/bin/app
#      运行阶段：执行上一步构建出的可执行文件，输出结果。
#
# g++ 没有输出表示编译和链接成功；出现 warning/error 时，先按文件名、行号和原因修复。
# 第三步输出 Hello, World!，表示程序正常运行。-std=c++20 选择语言标准，
# -Wall -Wextra 打开常用警告，-Werror 将警告升级为错误；CMakeLists.txt 中的
# CMAKE_RUNTIME_OUTPUT_DIRECTORY 对应直接编译命令的 -o build/bin/app。

# 命令失败、使用未定义变量或管道出错时停止脚本。
set -euo pipefail

# 无论从哪里调用，都先切换到脚本所在的项目目录。
project_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$project_dir"

# 构建目录与目标名与 CMakeLists.txt 保持一致。
build_dir="build"
target="app"

# 配置：生成 Ninja 构建文件，同时导出 compile_commands.json 给 clangd。
printf '\n==> 配置\n\n'
cmake -G Ninja -B "$build_dir" -DCMAKE_BUILD_TYPE=Debug

# 构建：调用 Ninja 编译并链接 CMakeLists.txt 中声明的目标。
printf '\n==> 构建\n\n'
cmake --build "$build_dir"

# 运行：可执行文件统一放在 build/bin，和中间产物分开。
printf '\n==> 运行\n\n'
"$build_dir/bin/$target"
