// 最小断言式测试（未引框架；组合用法成熟后可换 Catch2 / GTest）
#include <cassert>

#include "{{PROJECT_NAME}}/{{PROJECT_NAME}}.h"

int main() {
  assert(Answer() == 42);
  return 0;
}
