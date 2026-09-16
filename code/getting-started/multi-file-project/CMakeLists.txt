# 构建 MultiFileProject 可执行目标。
cmake_minimum_required(VERSION 3.31)
project(MultiFileProject LANGUAGES CXX)

# 使用 C++20，并把可执行文件统一输出到 build/bin。
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 生成编译数据库，记录每个源文件的实际编译参数。
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 收集程序源文件，新增 .cpp 后 CMake 会自动重新配置。
file(GLOB APP_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

# 创建 app 可执行目标。
add_executable(app ${APP_SOURCES})

# 让 app 找到 include/ 中的头文件。
target_include_directories(app PRIVATE include)

# 使用 libc++，并启用常用警告。
target_compile_options(app PRIVATE -stdlib=libc++ -Wall -Wextra -Werror)
target_link_options(app PRIVATE -stdlib=libc++)
