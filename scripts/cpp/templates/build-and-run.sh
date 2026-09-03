#!/usr/bin/env bash
# 一键构建并运行 CMake 示例（Ubuntu / WSL2）
#
# 固定约定（后续章节统一沿用）：
#   - 构建目录       build/
#   - 可执行文件位置 build/bin/
#   - 可执行文件名   app（须与 CMakeLists.txt 的 add_executable(app ...) 一致）
set -euo pipefail
# e：任一条命令返回非 0 立即退出；u：用到未定义变量立即报错；o pipefail：管道中任一步失败都算失败

# 无论在哪里执行，都先切到脚本所在目录（即示例目录），保证相对路径稳定
cd "$(dirname "$0")"

# —— 以下两项须与 CMakeLists.txt 保持一致 ——
BUILD_DIR="build"
BIN_DIR="$BUILD_DIR/bin"   # 可执行文件输出位置
TARGET="app"               # 生成的可执行文件名

# -DCMAKE_EXPORT_COMPILE_COMMANDS=ON 会生成 build/compile_commands.json，
# 它是 clangd 的编译数据库：clangd 从源文件向上查找并自动进入 build/ 子目录读取，
# 有了它，补全与跳转才能拿到真实的头文件路径和编译参数（比 .clangd 的兜底参数准确）。
echo "==> 第 1 步：配置（生成构建系统到 $BUILD_DIR/）"
cmake -S . -B "$BUILD_DIR" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

echo "==> 第 2 步：构建（编译出 $BIN_DIR/$TARGET）"
cmake --build "$BUILD_DIR"

# 用分隔线把「构建」与「运行」的输出隔开，方便阅读
echo
echo "=================================================="
echo " 运行 $BIN_DIR/$TARGET"
echo "=================================================="
echo
"./$BIN_DIR/$TARGET"
