// 强类型包装示例：用两个包装类型区分距离与时长。
#include <iostream>

struct Meters {
  double value{0};
};

struct Seconds {
  double value{0};
};

int main() {
  Meters distance{100.0};
  Seconds duration{9.58};
  // distance 与 duration 类型不同，互相赋值会被编译器拒绝
  std::cout << "距离: " << distance.value << " 米\n";
  std::cout << "时长: " << duration.value << " 秒\n";
  return 0;
}
