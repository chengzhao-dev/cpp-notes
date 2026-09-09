#!/usr/bin/env bash
# 一键配置、构建并运行当前 CMake 示例。
# 用法：在项目目录中运行 bash build-and-run.sh。
#
# 本脚本包含 C++ 工程中最关键的三条指令：
#   1. g++ -std=c++20 -Wall -Wextra -Werror main.cpp -o build/bin/app
#      不经过构建工具，直接编译链接单个源文件；-std 选定语言标准，
#      -Wall -Wextra 打开常用警告，-Werror 把警告升级为错误，-o 指定输出路径。
#   2. cmake -G Ninja -B build -DCMAKE_BUILD_TYPE=Debug
#      配置阶段：-G 选定底层构建工具 Ninja，-B 指定生成物目录，
#      -D 写入缓存变量；Debug 给构建加上 -g 且不启用优化，便于 gdb 查看变量。
#   3. cmake --build build
#      构建阶段：调用 Ninja 按依赖关系编译并链接目标，只重建受影响的部分。

set -euo pipefail

# 无论从哪里调用，都先切换到脚本所在的项目目录。
project_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$project_dir"

build_dir="build"
target="app"

# 配置：生成 Ninja 构建文件，同时导出 compile_commands.json 给 clangd。
printf '\n==> 配置\n\n'
cmake -G Ninja -B "$build_dir" -DCMAKE_BUILD_TYPE=Debug

# 构建：调用 Ninja 编译并链接 CMakeLists.txt 声明的目标。
printf '\n==> 构建\n\n'
cmake --build "$build_dir"

# 运行：可执行文件统一放在 build/bin，和中间产物分开。
printf '\n==> 运行\n\n'
"$build_dir/bin/$target"