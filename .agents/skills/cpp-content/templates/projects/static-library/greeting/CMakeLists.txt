# 构建 greeting 静态库。

# 收集库源文件，新增 .cpp 后 CMake 会自动重新配置。
file(GLOB LIBRARY_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp")

# 构建静态库，并把 include/ 作为它的公开接口目录。
add_library(greeting STATIC ${LIBRARY_SOURCES})
target_include_directories(greeting PUBLIC include)
target_compile_options(greeting PRIVATE -stdlib=libc++ -Wall -Wextra -Werror)
