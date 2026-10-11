# 构建 greeting 动态库。

# 声明 greeting 共享库目标：由 src/greeting.cpp 编译生成。
add_library(greeting SHARED src/greeting.cpp)

# include/ 加入头文件搜索路径，供使用方 include。
target_include_directories(greeting PUBLIC include)

# 编译时启用 libc++ 与常用警告。
target_compile_options(greeting PRIVATE -stdlib=libc++ -Wall -Wextra -Werror)
# 链接时也使用 libc++。
target_link_options(greeting PRIVATE -stdlib=libc++)
