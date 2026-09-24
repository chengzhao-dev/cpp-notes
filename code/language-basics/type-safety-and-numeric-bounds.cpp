// 数值安全示例：展示类型边界、明确宽度、浮点容差和 bool 输出。
#include <cmath>
#include <cstdint>
#include <iostream>
#include <limits>

int main() {
  std::cout << "int 字节数: " << sizeof(int) << "\n";
  std::cout << "int 最大值: " << std::numeric_limits<int>::max() << "\n";

  std::int32_t value{1000};
  unsigned int wrapped{std::numeric_limits<unsigned int>::max()};
  ++wrapped;

  double a{0.1 + 0.2};
  bool closeEnough{std::abs(a - 0.3) < 1e-9};
  bool enabled{static_cast<bool>(2)};

  std::cout << "明确宽度的值: " << value << "\n";
  std::cout << "无符号回绕后: " << wrapped << "\n";
  std::cout << std::boolalpha << "浮点值足够接近: " << closeEnough << "\n";
  std::cout << "是否启用: " << enabled << "\n";
  return 0;
}
