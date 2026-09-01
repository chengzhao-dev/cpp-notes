# 现代 C++ 核心

> 速查：RAII 管资源 · `unique_ptr` 默认 · 移动而非拷贝 · `const` 正确性 · `auto`/`nullptr`/`enum class`/`override` · `{}` 初始化防窄化

## 为什么重要

C++ 不强制你用现代特性，但**不用现代 C++ 几乎必然写出更慢、更易漏的内存/生命周期错误**。现代 C++（C++11 起，本备忘录默认 C++20）把大量"靠纪律保证"的事情变成了"靠类型/编译器保证"——这是 *C++ Primer*（第 5 版全面转向 C++11）与 *C++ Core Guidelines* 的核心立场。

## 核心规则

- **RAII**（C++98 即有，C++11 后成绝对主流）：资源（内存、文件、锁、socket）在构造函数获取、析构函数释放；**绝不手动 `new`/`delete`**（实现低级容器除外）。
- **智能指针**（C++11）：`unique_ptr` 默认独占、`shared_ptr` 仅在确需共享时用、`weak_ptr` 破循环。用 `make_unique`/`make_shared` 创建（异常安全、减少分配）。
- **移动语义**（C++11）：返回临时对象直接 `return`，依赖 NRVO/移动；大对象按值返回或移动。移动构造务必标 `noexcept`，否则 `vector` 扩容退化为拷贝。
- **const 正确性**：只读成员函数加 `const`；参数能 `const&` 就不传值/非 `const&`；返回 `const&` 警惕悬垂。
- **auto / 结构化绑定**（C++11/17）：`auto` 减冗长但别隐藏预期类型；遍历优先 `const auto&`。
- **显式优于隐式**：`nullptr` 而非 `NULL`/`0`；`enum class` 而非裸 `enum`；重写虚函数标 `override`/`final`；单参构造加 `explicit`。
- **统一初始化 `{}`**（C++11）：避免窄化转换；注意 `vector<int> v{1,2,3}`（初始化列表）与 `vector<int> v(10,1)`（10 个 1）的区别。

::: {.callout-important}
## 关键概念
现代 C++ 的核心心智模型是**把"靠纪律保证"的事变成"靠类型和编译器保证"**——RAII 用析构函数兜底资源回收，智能指针把所有权写进类型，移动语义让"返回大对象"既安全又零拷贝，从而从语言层面消除一类内存/生命周期错误。
:::

## 正例 ✓ vs 反例 ✗

✓ 用 RAII + 智能指针，资源自动回收：

```cpp
// 片段
#include <memory>
#include <fstream>

void Process() {
  auto file = std::make_unique<std::ofstream>("log.txt"); // 构造即获取
  auto buf  = std::make_unique<std::vector<int>>(1'000'000);
  // 离开作用域自动析构、关闭文件、释放内存——无需手写 delete
}
```

✗ 手动 `new`/`delete`，异常路径必泄漏：

```cpp
// 片段
void Process() {
  std::ofstream* file = new std::ofstream("log.txt");
  if (something_wrong()) return;        // 泄漏：没 delete
  // ... 若此处抛异常，同样泄漏
  delete file;
}
```

✓ 移动语义：返回大对象直接按值返回：

```cpp
// 片段
std::vector<int> MakeBig() {
  std::vector<int> v(1'000'000);
  return v;          // NRVO / 移动，零拷贝
}
std::vector<int> big = MakeBig();
```

✗ 无谓拷贝 + 未标 `noexcept` 致 `vector` 扩容退化：

```cpp
// 片段
struct Widget {
  Widget(Widget&&) /* 忘写 noexcept */ { /* ... */ }
};
std::vector<Widget> v;
v.reserve(1);          // 一旦扩容，因移动非 noexcept 而改拷贝——性能骤降
```

## 常见误区

- 认为 `shared_ptr` "更安全"就到处用——共享所有权是设计信号，滥用会掩盖生命周期、引入循环引用。
- 返回 `const&` 指向局部/临时对象（悬垂）。
- `auto` 推导出不期望的类型（如 `auto x = {1}` 得 `std::initializer_list`），必要时写清类型。
- 把统一初始化当万能：`std::vector<int> v(10)` 与 `std::vector<int> v{10}` 语义不同，别混用。

## 小结
- RAII 是基石：资源在构造获取、析构释放，绝不手动 `new`/`delete`，让编译器替你兜底生命周期。
- 智能指针表达所有权（`unique_ptr` 默认独占、`shared_ptr` 仅在确需共享时用），移动语义让按值返回大对象零拷贝，且移动构造务必标 `noexcept`。
- 用显式优于隐式（`nullptr`/`enum class`/`override`）与统一初始化 `{}` 防窄化，能在编译期拦下的错误不要留到运行时。

## 延伸阅读

- C++ Core Guidelines：[R.1–R.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii)（资源管理）
- C++ Core Guidelines：[F.15](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#fcall)（参数传递）
- *C++ Primer* 第 12、13 章（动态内存、拷贝控制）
- 本备忘录：`pitfalls-ub.md`（悬垂/失效）、`stl.md`（容器选择）
