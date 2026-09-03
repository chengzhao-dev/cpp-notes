# C++ 写作约定入口

> 速查：示例 `-std=c++20 -Wall -Wextra` · 完整代码带 `int main` · 片段标 `// 片段` · 文件/目录纯 ASCII

## 术语速查

| 英文 | 中文 |
|---|---|
| RAII | 资源获取即初始化 |
| UB | 未定义行为 |
| lvalue / rvalue | 左值 / 右值 |
| NRVO | 命名返回值优化 |

## 章节写法节奏

动机 + 规则 → 正确/错误对照 → 常见误区 → FAQ（≤2–3 条）。

## 内容参考依据

| 来源 | 用作 |
|---|---|
| C++ Primer (5th ed.) | 主线讲解顺序与术语 |
| learncpp.com | 章节拆分粒度、渐进式披露 |
| zh.cppreference.com | 译名、标准措辞、复杂度（`## 深入` 引标准时以此为准） |
| CMake 官方文档 | 构建章节的 command/variable 语义与注释措辞 |
| Google C++ Style Guide | 命名与排版；**例外：本仓库启用异常**，不用「不使用异常」条款 |

## Callout（只用内置类型）

`{.callout-tip}` + `## 最佳实践` · `{.callout-warning}` + `## 关键洞察` · `{.callout-important}` + `## 深入`（大师向，章末）。自定义 `.callout-*` 类会被 Quarto 静默丢弃，见 `quarto-docs` 的 `pitfalls.md` #12。

## 核心主题索引

| 主题 | 参考 |
|---|---|
| 变量、类型、函数、类 | 本文件 + core 章节任务 |
| 现代 C++（RAII/移动/智能指针） | `modern-cpp.md` |
| STL | `stl.md` |
| 模板 | `templates.md` |
| 性能 | `performance.md` |
| UB 与陷阱 | `pitfalls-ub.md` |
| 构建 | `toolchain.md` |
| 工程实践 | `engineering.md` |

## 示例约定

- 源码：`code/<part>/<name>.cpp`，与 `content/<part>/` 对齐。
- 新建工程：`python scripts/cpp/init_project.py --name <name> --dir code/<part>`。
- 校验：`python .cursor/skills/cpp-content/scripts/verify_examples.py`。

## 命名

文件/目录纯 ASCII，连字符用 `-`（U+002D）。C++ 标识符见 `code-style.md`。
