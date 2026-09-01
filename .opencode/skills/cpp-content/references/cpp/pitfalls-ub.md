# 常见陷阱与未定义行为（UB）

> 速查：悬垂指针/引用 · 迭代器失效 · signed 溢出是 UB · `volatile` 不等于线程安全 · 浮点别用 `==` · 空指针解引用前检查

## 为什么重要

C++ 的许多"诡异现象"本质是**未定义行为（UB）**：编译器一旦能证明 UB，便可以任意方式优化，结果不可预测且随编译选项/版本变化。**识别 UB 比记忆语法更重要**——这是 *C++ Primer* 反复强调、*C++ Core Guidelines* 用大量规则封堵的点。

## 核心规则

- **悬垂指针/引用**：指向已析构对象即 UB。绝不返回局部对象的引用/指针。
- **迭代器/引用失效**（C++98 起）：向 `vector`/`string`/`deque` 插入/删除会使迭代器、引用、指针失效；`unordered_map` rehash 同理。失效后不得使用旧迭代器。
- **整数规则**：**有符号溢出是 UB**；`size_t` 等无符号会回绕（不是 UB，但易错）。`signed`/`unsigned` 混用导致负数上溢要警惕。
- **多线程**：共享可变数据必须同步（`std::mutex`、原子变量）；**`volatile` 不是同步原语**，只防编译器优化、不保证线程安全。`std::atomic` 用于简单计数器/标志。
- **对象生命周期**：跨翻译单元静态/全局对象初始化顺序不确定、析构顺序未定义；用"首次使用即初始化"的函数局部静态规避。
- **强转**：`reinterpret_cast`/C 风格强转可能违反严格别名规则而 UB；避免不必要的指针强转。
- **浮点比较**：勿用 `==` 直接比较浮点，用容差。
- **空指针解引用**：使用返回的裸指针/迭代器（如 `map::find`、`vector::data` 空容器）前检查。

::: {.callout-important}
## 关键概念
UB（未定义行为）的核心心智模型是**"编译器一旦证明你越界，便可任意优化，结果随版本与选项漂移"**：识别并规避 UB 比记忆语法更重要，因为"这次跑对了"只是 UB 没发作，而非没有 UB——这是 C++ 大量诡异现象与线上崩溃的根源。
:::

## 正例 ✓ vs 反例 ✗

✓ 返回值的副本/移动，调用方拥有独立生命期：

```cpp
// 片段
std::string Make() {
  std::string s = "hello";
  return s;                 // 返回副本/移动，调用方安全持有
}
```

✗ 返回局部对象的引用——悬垂 UB：

```cpp
// 片段
std::string& Make() {
  std::string s = "hello";
  return s;                 // s 析构后引用悬垂，使用即 UB
}
```

✓ 共享数据用 `std::atomic` 同步：

```cpp
// 片段
#include <atomic>
std::atomic<int> counter{0};
counter.fetch_add(1, std::memory_order_relaxed); // 线程安全
```

✗ 以为 `volatile` 能护住并发：

```cpp
// 片段
volatile int flag = 0;
// 多线程读写 flag 仍是无数据竞争 UB——volatile 不提供同步
```

✓ 浮点用容差比较：

```cpp
// 片段
bool Near(double a, double b) { return std::abs(a - b) < 1e-9; }
```

## 常见误区

- 把"程序这次跑对了"当成"没有 UB"——UB 只是这次没发作。
- 依赖 `delete` 后置空指针再判空来"防重复释放"——反模式，应靠 RAII 从根上避免（见 `modern-cpp.md`）。
- 以为加了 `-O0` 调试就没有 UB 后果——未定义就是未定义。
- 用 `std::vector<bool>` 取地址/引用的例外行为（它是特化位容器），别当普通 `vector` 用。

## 小结
- 悬垂指针/引用与迭代器失效是最常见 UB：绝不返回局部对象的引用，向 `vector`/`string`/`deque` 插入删除后旧迭代器即失效。
- 有符号整数溢出是 UB、`volatile` 不等于线程安全（同步要用 `std::mutex`/`std::atomic`）、浮点勿用 `==` 比较、空指针解引用前务必检查。
- "能编译通过/这次跑对"不等于没有 UB——用 sanitizer 与严格警告在开发期兜底，依赖 RAII 从根上消除一类生命周期错误。

## 延伸阅读

- C++ Core Guidelines：[ES.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-int-types)（类型/范围）
- C++ Core Guidelines：[CP.*](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#cp-concurrency)（并发）
- cppreference：[Undefined behavior](https://en.cppreference.com/w/cpp/language/ub)
- 本备忘录：`./modern-cpp.md`（RAII/生命周期）、`./stl.md`（迭代器失效）、`./engineering.md`（线程安全审查）
