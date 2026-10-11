// 分支与循环示例：switch 选择一支，for 打印一行。
#include <iostream>

int main() {
  int code{1};
  switch (code) {
    case 0:
      std::cout << "空\n";
      break;
    case 1:
      std::cout << "一\n";
      break;
    case 2:
      std::cout << "二\n";
      break;
    default:
      std::cout << "其他\n";
      break;
  }
  for (int column = 0; column < 3; ++column) {
    std::cout << column;
    if (column < 2) {
      std::cout << ' ';
    }
  }
  std::cout << '\n';
  return 0;
}
