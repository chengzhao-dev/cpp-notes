#!/usr/bin/env bash
# 一键配置、构建并运行当前 CMake 示例。
# 用法：在项目目录中运行 bash build-and-run.sh。
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

# 配置：生成 Ninja 构建文件，同时导出 compile_commands.json 给 clangd。
printf '\n==> 配置\n\n'
cmake -G Ninja -B "$build_dir" -DCMAKE_BUILD_TYPE=Debug

# 构建：调用 Ninja 编译并链接 CMakeLists.txt 中声明的目标。
printf '\n==> 构建\n\n'
cmake --build "$build_dir"

# 运行：可执行文件统一放在 build/bin，和中间产物分开。
printf '\n==> 运行\n\n'
"$build_dir/bin/$target"
