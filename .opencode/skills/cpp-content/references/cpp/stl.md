# STL 使用要点

> 速查：默认 `vector` · 算法优先手写循环 · erase-remove 惯用法 · `reserve` 已知容量 · 避免重复 `map[k]` 查找

## 为什么重要

STL 不是"一堆容器"，而是一套**复杂度有契约**的抽象。选错容器或手写本可由算法表达的循环，往往换来隐蔽的性能退化与更多 bug。*C++ Primer* 与 *Effective STL* 的共同建议是：**先选对容器，再用算法，最后才考虑手写**。

## 核心规则

- **容器选择**（各有时间/空间契约）：
  - 顺序访问、`push_back` 为主 → `std::vector`（C++98 默认之选）。
  - 头尾插入频繁 → `std::deque`；中间插入频繁 → `std::list`/`std::forward_list`。
  - 需要自动排序 → `std::set`/`std::multiset`；键值查找 → `std::map`（有序）或 `std::unordered_map`（哈希、更快但无序）。
  - 数量小且编译期已知 → `std::array` 优于 `std::vector`。
  - 多次字符串拼接 → `std::string` 直接 `+=`（内部连续 `reserve`）或 `ostringstream`，避免反复 `+` 产生多次拷贝。
- **算法优先于手写循环**（C++98 起）：`<algorithm>` 的 `std::find`/`std::sort`/`std::transform`/`std::remove_if`/`std::accumulate` 更可读、更少出错。
- **erase-remove 惯用法**（C++98 起）：删除满足条件的元素用 `v.erase(std::remove_if(...), v.end())`，**不要在循环里逐个 `erase`**（O(n²) 且易迭代器失效）。
- **避免重复查找**：`auto it = m.find(k); if (it != m.end()) ...`，而非两次 `m[k]`（后者在缺失时会插入）。
- **`reserve`**：已知容量先 `reserve`，避免反复扩容拷贝。
- **字符串字面量 `""s`**（C++14，需 `using namespace std::string_literals;`）避免 `const char*` 到 `string` 的隐式构造。

::: {.callout-important}
## 关键概念
STL 的核心心智模型是**把容器视为"有复杂度契约的抽象"**：每种容器/算法都承诺了明确的时间与空间代价，先按访问模式选对容器、再用算法表达意图，比手写循环更可读也更难出错——性能与正确性都来自"选对工具"而非"写得更聪明"。
:::

## 正例 ✓ vs 反例 ✗

✓ 用 erase-remove 删除偶数，单次 O(n) 且无迭代器失效：

```cpp
// 片段
#include <vector>
#include <algorithm>

void DropEven(std::vector<int>& v) {
  v.erase(std::remove_if(v.begin(), v.end(),
       [](int x) { return x % 2 == 0; }),
      v.end());
}
```

✗ 循环里逐个 `erase`，迭代器失效且 O(n²)：

```cpp
// 片段
void DropEven(std::vector<int>& v) {
  for (auto it = v.begin(); it != v.end(); ++it) {
    if (*it % 2 == 0) v.erase(it); // it 已失效；且漏删、复杂度爆炸
  }
}
```

✓ 单次查找并用结果，不重复索引：

```cpp
// 片段
auto it = m.find(key);
if (it != m.end()) { Use(it->second); }   // 一次查找
```

✗ 重复 `operator[]` 既低效又可能误插入：

```cpp
// 片段
if (m[key] != 0) { ... }   // key 不存在时被插入为默认值
```

## 常见误区

- 用 `std::list` 追求"插入不失效"，却忽略其缓存不友好、遍历远慢于 `vector`。
- 以为 `std::map` 比 `unordered_map` 快（哈希版本通常更快，除非需要有序）。
- `reserve` 之后又 `resize`/`clear` 行为混淆：`clear` 不释放容量，`reserve` 只为容量。
- 返回 `auto&&` 绑定到临时时的生命周期陷阱（见 `pitfalls-ub.md`）。

## 小结
- 容器各有复杂度契约：默认选 `vector`，频繁头尾插入用 `deque`，键查找用 `map`/`unordered_map`，编译期已知小集合用 `array`。
- 优先用 `<algorithm>` 表达意图（如 erase-remove 惯用法避免 O(n²) 的循环逐个 `erase`），并避免对 `map` 重复 `operator[]` 查找造成误插入。
- 已知容量先 `reserve` 防反复扩容，注意 `clear` 不释放容量、字符串拼接优先 `+=`/`ostringstream` 等缓存友好写法。

## 延伸阅读

- C++ Core Guidelines：[SL.containers](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#sl-containers) 系列
- *Effective STL*（Scott Meyers）第 5 章容器选择
- 本备忘录：`./modern-cpp.md`（移动/RAII）、`./performance.md`（缓存友好）、`./pitfalls-ub.md`（迭代器失效）
