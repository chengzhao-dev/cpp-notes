// 常量示例：展示命名常量、初始化要求和不可修改限制。
#include <iostream>

int main() {
  const int kMaxRetries = 3;
  constexpr double kPi = 3.14159;

  std::cout << "最大重试次数: " << kMaxRetries << "\n";
  std::cout << "圆周率近似值: " << kPi << "\n";
  return 0;
}
