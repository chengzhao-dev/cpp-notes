// 指针使用场景示例：可空输入、可选输出与判空约定。
#include <iostream>
#include <string>

// 可选的只读输入：const 指针，传 nullptr 表示没有这项信息。
void PrintTask(const std::string& title, const std::string* note) {
  std::cout << "任务: " << title << "\n";
  if (note != nullptr) {
    std::cout << "备注: " << *note << "\n";
  }
}

// 可选输出：非 const 指针；找到首个数字时写入并返回 true。
bool TryFirstDigit(const std::string& text, int* digit_out) {
  for (char ch : text) {
    if (ch >= '0' && ch <= '9') {
      *digit_out = ch - '0';
      return true;
    }
  }
  return false;
}

int main() {
  const std::string note{"每周重开一局"};
  PrintTask("井字棋", &note);
  PrintTask("自由练习", nullptr);

  int digit = 0;
  if (TryFirstDigit("第 3 局", &digit)) {
    std::cout << "首个数字: " << digit << "\n";
  }
  if (!TryFirstDigit("残局", &digit)) {
    std::cout << "残局不含数字\n";
  }
  return 0;
}
