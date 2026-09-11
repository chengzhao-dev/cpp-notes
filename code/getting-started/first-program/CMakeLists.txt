# Ubuntu 26.04 的项目基线使用 CMake 3.31。
cmake_minimum_required(VERSION 3.31)

# 声明项目名称，并启用 C++ 语言支持。
project(first-program LANGUAGES CXX)

# 与 g++ 直编命令的 -std=c++20 保持一致；省略会回到编译器默认标准。
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 对应 g++ 的 -o build/bin/app，统一把可执行文件放进 build/bin。
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 导出编译数据库，让 clangd 读到与实际构建一致的编译参数。
# 开启后配置阶段会生成 build/compile_commands.json。
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 从 main.cpp 构建名为 app 的可执行文件。
add_executable(app main.cpp)

# -Wall -Wextra 打开常用警告，-Werror 把警告升级为错误。
# 编译器没有输出表示编译和链接成功；出现 warning/error 时，
# 先按文件名、行号和原因修复。编译通过不代表程序逻辑正确。
target_compile_options(app PRIVATE -Wall -Wextra -Werror)
