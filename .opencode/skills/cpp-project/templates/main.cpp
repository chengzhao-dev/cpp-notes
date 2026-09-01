#include <iostream>

// 最小可运行入口：验证工具链可编译、可运行。
int main() {
  const int kAnswer = 42;  // 常量：k 前缀 + 大驼峰（Google 命名）
  std::cout << "answer: " << kAnswer << "\n";
  return 0;
}
