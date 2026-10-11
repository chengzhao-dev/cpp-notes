// overview 示例：点名几个常用标准库类型，不展开 API。
#include <array>
#include <iostream>
#include <string>
#include <vector>

int main() {
  std::array<int, 2> fixed{1, 2};
  std::vector<int> dynamic{3, 4};
  std::string label = "stl";

  std::cout << "array size=" << fixed.size() << '\n';
  std::cout << "vector size=" << dynamic.size() << '\n';
  std::cout << "string=" << label << '\n';
  return 0;
}
