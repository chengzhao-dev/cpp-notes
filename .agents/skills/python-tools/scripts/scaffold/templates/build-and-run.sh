#!/usr/bin/env bash
# 一键配置、构建并运行当前 CMake 示例。
# 在项目目录中运行 bash build-and-run.sh
#
# 脚本依次完成配置、构建和运行。
# CMakeLists.txt 统一 C++ 标准、警告策略和可执行文件输出目录。

set -euo pipefail

# 无论从哪里调用，都先切换到脚本所在的项目目录。
project_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$project_dir"

build_dir="build"
target="app"

# 配置 Ninja Debug 构建
printf '\n==> 配置\n\n'
cmake -S . -B "$build_dir" -G Ninja -DCMAKE_BUILD_TYPE=Debug

# 构建 CMakeLists.txt 声明的目标。
printf '\n==> 构建\n\n'
cmake --build "$build_dir"

# 运行构建结果
printf '\n==> 运行\n\n'
"$build_dir/bin/$target"
