# 构建 CMakeProject 可执行目标。
cmake_minimum_required(VERSION 3.31)
project(CMakeProject LANGUAGES CXX)

# 使用 C++20 作为语言标准。
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# 可执行文件统一输出到 build/bin。
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 生成编译数据库，记录每个源文件的实际编译参数。
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 创建 app 可执行目标。
add_executable(app main.cpp)

# 编译时启用 libc++ 与常用警告。
target_compile_options(app PRIVATE -stdlib=libc++ -Wall -Wextra -Werror)
# 链接时也使用 libc++。
target_link_options(app PRIVATE -stdlib=libc++)
