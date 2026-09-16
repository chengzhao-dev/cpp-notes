#!/usr/bin/env bash
# 编译并运行最小程序结构示例。

# 任一命令失败时立即停止。
set -euo pipefail

cd "$(dirname "$0")"

mkdir -p build

printf '\n==> 编译\n\n'
clang++ -std=c++20 -stdlib=libc++ -Wall -Wextra -Werror \
  main.cpp greeting.cpp -o build/minimal-program-structure

printf '\n==> 运行\n\n'
./build/minimal-program-structure
