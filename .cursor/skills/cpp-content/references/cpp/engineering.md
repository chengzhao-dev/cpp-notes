# 工程实践

> 项目布局 · 错误处理 · 测试

## 工程讲解顺序

工程章节按“源码 → 构建目标 → 构建规则 → 构建命令 → 生成结果 → 验证”展开。先让读者看到一个可运行目标，再逐步引入目录、库、测试和安装等组织方式。

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
