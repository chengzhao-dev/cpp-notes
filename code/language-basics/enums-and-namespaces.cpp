// 枚举与命名空间示例：定义封闭取值的状态类型并输出其编号。
#include <iostream>

enum class GameState { kOngoing, kWin, kDraw };

int main() {
  GameState state{GameState::kOngoing};
  std::cout << "初始状态编号: " << static_cast<int>(state) << "\n";
  state = GameState::kWin;
  std::cout << "当前状态编号: " << static_cast<int>(state) << "\n";
  return 0;
}
