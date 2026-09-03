// 引入 iostream：标准库提供的输入/输出（I/O）功能都在这里
#include <iostream>

// 每个 C++ 程序都必须有 main 函数，它是操作系统启动程序时调用的入口
int main()
{
    // std::cout 代表「标准输出」（通常是屏幕）
    // << 是输出运算符，把右侧内容写入左侧的输出流
    // std::endl 先输出一个换行，再刷新缓冲区，确保立刻显示
    std::cout << "Hello, World!" << std::endl;

    // main 返回 0 表示程序正常结束
    return 0;
}
