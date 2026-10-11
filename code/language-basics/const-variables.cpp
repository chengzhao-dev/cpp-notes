// 常量示例：展示 const 变量的初始化和读取。
#include <iostream>

int main() {
  const int kMaxCount{5};
  const int kTimeoutMs{3000};

  std::cout << "最大数量: " << kMaxCount << "\n";
  std::cout << "超时毫秒数: " << kTimeoutMs << "\n";
  return 0;
}
