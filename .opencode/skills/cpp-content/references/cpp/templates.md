# 模板与泛型

> 速查：模板放头文件 · concepts（C++20）约束优先于 SFINAE · `if constexpr`（C++17）做编译期分支 · 转发引用 `T&&` + `std::forward` 保值类别 · CTAD（C++17）省去显式类型

## 为什么重要

模板让一份代码服务多种类型，是 STL 与多数现代库的基石。但"泛型"也是 C++ 最容易写出**难以理解的错误信息**和**隐性开销**的地方：传统模板靠 SFINAE（替换失败并非错误）做约束，报错时编译器把整条重载决议链摊给你看；值类别转发写错则悄悄多出拷贝；模板定义放错翻译单元会直接链接失败。C++20 起用 concepts 把"约束"显式表达出来，把编译期分支交给 `if constexpr`，心智负担大幅下降。

## 核心规则

- **模板定义放在头文件**（C++98 起）：模板在实例化处才生成代码，跨翻译单元需可见；实在要隔离编译单元就用显式实例化 `template class Foo<int>;`。
- **用 concepts / requires 约束**（C++20）：优先于传统 SFINAE，错误信息直接指出"约束不满足"，可读性更好。
- **`if constexpr`**（C++17）：编译期分支，不满足的分支直接不实例化——替代大量 `std::enable_if` 技巧。
- **转发引用 `T&&` + `std::forward<T>`**（C++11）：保持实参的值类别（左值仍左值、右值仍右值）；注意 `T&&` 仅在类型推导中才是转发引用，普通函数参数 `Widget&&` 是右值引用。
- **类模板参数推导 CTAD**（C++17）：构造时省去 `std::pair<int, std::string>{...}` 这类冗长写法，编译器从实参推导模板参数。
- **避免过度泛型**：可读性优先；能用 `std::function`、接口抽象或 concrete 类型解决的问题，不必硬上模板元编程。

::: {.callout-important}
## 关键概念
模板的核心心智模型是**"约束显式化、实例化零噪声"**：C++20 的 concepts 把"哪些类型合法"变成首类编译错误而非淹没在 SFINAE 噪声里，`if constexpr` 让编译期分支不再实例化无用代码，转发引用配 `std::forward` 把值类别原样传递——三者共同把泛型从"难调试的黑魔法"变成可读、可控的抽象。
:::

## 正例 ✓ vs 反例 ✗

✓ 用 concept 约束 + `if constexpr` 分发，错误信息清晰、无冗余实例化：

```cpp
#include <concepts>
#include <type_traits>
#include <string>
#include <iostream>

// concept：只接受整数类型（C++20）
template <std::integral T>
void Print(T v) {
  if constexpr (std::is_signed_v<T>) {
    std::cout << "有符号整数: " << v << "\n";
  } else {
    std::cout << "无符号整数: " << v << "\n";
  }
}

int main() {
  Print(42);          // 有符号整数
  Print(42u);         // 无符号整数
  // Print(std::string{});  // 编译错误：不满足 std::integral 约束
}
```

✗ 用传统 SFINAE 做约束，报错信息冗长难读，且分支靠 `enable_if` 堆砌：

```cpp
#include <type_traits>
#include <string>
#include <iostream>

// 用 enable_if 模拟"仅整数"约束，错误信息晦涩
template <typename T,
     typename = typename std::enable_if<std::is_integral<T>::value>::type>
void Print(T v) {
  std::cout << v << "\n";
}

int main() {
  Print(42);
  // Print(std::string{});  // 报错：一堆 substitution failure 噪声
}
```

✓ 转发引用 + `std::forward` 精确转发，大对象零拷贝移动：

```cpp
#include <utility>
#include <string>
#include <vector>

// T&& 是转发引用：左值保持左值、右值保持右值
template <typename T>
void Sink(T&& x) {
  std::vector<std::string> v;
  v.emplace_back(std::forward<T>(x));  // 右值时移动，左值时拷贝
}

int main() {
  std::string s = "hi";
  Sink(s);              // 拷贝（s 仍可用）
  Sink(std::string{"by"}); // 移动
}
```

✗ 错把 `T&&` 当作右值引用滥用，或对非推导上下文误用，导致意外拷贝或编译失败：

```cpp
#include <string>
#include <vector>
#include <utility>

// 注意：这不是转发引用——T 已确定，Widget&& 就是右值引用
struct Widget {
  void Sink(std::string&& x) {  // 只接受右值
    v.emplace_back(std::move(x));
  }
  std::vector<std::string> v;
};

int main() {
  Widget w;
  std::string s = "hi";
  // w.Sink(s);   // 编译错误：不能把左值绑到右值引用
  w.Sink(std::move(s));  // 必须手动 std::move
}
```

两组对照说明：concepts 让"约束不满足"成为**首类编译错误**而非淹没在 SFINAE 噪声里；`if constexpr` 让编译期分支不再实例化无用代码。转发引用必须配 `std::forward` 才能保住值类别——否则右值会被当左值，错失移动优化。

## 常见误区

- 把普通函数参数 `Foo&&` 当成转发引用——只有涉及类型推导的 `T&&` 才是转发引用。
- 忘记 `std::forward`，转发到下游时右值被降级为左值，多出拷贝。
- 模板定义只写在 `.cpp` 里，链接时报"未定义引用"（模板需头文件可见或显式实例化）。
- 用 CTAD 时误以为 `std::vector v{10}` 是 10 个 0——`{10}` 是单元素 initializer_list，要 10 个元素得写 `std::vector<int> v(10)`。
- 用 SFINAE 硬凑约束而不用 concepts，错误信息对调用方极不友好。

## 小结
- 模板定义需放在头文件（或在 `.cpp` 显式实例化），否则跨翻译单元实例化的代码不可见而链接失败。
- 用 concepts/requires 表达约束、用 `if constexpr` 做编译期分支，优先于传统 SFINAE 与 `enable_if`，错误信息更友好、分支零实例化。
- 转发引用 `T&&`（仅类型推导中）必须配 `std::forward` 保值类别，普通 `Widget&&` 只是右值引用；避免过度泛型，可读性优先。

## 延伸阅读

- C++ Core Guidelines：[T.1–T.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-templates)（模板设计）
- C++ Core Guidelines：[T.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#tt-where)（concepts）
- cppreference：[Constraints and concepts](https://en.cppreference.com/w/cpp/language/constraints)
- cppreference：[std::forward](https://en.cppreference.com/w/cpp/utility/forward)
- 本备忘录：`./modern-cpp.md`（移动/转发基础）、`./stl.md`（容器与算法）、`./pitfalls-ub.md`（实例化期 UB）
