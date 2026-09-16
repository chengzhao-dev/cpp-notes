#!/usr/bin/env bash
# 编译并运行当前单文件程序。

# 任一命令失败时立即停止。
set -euo pipefail

cd "$(dirname "$0")"

mkdir -p build

printf '\n==> 编译\n\n'
clang++ -std=c++20 -stdlib=libc++ -Wall -Wextra -Werror first-program.cpp -o build/first-program

printf '\n==> 运行\n\n'
./build/first-program
