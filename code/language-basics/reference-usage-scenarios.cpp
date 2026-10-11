// 引用使用场景示例：按场景为参数选择按值、const 引用与非 const 引用。
#include <iostream>
#include <string>
#include <vector>

// 只读小对象：按值传递，拷贝廉价，调用处清晰。
int SumCoords(int row, int col) {
  return (row * 10) + col;
}

// 只读大对象：const 引用避免拷贝，函数承诺不修改元素。
int TotalChars(const std::vector<std::string>& words) {
  int total = 0;
  for (const std::string& word : words) {
    total += static_cast<int>(word.size());
  }
  return total;
}

// 需要修改且必须存在：非 const 引用承担输出，不可为空。
void Capitalize(std::string& text) {
  for (char& ch : text) {
    if (ch >= 'a' && ch <= 'z') {
      ch = static_cast<char>(ch - 'a' + 'A');
    }
  }
}

int main() {
  std::vector<std::string> words{"board", "game", "grid"};
  std::string title{"tic tac toe"};

  std::cout << "坐标和: " << SumCoords(1, 2) << "\n";
  std::cout << "总字符数: " << TotalChars(words) << "\n";

  Capitalize(title);
  std::cout << "大写标题: " << title << "\n";
  return 0;
}
