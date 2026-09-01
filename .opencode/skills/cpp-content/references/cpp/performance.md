# 性能优化要点

> 速查：先测量再优化 · 减少堆分配（`reserve`/SSO/栈） · 移动大对象 · 避免无谓拷贝 · 缓存友好顺序遍历 · `constexpr` 编译期计算

## 为什么重要

"C++ 快"不是自动获得的——错误的数据结构或拷贝习惯能让程序慢一个数量级。*C++ Primer* 与 *Effective C++* 的共识：**优化前先 profiling 定位热点，再针对瓶颈下手**，凭直觉优化常常无效甚至起反作用。

## 核心规则

- **先测量再优化**：用 profiler（如 `perf`、`gprof`、或 `-ftime-trace`）定位热点，不凭猜测。
- **减少堆分配**：优先栈对象、复用缓冲；已知容量先 `reserve`；小字符串走 SSO（短字符串优化）。
- **移动语义**（C++11）：返回大对象直接按值返回；形参大对象按值接收再 `std::move`。
- **避免不必要拷贝**：`const&` 传参；避免按值返回复杂对象；用 `std::string_view`（C++17）传只读字符串。
- **缓存友好**：顺序遍历 `vector` 远优于链表随机访问；减少指针跳跃与缓存未命中。
- **编译期计算**（C++11/20）：`constexpr`/`consteval` 把计算移到编译期；模板元编程仅在必要、收益明确时使用。
- **多线程**：低竞争时用原子操作优于互斥锁；减少锁竞争与临界区长度。

::: {.callout-important}
## 关键概念
性能的核心心智模型是**"先测量、再针对瓶颈下手"**：C++ 的快来自正确的数据结构与零拷贝习惯（栈/SSO/`reserve`/移动/`string_view`/缓存友好遍历），而非凭直觉优化；盲目加 `std::move` 或过早改写可读性，常换来微优化甚至负优化。
:::

## 正例 ✓ vs 反例 ✗

✓ 已知容量先 `reserve`，单次分配、零重分配：

```cpp
// 片段
std::vector<int> Collect(const std::vector<int>& src) {
  std::vector<int> out;
  out.reserve(src.size());        // 避免反复扩容拷贝
  for (int x : src) out.push_back(x * 2);
  return out;                     // NRVO / 移动，无深拷贝
}
```

✗ 边增长边扩容，且反复按值返回大对象：

```cpp
// 片段
std::vector<int> Collect(const std::vector<int>& src) {
  std::vector<int> out;
  // 缺 reserve：每次 push_back 都可能触发扩容拷贝
  for (int x : src) out.push_back(x * 2);
  return out;
}
```

✓ 只读字符串用 `std::string_view` 避免拷贝与分配：

```cpp
// 片段
#include <string_view>
void Log(std::string_view msg) { /* 零拷贝，可接 string / "字面量" */ }
```

✗ 仅读取却传 `const std::string&` 并要求调用方先构造 `std::string`（可能触发分配）：

```cpp
// 片段
void Log(const std::string& msg);  // "字面量" 需隐式构造临时 string
```

## 常见误区

- 盲目"用 `std::move` 一切"——对小块类型（如 `int`）移动无收益，甚至妨碍 RVO。
- 把 `std::vector<bool>` 当普通容器做性能假设（位压缩、非连续）。
- 过早优化：在没 profiling 前改写可读性换微优化。
- 忽视 `reserve` 却用 `push_back` 灌百万级元素——扩容成本被放大。

## 小结
- 优化前先用 profiler 定位热点，不凭猜测——过早优化常无效甚至起反作用。
- 减少堆分配（`reserve`、栈对象、小字符串 SSO）、用移动语义与 `std::string_view` 避免无谓拷贝，顺序遍历 `vector` 远比链表缓存友好。
- `constexpr`/`consteval` 把计算移到编译期；小类型（如 `int`）移动无收益，`std::vector<bool>` 是位压缩特化需谨慎对待。

## 延伸阅读

- C++ Core Guidelines：[Per](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#per-performance) 性能规则
- *Effective C++*（Meyers）第 5 章：实现与效率
- 本备忘录：`./modern-cpp.md`（移动/`noexcept`）、`./stl.md`（容器与缓存友好）、`./toolchain.md`（`-O2`/sanitizer）
