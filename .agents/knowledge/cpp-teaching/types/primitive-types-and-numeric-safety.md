---
kb_id: "cpp-primitive-types-numeric-safety-v1"
title: "C++ 基础类型与数值安全"
domain: "cpp-teaching"
subdomain: "types"
tags: [cpp, primitive_types, variables, integer, floating_point, bool, conversion, overflow, undefined_behavior, size_t]
level_range: [0, 4]
dependencies: ["cpp-language-basics-path-v1", "cpp-list-initialization-v1"]
created: "2026-09-19"
updated: "2026-09-30"
chunk_strategy: "semantic_heading"
estimated_tokens: 1600
---

# C++ 基础类型与数值安全

## 类型边界不是固定常数

### 大小、范围与明确宽度

C++ 标准只规定基础整数类型的最小范围，不保证 `int` 永远是 32 位，也不保证 `long` 一定比 `int` 大。`sizeof(T)` 返回 `std::size_t`，表示当前实现中类型占用的字节数；`<limits>` 的 `std::numeric_limits<T>` 用于查询最大值、最小值、有效数字和特殊值。

如果协议、文件格式或网络布局要求固定宽度，使用 `<cstdint>` 中存在的 `std::int32_t`、`std::uint64_t` 等类型，并仍然检查目标平台是否提供该类型。不要用 `sizeof` 的结果推断所有平台上的数值范围。

### `char`、整数文字量与 `size_t`

`char` 是否带符号由实现决定，存字符时不要把它当成固定范围的有符号整数。整数文字量的类型由后缀和候选类型决定；当宽度或符号是接口的一部分时，写出目标类型并检查转换。

`std::size_t` 常用于对象大小和下标，是无符号类型。它与 `int` 混用的风险出在混合比较：负的 `int` 可能先转换成很大的无符号值，比较结果与直觉相反。统一索引类型或先验证非负条件，再进行比较。

## 符号、转换与溢出

### 有符号和无符号

`int`、`long` 等普通整数类型默认有符号；加上 `unsigned` 后只表示非负值。混用有符号和无符号会触发通常算术转换，结果可能改变比较和减法的含义。新手应优先使用清晰的有符号类型，只有确有非负语义且理解边界时才选择无符号类型。

### 溢出和未定义行为

无符号整数运算按模 `2^N` 回绕，这是有定义的行为；有符号整数溢出是未定义行为。数组越界、空指针解引用、读取未初始化变量也属于未定义行为。未定义行为不是“每次随机”，而是编译器可以假设它不会发生，因此优化后的结果可能与直觉完全不同。

### 整数除法与余数

两边都是整数时，`/` 的结果向零截断，`%` 给出余数；`7 / 2` 是 `3`。整数除以零是未定义行为，不能把它和浮点除零的 `inf` 或 `nan` 混为一谈。

### 隐式与显式转换

`int` 转 `double`、`double` 转 `int`、有符号转无符号都可能隐式发生。需要表达转换意图时使用 `static_cast<T>(value)`。浮点转整数会截断小数，大整数转小整数可能丢失高位或改变符号；先检查范围，再决定是否转换。避免 `(int)value` 这类 C 风格强转，它隐藏了转换类别。

## 浮点数与布尔值

### 浮点精度、NaN 与无穷大

二进制浮点数通常不能精确表示十进制小数，因此 `0.1 + 0.2` 不应直接与 `0.3` 用 `==` 比较。比较计算结果时使用与量纲和误差预算匹配的容差，例如 `std::abs(a - b) < 1e-9`，并单独处理 `NaN` 与无穷大。浮点除以零可能产生 `inf` 或 `nan`；整数除以零是未定义行为。

### `bool` 的转换与输出

整数 `0` 转为 `false`，非 `0` 转为 `true`。流默认把 `bool` 输出为 `0` 或 `1`；需要可读文本时先写 `std::boolalpha`。不要把 `bool` 当成承载多个状态的整数，多个互斥状态应在后续章节使用更合适的类型表达。

## 基础类型的教学取舍

金额优先保存为最小货币单位的整数，例如“分”，避免二进制浮点舍入进入结算核心。折扣率、比例和物理量可以使用 `double`，但必须说明误差和比较策略。类型安全的目标不是消灭所有转换，而是让范围、单位、符号和精度成为可检查的设计信息。

## 两仓工程代码的定宽整型约定

姊妹仓库 cpp-board-games 的工程代码有一条比本文件更严的约定，按角色分层：

| 角色 | 类型 | 理由 |
| --- | --- | --- |
| 领域坐标与尺寸（`kRows` / `kCols`、`Position::row` / `col`、循环下标） | `std::int32_t` | 参与有符号边界判定，与坐标同一有符号族 |
| 容器长度与下标（`kCellCount`、`std::array` 长度、`CellIndex` 返回值） | `std::size_t` | 容器 / NTTP 侧，与 STL 一致 |
| 封闭状态码枚举底层 | `std::uint8_t` | 唯一的小无符号用途：取值集合与布局，不是算术尺寸 |

选型按场景论证：边界判定要能表达越界输入（如负坐标），有符号类型才表达得了，也避开 `size_t` 与负数比较的隐式转换陷阱；否决更小无符号（`uint8_t` / `uint16_t` 作坐标）——负坐标无法表达、与 `int` / `size_t` 混算触发整数提升、省字节收益为零；不用裸 `int` 是为跨平台宽度可预测。依据与偏离说明见姊妹仓库标识 `bg-google-cpp-style-v1` 的知识文件「整型与枚举底层类型」；notes 教学示例正文仍按本章讲解 `int` 的范围与转换语义，练习代码触及工程边界时跟随该约定。

### 有符号乘法进入容器前的隐式拓宽

有符号领域的乘法在 `std::int32_t` 完成后才隐式拓宽为 `std::size_t`，`3 * 3` 这类不会溢出的乘法同样会触发 `bugprone-implicit-widening-of-multiplication-result` 报警。正反例：

```text
不佳（int32 乘积先算完，再隐式拓宽成数组长度）：
std::array<Mark, kRows * kCols> cells_;

改写（操作数先显式拓宽，乘法直接在 size_t 完成）：
inline constexpr std::size_t kCellCount =
    static_cast<std::size_t>(kRows) * static_cast<std::size_t>(kCols);
std::array<Mark, kCellCount> cells_;
```

下标换算同理：工程代码提供 `CellIndex(Position)` 返回 `std::size_t`，函数内先 `static_cast<std::size_t>` 各操作数再乘加；不关闭该检查，也不把领域坐标改成 `size_t`。
