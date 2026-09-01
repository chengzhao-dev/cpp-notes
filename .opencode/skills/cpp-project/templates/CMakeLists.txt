cmake_minimum_required(VERSION 3.16)
project({{PROJECT_NAME}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable({{PROJECT_NAME}} main.cpp)
target_compile_options({{PROJECT_NAME}} PRIVATE -Wall -Wextra -Werror)

# 开发期兜底（可选）：内存与 UB 检测，切勿编入发布产物
# target_compile_options({{PROJECT_NAME}} PRIVATE -fsanitize=address,undefined -g)
# target_link_options({{PROJECT_NAME}} PRIVATE -fsanitize=address,undefined)
