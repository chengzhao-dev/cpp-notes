#!/usr/bin/env bash
# 配置、构建并运行当前 CMake 项目。

# 任一命令失败时立即停止。
set -euo pipefail

cd "$(dirname "$0")"
readonly STAGE_BIN="${PWD}/build/bin"
readonly APP_NAME="app"

# 打印步骤标题，空行用于分隔连续步骤。
header() {
  printf '\n==> %s\n' "$*"
}

# 将错误提示写到 stderr，避免混入正常输出。
err() {
  printf '错误: %s\n' "$*" >&2
}

# 失败时补充定位提示，并保留原命令的非零退出码。
trap 'err "构建流程失败，定位最靠近上方的失败命令后重试"' ERR

# main：1 配置 → 2 构建 → 3 运行。
main() {
  header "1. 配置"
  cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++

  header "2. 构建"
  cmake --build build

  header "3. 运行"
  # 子 shell 进入产物目录执行，父脚本工作目录不变。
  (
    cd "${STAGE_BIN}"
    "./${APP_NAME}"
  )
}

main "$@"
