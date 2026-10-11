// 枚举类示例：封闭取值的状态类型、底层类型与按值传参。
#include <cstdint>
#include <iostream>

// 对局状态
enum class GameState : std::uint8_t {
  kOngoing = 0,  // 对局尚未结束，可继续落子。
  kWin = 1,      // 一方达成三连获胜。
  kDraw = 2,     // 棋盘下满且无人三连。
};

// 对局玩家：kX 先手，kO 后手。
enum class Player : std::uint8_t {
  kX = 0,
  kO = 1,
};

// 棋盘格子状态
enum class CellState : std::uint8_t {
  kEmpty = 0,  // 空格。
  kX = 1,
  kO = 2,
};

// 由对局玩家得到落子用的棋盘格子状态。
CellState PlayerToCellState(Player player) {
  return player == Player::kX ? CellState::kX : CellState::kO;
}

int main() {
  GameState state{GameState::kOngoing};
  std::cout << "初始状态编号: " << static_cast<int>(state) << "\n";
  state = GameState::kWin;
  std::cout << "当前状态编号: " << static_cast<int>(state) << "\n";

  Player current{Player::kO};
  CellState mark = PlayerToCellState(current);
  std::cout << "当前玩家状态编号: " << static_cast<int>(mark) << "\n";
  return 0;
}
