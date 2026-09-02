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
