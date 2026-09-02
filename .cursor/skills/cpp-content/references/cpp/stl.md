# STL 要点

> 容器 · 迭代器 · 算法

## 容器选型

| 容器 | 场景 |
|---|---|
| `vector` | 默认动态数组，随机访问 |
| `array` | 固定大小栈数组 |
| `map`/`set` | 有序关联 |
| `unordered_map`/`unordered_set` | 哈希，均摊 O(1) |

## 迭代器

- 半开区间 `[begin, end)`；`cbegin`/`cend` 只读。
- 失效规则：向 `vector` 插入可能使全部迭代器失效。

## 算法

- `<algorithm>`：`sort`、`find`、`transform`、`accumulate`。
- 优先算法 + 迭代器，少手写循环。

## 章节落点

- `content/stl/intro-stl.qmd` 起逐章展开
