# 工程实践

> 项目布局 · 错误处理 · 测试

## 项目布局

```
project/
├── CMakeLists.txt
├── src/
├── include/
└── tests/   # 进阶
```

## 错误处理

- 构造函数失败 → 异常；可预期失败 → `optional`/`expected`。
- 资源管理靠 RAII，见 `modern-cpp.md`。

## CMake 现代写法

- target-based：`target_link_libraries`、`target_compile_features`。
- 见 `toolchain.md` 与 `content/toolchain/` 章节。

## 章节落点

- `content/toolchain/cmake-targets.qmd`、`project-layout.qmd`
