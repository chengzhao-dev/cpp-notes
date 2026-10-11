// 命名空间示例：同名常量放在不同命名空间并分别输出。
#include <iostream>

namespace board {
constexpr int kSize{3};
}

namespace config {
constexpr int kSize{16};
}

int main() {
  std::cout << "棋盘尺寸: " << board::kSize << "\n";
  std::cout << "配置尺寸: " << config::kSize << "\n";
  return 0;
}
