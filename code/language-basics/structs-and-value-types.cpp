// 结构体与值类型示例：用 struct 聚合坐标成员并逐个输出。
#include <iostream>

struct Position {
  int x{0};
  int y{0};
};

int main() {
  Position start{1, 2};
  Position finish{2, 2};
  std::cout << "起点: " << start.x << "," << start.y << "\n";
  std::cout << "终点: " << finish.x << "," << finish.y << "\n";
  return 0;
}
