// 最小可运行示例用于验证工具链
// 标准库的输入 / 输出功能都在 iostream 里
#include <iostream>

int main() {
  // 常量使用 k 前缀和大驼峰命名
  const int kAnswer = 42;

  // 把结果写入标准输出。"\n" 比 std::endl 少一次刷新
  std::cout << "answer: " << kAnswer << "\n";

  // 返回 0 表示程序正常结束
  return 0;
}
