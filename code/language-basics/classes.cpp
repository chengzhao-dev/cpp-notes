// 类示例：数据和不变量放进类，查询函数带 const。
#include <iostream>

// 一个只能通过成员函数修改的计数。
class Counter {
 public:
  explicit Counter(int start) : value_{start} {}

  // 返回当前计数。尾部 const 承诺不修改实例。
  [[nodiscard]] int Value() const {
    return value_;
  }

  // 把增量加进计数。
  void Add(int delta) {
    value_ += delta;
  }

 private:
  int value_;
};

int main() {
  Counter counter{2};
  counter.Add(3);
  std::cout << "计数: " << counter.Value() << "\n";
  return 0;
}
