#!/usr/bin/env bash
# 一键配置、构建并运行当前 CMake 示例。
# 在项目目录中运行 bash build-and-run.sh
#
# 脚本依次完成配置、构建和运行。
# CMakeLists.txt 统一 C++ 标准、警告策略和可执行文件输出目录。

# 命令失败、使用未定义变量或管道出错时停止脚本。
set -euo pipefail

# 无论从哪里调用，都先切换到脚本所在的项目目录。
project_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$project_dir"

# 构建目录与目标名与 CMakeLists.txt 保持一致。
build_dir="build"
target="app"

# 配置 clang++ 与 Ninja Debug 构建
printf '\n==> 配置\n\n'
cmake -S . -B "$build_dir" -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++

# 构建 CMakeLists.txt 中声明的目标。
printf '\n==> 构建\n\n'
cmake --build "$build_dir"

# 运行构建结果
printf '\n==> 运行\n\n'
"$build_dir/bin/$target"
