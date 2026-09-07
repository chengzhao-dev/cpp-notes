# 要求支持当前项目语法的最低 CMake 版本。
cmake_minimum_required(VERSION 3.31)

# 声明项目名称，并启用 C++ 语言支持。
project(first-program LANGUAGES CXX)

# 使用 C++20，并要求构建工具遵守该标准。
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 将可执行文件集中输出到 build/bin，便于查找运行结果。
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 导出编译数据库，让 clangd 读到与实际构建一致的编译参数。
# 开启后配置阶段会生成 build/compile_commands.json。
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 从 main.cpp 构建名为 app 的可执行文件。
add_executable(app main.cpp)

# 启用常用警告，并把警告当作错误处理。
target_compile_options(app PRIVATE -Wall -Wextra -Werror)