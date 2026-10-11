// 简单项目设计示例：用 Board 守住棋盘状态，把显示留给调用方。
#include <array>
#include <cstddef>
#include <cstdint>
#include <iostream>

namespace example {

// 棋盘格子的状态。
enum class CellState : std::uint8_t {
  kEmpty = 0,
  kCross = 1,
  kNought = 2,
};

// 棋盘格子的行列坐标，行和列从 0 开始。
struct CellPosition {
  int row;
  int col;
};

// 一个 3×3 棋盘。
// 负责保存格子状态，并拒绝无效或重复的落子。
class Board {
public:
  // 判断坐标是否在棋盘范围内。
  [[nodiscard]] static constexpr bool IsValidPosition(CellPosition position) {
    return position.row >= 0 && position.row < kRows && position.col >= 0 &&
           position.col < kCols;
  }

  // 返回指定坐标处的格子状态。
  [[nodiscard]] CellState CellAt(CellPosition position) const {
    return cells_.at(ToIndex(position));
  }

  // 尝试在指定坐标落子。
  // 坐标无效、状态为空或格子已占用时返回 false。
  [[nodiscard]] bool Place(CellPosition position, CellState state) {
    if (!IsValidPosition(position) || state == CellState::kEmpty) {
      return false;
    }
    CellState &cell = cells_.at(ToIndex(position));
    if (cell != CellState::kEmpty) {
      return false;
    }
    cell = state;
    return true;
  }

private:
  // 将已验证的坐标转换为行优先下标。
  [[nodiscard]] static constexpr std::size_t ToIndex(CellPosition position) {
    return static_cast<std::size_t>((position.row * kCols) + position.col);
  }

  // 按行优先保存棋盘格子。
  std::array<CellState, 9> cells_{};

  static constexpr int kRows = 3;
  static constexpr int kCols = 3;
};

} // namespace example

int main() {
  example::Board board;
  const bool placed =
      board.Place({.row = 1, .col = 1}, example::CellState::kCross);
  const char center =
      board.CellAt({.row = 1, .col = 1}) == example::CellState::kCross ? 'X'
                                                                       : ' ';
  std::cout << "中心格: " << center << ", 落子成功: " << placed << "\n";
  return 0;
}
