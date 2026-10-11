# 构建 greeting 静态库。

# 声明 greeting 静态库目标：由 src/greeting.cpp 编译生成。
add_library(greeting STATIC src/greeting.cpp)

# include/ 加入头文件搜索路径，供使用方 include。
target_include_directories(greeting PUBLIC include)

# 编译时启用 libc++ 与常用警告。
target_compile_options(greeting PRIVATE -stdlib=libc++ -Wall -Wextra -Werror)
