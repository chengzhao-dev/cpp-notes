# 工程实践与大型项目

> 速查：小步可编译迭代 · 所有权/生命周期优先审查 · const 正确性 · 异常安全靠 RAII · 可恢复错误用 `std::expected`/`optional` · 关键逻辑补测试

## 为什么重要

大型 C++ 项目最贵的不是"写不出功能"，而是**改一处崩三处**：悬垂引用、double-free、数据竞争、迭代器失效，往往潜伏到上线才爆发；而"能跑"的代码若所有权模型混乱、接口边界模糊，后续维护成本会指数级上升。C++ Primer 与 Core Guidelines 的共识是——用明确的**所有权（ownership）与生命周期（lifetime）**模型约束设计，让编译器与审查清单替你兜底，而非靠个人纪律。

## 核心规则

- **工作流**：需求理解 → 模块/接口设计 → 骨架（目录+构建系统）→ **每步可编译可运行的小步实现** → 编译/调试 → 测试 → 评审重构。
- **所有权与生命周期**：明确每个对象归谁所有；用 `unique_ptr` 表达独占、避免悬垂/double-free/迭代器失效（详见 `./modern-cpp.md`）。
- **const 正确性**：只读成员函数与参数加 `const`；返回 `const&` 警惕悬垂。
- **异常安全**：构造函数在体内完成资源获取（RAII），保证异常时资源不泄漏；不在析构函数、`noexcept` 函数中抛异常。
- **错误处理**：可恢复错误用异常或 `std::expected`（C++23）、`std::optional`；明确错误边界，避免跨模块抛出实现细节。
- **命名与组织**：排版 LLVM / 命名 Google（类型/函数大驼峰、变量小写下划线，唯一出处见 `./code-style.md`）；头文件最小化接口，实现放 `.cpp` 减少编译依赖。
- **线程安全**：共享可变数据必须同步；用 `const`、不可变数据或明确的所有权降低竞争面。

::: {.callout-important}
## 关键概念
大型 C++ 工程的核心心智模型是**"用明确的所有权与生命周期约束设计"**：把"谁负责释放、对象活多久"写进类型（如 `unique_ptr` 表达独占），让编译器与审查清单替你兜底——相比靠个人纪律，这能从根上抑制悬垂、double-free 与耦合爆炸。
:::

## 正例 ✓ vs 反例 ✗

✓ 小步迭代 + 明确所有权，每步可编译；错误用返回值表达边界：

```cpp
// 片段
#include <memory>
#include <vector>
#include <optional>

// 模块接口：明确所有权——返回独占指针，调用方拥有结果
std::unique_ptr<std::vector<int>> Load() {
  auto v = std::make_unique<std::vector<int>>();
  v->push_back(1);
  return v;  // 移动返回，零拷贝
}

// 可恢复失败用 std::optional 而非抛异常
std::optional<int> At(const std::vector<int>& v, std::size_t i) {
  if (i >= v.size()) return std::nullopt;  // 边界清晰
  return v[i];
}
```

✗ 大块一次性实现、所有权不清、用异常跨边界抛内部细节：

```cpp
// 片段
#include <vector>
#include <stdexcept>

std::vector<int>* Load() {           // 返回裸指针：谁负责 delete？
  auto v = new std::vector<int>(); // 异常路径泄漏
  // ...
  return v;
}

int At(std::vector<int>& v, std::size_t i) {
  if (i >= v.size()) throw std::runtime_error("bad"); // 跨模块抛实现细节
  return v[i];
}
```

对照说明：正例用 `unique_ptr` 把"释放责任"编码进类型，用 `optional` 把"可能失败"写进签名，调用方无法误用。反例返回裸指针让所有权悬空（易泄漏/谁删都错），用异常把内部错误甩给上层，破坏模块边界。代价上，反例的泄漏与耦合会在重构时集中引爆。

## 常见误区

- 大段代码一次写完再编译——错一处全盘重来，不如小步可编译迭代。
- 忽略所有权模型：返回裸指针/引用指向局部或临时对象（悬垂）。
- 在析构函数或 `noexcept` 函数里抛异常，导致 `std::terminate`。
- 共享可变状态不保护：以为"只读"却在某处被改，埋下数据竞争。
- 过度模板/魔法数字降低可读性，优先用 `<algorithm>` 与具名常量。
- 只写 happy path 测试，漏掉边界与异常路径。

## 小结
- 采用小步可编译迭代：每步可编译可运行，避免大段代码一次写完再调试，重构成本随可编译粒度显著下降。
- 用 `unique_ptr` 把释放责任编码进类型、用 `optional`/`expected` 把"可能失败"写进签名，明确所有权与错误边界，杜绝裸指针与跨模块抛内部细节。
- 异常安全靠 RAII（构造即获取、异常不泄漏），不在析构/`noexcept` 函数抛异常；共享可变状态必须同步，关键逻辑补边界与异常路径测试。

## 延伸阅读

- C++ Core Guidelines：[I.1–I.5](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-interfaces)（接口设计）
- C++ Core Guidelines：[E.1–E.6](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-errors)（错误处理）
- C++ Core Guidelines：[Con.1–Con.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-const)（const）
- *C++ Primer* 第 13、18 章（拷贝控制、大型程序工具）
- 本备忘录：`./modern-cpp.md`（RAII/智能指针）、`./toolchain.md`（构建与 sanitizer）、
  `./pitfalls-ub.md`（悬垂/失效）、`./templates.md`（泛型设计）
