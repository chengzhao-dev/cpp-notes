# 构建 LanguageAdvanced 分册各章的可执行文件。
cmake_minimum_required(VERSION 3.31)
project(LanguageAdvanced LANGUAGES CXX)

# 使用 C++20，并把可执行文件统一输出到 build/bin。
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 生成编译数据库，记录每个源文件的实际编译参数。
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 收集分册根目录下各章源文件；新增一章源文件后不必修改本文件。
file(GLOB CHAPTER_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

foreach(source IN LISTS CHAPTER_SOURCES)
  get_filename_component(chapter "${source}" NAME_WE)
  # 每章一个同名可执行目标，例如 strong-types.cpp 生成 strong-types。
  add_executable(${chapter} "${source}")
  # 使用 libc++，并启用常用警告。
  target_compile_options(${chapter} PRIVATE -stdlib=libc++ -Wall -Wextra -Werror)
  target_link_options(${chapter} PRIVATE -stdlib=libc++)
endforeach()
