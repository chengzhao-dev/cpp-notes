cmake_minimum_required(VERSION 3.31)
project(first-program LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 将可执行文件输出到 build/bin；运行时先进入该目录。
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(app main.cpp)
target_compile_options(app PRIVATE -Wall -Wextra -Werror)

# 开发期兜底（可选）：内存与 UB 检测，切勿编入发布产物
# target_compile_options(app PRIVATE -fsanitize=address,undefined -g)
# target_link_options(app PRIVATE -fsanitize=address,undefined)
