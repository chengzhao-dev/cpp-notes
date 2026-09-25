# 性能与陷阱

## 性能优化要点

> 先测量再优化 · 局部性 · 移动/RVO

### 原则

- Profile 找热点。避免过早优化。
- 算法复杂度优先于微优化。

性能章节按“可测量的目标 → 基线 → 瓶颈假设 → 最小改动 → 再测量”推进。每个优化都说明收益、代价和适用边界。

### 常见手段

| 手段 | 说明 |
|---|---|
| 缓存局部性 | 顺序访问、SoA vs AoS |
| 移动/RVO | 减少拷贝 |
| `reserve` | 预知大小时预分配 |
| 避免虚函数热点内联失败 | 视场景用 CRTP/模板 |

### 章节落点

- `content/performance/profiling.qmd`、`cache-locality.qmd`、`rvo-nrvo.qmd`

## 陷阱与未定义行为
> UB · 生命周期 · 常见 bug

### UB 典型来源

- 越界访问、use-after-free、数据竞争。
- 有符号整数溢出、错误 `reinterpret_cast`。

### 调试向

- `-fsanitize=address,undefined`（ASan/UBSan）。
- `-Wall -Wextra` 作基线。`-Werror` 可选。

排错先复现，再缩小范围，最后解释根因。不要只列出 UB 名称。示例应说明触发条件、可观察结果和最短验证办法。

### 常见误区

- 返回局部变量引用。
- `vector` 扩容后仍用旧指针/迭代器。
- 多线程无同步写共享数据。

### 章节落点

- `content/debugging/common-bugs.qmd`、`sanitizers.qmd`
