# C++ 代码风格

> LLVM 排版 · Google 命名 · C++20 · 2 空格缩进 · 配置源见 `.config/cpp/`

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

clang 配置源位于 `.config/cpp/`，由 `scripts/cpp/init_project.py` 复制到独立工程根目录。

Windows 下的编译校验会自动通过 WSL2 执行。日常修改后运行一次 `python scripts/agent/run.py verify`；单章节构建使用 `python scripts/agent/run.py build <part>/<chapter>`。默认只输出结论，失败时再追加 `--verbose` 查看诊断，避免无意义地展开完整编译日志。

## 示例

- `code/<part>/<name>.cpp` 使用 `-std=c++20 -Wall -Wextra`。
- 完整示例带 `int main`；片段首行使用 `// 片段` 标明。
- 每个代码块不超过 40 行，标识符使用 ASCII。

教程代码先展示能运行的最小版本，再按一个变化点逐步扩展。每次扩展都说明行为变化和验证方式，不把最终工程一次性倾倒给初学者。

## 重要代码行的注释

注释只说明当前代码块的学习重点。不要引入正文尚未出现的比较对象，也不要解释本节没有展开的语言原理；如果代码块只用于展示操作，使用简短的中性注释即可。

注释服务于本节的学习目标，不是逐行翻译代码。某个标识符、语句或配置第一次出现且需要读者记住时，在对应代码行正上方使用语言原生注释；背景代码不重复注释，复杂原理放在代码块外的正文中。

第一次展示 `CMakeLists.txt` 或 Shell 脚本时，为版本要求、目标、输出目录和脚本控制语句提供足够的职责注释。`set -euo pipefail` 等组合选项要用简短准确的注释说明停止条件；后续示例不重复相同解释。

- 第一个 C++ 程序可注释 `#include <iostream>`、`main` 和 `std::cout`。
- 讲 `vector` 时只注释 `std::vector`、元素访问和迭代器等 vector 重点，不重复注释 `iostream` 或 `std::cout`。
- CMake 命令和变量优先采用 CMake 官方中文文档术语；C++ 语言和标准库优先参考主流中文教材与 [cppreference 中文站](https://zh.cppreference.com/)。

代码块只承担一个主要学习目标。多行原理说明移到正文，注释放在被说明代码的上一行，不使用行尾长注释；讲解同一概念的后续示例应减少重复注释。C++、CMake、Shell 和配置文件统一使用 2 空格缩进，逻辑块之间保留一个空行。CMake 和 Shell 的命令说明也遵循这一规则，先在正文说明目的，再给出干净、可复制的代码块。

代码和终端输出左对齐，保留必要缩进；字段名与说明的对齐交给表格。Shell、CMake 和 C++ 示例禁止把长解释写成行尾注释。中文说明使用完整句子，代码语法中的冒号不受正文标点规则影响。

网页中的 C++、CMake 和 Shell 代码统一使用 Quarto 的 GitHub Light / GitHub Dark 高亮。代码块中的括号、标点和普通文本不手工指定颜色；不要用位置选择器或命令名选择器修补高亮器产生的局部颜色。

## 异常

默认启用异常；构造失败抛异常；可预期失败用 `optional`/`expected`；资源靠 RAII。
