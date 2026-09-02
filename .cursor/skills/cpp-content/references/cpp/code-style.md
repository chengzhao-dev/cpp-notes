# C++ 代码风格

> LLVM 排版 · Google 命名 · 异常启用 · 见 `scripts/cpp/templates/`

## 命名

| 实体 | 规则 | 示例 |
|---|---|---|
| 类型/函数 | 大驼峰 | `HttpRequest`、`AddEntry()` |
| 变量/参数 | snake_case | `entry_count` |
| 类私有成员 | snake_case + `_` | `width_` |
| 常量 | `k` + 大驼峰 | `kMaxRetries` |
| 文件 | snake_case.cpp | `url_table.cpp` |

## 工具

```bash
python .cursor/skills/cpp-content/scripts/verify_examples.py
python .cursor/skills/cpp-content/scripts/verify_examples.py --style
```

clang 配置由 `scripts/cpp/init_project.py` 复制到工程根。

## 示例

- `code/<part>/<name>.cpp`，`-std=c++20 -Wall -Wextra`
- 完整示例带 `int main`；片段首行 `// 片段`
- ≤40 行/块；中文注释，标识符 ASCII

## 异常

默认启用；构造失败抛异常；可预期失败用 `optional`/`expected`；资源靠 RAII。
