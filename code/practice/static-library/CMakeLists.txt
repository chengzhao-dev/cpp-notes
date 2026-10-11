# 构建 StaticLibrary 工程：根 main.cpp 使用 greeting/ 提供的静态库。
cmake_minimum_required(VERSION 3.31)
project(StaticLibrary LANGUAGES CXX)

# 使用 C++20 作为语言标准。
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# 可执行文件输出到 build/bin。
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
# 静态库输出到 build/lib。
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# 生成编译数据库，记录每个源文件的实际编译参数。
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 加载 greeting/CMakeLists.txt 中的静态库目标。
add_subdirectory(greeting)

# 创建 app 可执行目标。
add_executable(app main.cpp)

# 链接 greeting 静态库。
target_link_libraries(app PRIVATE greeting)

# 编译时启用 libc++ 与常用警告。
target_compile_options(app PRIVATE -stdlib=libc++ -Wall -Wextra -Werror)
# 链接时也使用 libc++。
target_link_options(app PRIVATE -stdlib=libc++)
