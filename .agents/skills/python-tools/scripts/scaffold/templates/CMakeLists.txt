# 低于此版本时配置阶段直接报错，不做兼容回退。
cmake_minimum_required(VERSION 3.31)
project({{PROJECT_NAME}} LANGUAGES CXX)

# 对应 g++ 的 -std=c++20。省略会回到编译器默认标准。
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 对应直接编译命令的 -o build/bin/app，统一输出路径。
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 导出编译数据库，供 clangd 读取与实际构建一致的编译参数。
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(app main.cpp)
# -Wall -Wextra 打开常用警告，-Werror 将警告升级为错误。
# 编译器没有输出表示编译和链接成功。出现 warning/error 时按文件名、行号和原因修复。
target_compile_options(app PRIVATE -Wall -Wextra -Werror)
