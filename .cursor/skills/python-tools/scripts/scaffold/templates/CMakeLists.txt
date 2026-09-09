cmake_minimum_required(VERSION 3.31)
project({{PROJECT_NAME}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 可执行文件输出到 build/bin；运行前先确认该目录。
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 导出编译数据库，供 clangd 读取与实际构建一致的编译参数。
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(app main.cpp)
target_compile_options(app PRIVATE -Wall -Wextra -Werror)