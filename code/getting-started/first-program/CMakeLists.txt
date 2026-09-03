# 要求的最低 CMake 版本；低于 3.31 直接报错，保证所有人行为一致
cmake_minimum_required(VERSION 3.31)

# 项目名 app，语言用 C++
project(app LANGUAGES CXX)

# 默认按 C++20 标准构建
set(CMAKE_CXX_STANDARD 20)
# 强制必须支持 C++20，编译器不支持就报错（而不是悄悄降级）
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 固定把可执行文件输出到 build/bin/（和一键脚本约定一致，方便直接用）
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 用 first-program.cpp 生成名为 app 的可执行文件
add_executable(app first-program.cpp)
