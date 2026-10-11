// 编译期常量示例：constexpr 变量与极简 constexpr 函数。
#include <iostream>

constexpr bool IsInRange(int value, int low, int high) {
  return value >= low && value <= high;
}

int main() {
  constexpr int kThreshold{5000};
  constexpr double kRatio{0.90};

  std::cout << "阈值: " << kThreshold << "\n";
  std::cout << "比例: " << kRatio << "\n";
  std::cout << std::boolalpha
            << "4200 在区间内: " << IsInRange(4200, 0, kThreshold) << "\n";
  return 0;
}
