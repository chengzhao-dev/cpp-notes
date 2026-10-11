// 成员函数上的 const 示例：查询函数与修改函数的承诺不同。
#include <cstdint>
#include <iostream>

// 棋盘格子状态
enum class CellState : std::uint8_t {
  kEmpty = 0,  // 空格。
  kX = 1,
  kO = 2,
};

// 一个棋盘格子：查询用尾部 const，落子要写入成员。
struct Cell {
  CellState state{CellState::kEmpty};

  // 查询函数：尾部 const 承诺不修改实例。
  CellState GetCellState() const {
    return state;
  }

  // 修改函数：没有尾部 const，允许写入成员。
  void Place(CellState new_state) {
    state = new_state;
  }
};

int main() {
  Cell cell;
  cell.Place(CellState::kX);
  std::cout << "格子状态编号: " << static_cast<int>(cell.GetCellState()) << "\n";
  return 0;
}
