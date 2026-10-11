// 函数示例：按值接收一个整数，按值返回另一个整数。
#include <iostream>

// 由输入整数得到它的两倍。
int DoubleOf(int value) {
  return value * 2;
}

int main() {
  int input{21};
  int result = DoubleOf(input);
  std::cout << "结果: " << result << "\n";
  return 0;
}
