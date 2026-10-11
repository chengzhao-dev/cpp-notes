// nodiscard 示例：标注过的返回值要处理，不能随手丢弃。
#include <cstdint>
#include <iostream>

// 落子结果：接受或拒绝。
enum class ApplyResult : std::uint8_t {
  kAccepted,  // 接受落子，格子已标记。
  kRejected,  // 拒绝落子，格子保持原样。
};

// 一个棋盘格子：重复落子会被拒绝。
struct Cell {
  bool filled{false};

  // 落子结果承载成败，标注后丢弃会得到编译器警告。
  [[nodiscard]] ApplyResult Place() {
    if (filled) {
      return ApplyResult::kRejected;
    }
    filled = true;
    return ApplyResult::kAccepted;
  }
};

int main() {
  Cell cell;
  ApplyResult first = cell.Place();
  ApplyResult second = cell.Place();
  std::cout << "第一次落子编号: " << static_cast<int>(first) << "\n";
  std::cout << "第二次落子编号: " << static_cast<int>(second) << "\n";
  return 0;
}
