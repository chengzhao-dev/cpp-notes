cmake_minimum_required(VERSION 3.16)
project({{PROJECT_NAME}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 核心库：头文件在 include/，实现放 src/，减少编译依赖
add_library({{PROJECT_NAME}}_core src/{{PROJECT_NAME}}.cpp)
target_include_directories({{PROJECT_NAME}}_core PUBLIC include)
target_compile_options({{PROJECT_NAME}}_core PRIVATE -Wall -Wextra -Werror)

add_executable({{PROJECT_NAME}} src/main.cpp)
target_link_libraries({{PROJECT_NAME}} PRIVATE {{PROJECT_NAME}}_core)
target_compile_options({{PROJECT_NAME}} PRIVATE -Wall -Wextra -Werror)

enable_testing()
add_subdirectory(tests)
