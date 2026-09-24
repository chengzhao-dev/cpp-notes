// 初始化示例：展示列表初始化、赋值、auto 和初始化列表推导。
#include <iostream>

int main() {
  int count{};
  int limit{100};
  count = 80;

  auto value = 1200;
  auto ratio = 4.5;
  auto enabled = true;
  auto values = {10, 20, 30};

  value -= 100;
  std::cout << "数量: " << count << "/" << limit << "\n";
  std::cout << "值: " << value << "\n";
  std::cout << "比例: " << ratio << "\n";
  std::cout << std::boolalpha << "已启用: " << enabled << "\n";
  std::cout << "值的数量: " << values.size() << "\n";
  return 0;
}
