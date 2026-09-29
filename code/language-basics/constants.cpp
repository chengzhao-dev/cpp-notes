// 常量示例：展示 const 与 constexpr 的初始化和读取。
#include <iostream>

int main() {
  const int kMaxCount{5};
  constexpr int kThreshold{5000};
  constexpr double kRatio{0.90};

  std::cout << "最大数量: " << kMaxCount << "\n";
  std::cout << "阈值: " << kThreshold << "\n";
  std::cout << "比例: " << kRatio << "\n";
  return 0;
}
