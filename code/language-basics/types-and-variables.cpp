// 类型示例：展示基础类型、初始化、赋值、作用域和 auto。
#include <iostream>
#include <string>

int main() {
  int age = 18;
  double scale = 1.5;
  bool ready = true;
  char grade = 'A';
  std::string name = "Ada";

  age = 19;
  const auto score = 95.5;

  {
    int localValue = 7;
    std::cout << "局部变量: " << localValue << "\n";
  }

  std::cout << name << " 的年龄是 " << age << "\n";
  std::cout << "缩放: " << scale << "\n";
  std::cout << "是否就绪: " << ready << "\n";
  std::cout << "等级: " << grade << "\n";
  std::cout << "分数: " << score << "\n";
  return 0;
}
