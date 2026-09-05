#!/usr/bin/env bash
# 一键配置、构建并运行当前 CMake 示例。
# 用法：在项目根目录运行 bash build-and-run.sh。
# 配置阶段会生成 compile_commands.json，供 clangd 还原真实编译参数。
set -euo pipefail

# 无论从哪里调用，都先切换到脚本所在的项目目录。
cd "$(dirname "$0")"

# 将生成物集中到 build/，避免污染源码目录。
BUILD_DIR="build"
BIN_DIR="$BUILD_DIR/bin"
TARGET="app"

# 导出编译数据库，让 clangd 的诊断与实际构建保持一致。
printf '\n==> 配置\n\n'
cmake -S . -B "$BUILD_DIR" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# 构建 CMakeLists.txt 声明的目标。
printf '\n==> 构建\n\n'
cmake --build "$BUILD_DIR"

# 可执行文件统一放在 build/bin，和中间文件分开。
printf '\n==> 运行\n\n'
cd "$BIN_DIR"
"./$TARGET"
