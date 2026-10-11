// subscript-and-at 示例：用 std::array 演示 [] 与 at。
#include <array>
#include <iostream>
#include <stdexcept>

int main() {
  std::array<int, 3> cells{10, 20, 30};

  // 合法下标：[] 与 at 读到同一格。
  std::cout << "cells[1]=" << cells[1] << '\n';
  std::cout << "cells.at(1)=" << cells.at(1) << '\n';

  try {
    // 非法下标：at 抛出 std::out_of_range。
    std::cout << cells.at(3) << '\n';
  } catch (const std::out_of_range& ex) {
    std::cout << "caught: " << ex.what() << '\n';
  }

  // 故意不演示越界 cells[3]：那是未定义行为，不是可依赖的报错。
  return 0;
}
