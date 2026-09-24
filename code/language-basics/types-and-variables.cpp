// 类型示例：展示基础类型、变量、全局作用域和块作用域。
#include <iostream>

int defaultLimit{1};

int main() {
  int count{12};
  double ratio{0.85};
  bool enabled{true};
  char grade{'A'};

  count -= 3;
  {
    int increment{3};
    count += increment;
    std::cout << "局部增量: " << increment << "\n";
  }

  std::cout << "默认上限: " << defaultLimit << "\n";
  std::cout << "数量: " << count << "\n";
  std::cout << "比例: " << ratio << "\n";
  std::cout << std::boolalpha << "已启用: " << enabled << "\n";
  std::cout << "等级: " << grade << "\n";
  return 0;
}
