# STL 要点

> 容器 · 迭代器 · 算法 · 下标与 at

## 容器选型

先从使用场景和所有权需求开始，再比较容器。每个容器至少说明访问复杂度、迭代器失效和适合的替代方案。不要只按字母罗列 API。

| 容器 | 场景 |
|---|---|
| `vector` | 默认动态数组，随机访问 |
| `array` | 固定大小栈数组 |
| `map`/`set` | 有序关联 |
| `unordered_map`/`unordered_set` | 哈希，均摊 O(1) |

## 下标与 at（共性章）

- 族 A（`array` / `vector` / `deque` / `string` / `string_view`）：`[]` 不检查（越界 UB），`at` 检查并抛 `std::out_of_range`。正文只演示 `std::array`，清单点名同类。依据见 `cpp-subscript-and-at-v1`。
- 族 B（`map` / `unordered_map`）：`[]` 缺键则插入；`at` 缺键则抛。不要写成与族 A「同一套不安全」。
- `span`（C++20）：本仓不以 `at` 为前提；C++26 才标准化 `span::at`。
- 异常文案见 `cpp-exception-message-format-v1`。

## 迭代器

- 半开区间 `[begin, end)`。`cbegin`/`cend` 只读。
- 失效规则：向 `vector` 插入可能使全部迭代器失效。

## 算法

- `<algorithm>`：`sort`、`find`、`transform`、`accumulate`。
- 优先算法 + 迭代器，少手写循环。

## 章节落点

- `content/standard-library/overview.qmd` 总览
- `content/standard-library/subscript-and-at.qmd` 下标与 at 共性
- 其后 `vector`、`map-set`、`iterators`、`algorithms`
