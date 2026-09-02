# 性能优化要点

> 先测量再优化 · 局部性 · 移动/RVO

## 原则

- Profile 找热点；避免过早优化。
- 算法复杂度优先于微优化。

## 常见手段

| 手段 | 说明 |
|---|---|
| 缓存局部性 | 顺序访问、SoA vs AoS |
| 移动/RVO | 减少拷贝 |
| `reserve` | 预知大小时预分配 |
| 避免虚函数热点内联失败 | 视场景用 CRTP/模板 |

## 章节落点

- `content/performance/profiling.qmd`、`cache-locality.qmd`、`rvo-nrvo.qmd`
