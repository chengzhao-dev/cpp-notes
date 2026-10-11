#!/usr/bin/env bash
# 编译并运行最小程序结构示例。

# 任一命令失败时立即停止。
set -euo pipefail

cd "$(dirname "$0")"

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

# main：1 编译 → 2 运行。
main() {
  header "1. 编译"
  mkdir -p build
  clang++ -std=c++20 -stdlib=libc++ -Wall -Wextra -Werror \
    main.cpp greeting.cpp -o build/minimal-program-structure

  header "2. 运行"
  ./build/minimal-program-structure
}

main "$@"
