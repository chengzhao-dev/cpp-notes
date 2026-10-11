# 构建 clang-tools 示例并生成编译数据库。
cmake_minimum_required(VERSION 3.31)
project(ClangTools LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 创建检查工具使用的最小可执行目标。
add_executable(clang-tools clang-tools.cpp)
target_compile_features(clang-tools PRIVATE cxx_std_20)
target_compile_options(clang-tools PRIVATE -Wall -Wextra -Werror)
