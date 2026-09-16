# C++ 代码风格

> Google 排版与 include 顺序 · 项目小驼峰命名 · C++20 · 2 空格缩进
> 配置源见 `.agents/skills/cpp-content/assets/config/`

## 命名

| 实体 | 规则 | 示例 |
|---|---|---|
| 类型 | 大驼峰 | `HttpRequest`、`UrlTable` |
| 函数/方法 | 小驼峰 | `addEntry()`、`makeGreeting()` |
| 变量/参数/成员 | 小驼峰 | `entryCount`、`maxRetries` |
| 类私有成员 | 小驼峰 + `_` | `width_`、`entryCount_` |
| 常量 | `k` + 大驼峰 | `kMaxRetries` |
| 命名空间 | `lower_case` | `url_table` |
| C++ 文件 | snake_case | `url_table.cpp` |

这套命名以 Google C++ Style Guide 的结构和常量约定为底，只把函数、变量、参数和成员改为
Qt、WebKit 常用的小驼峰。Google 原规则对函数使用大驼峰，对变量和成员使用 snake_case。
这里不把两种规则混写成“Google 默认小驼峰”。命名依据见标识 `cpp-naming-format-v1`。

## Include 顺序

源文件按下面的顺序包含头文件，各组之间保留一个空行，组内按字母排序：

1. 对应实现文件自身的头文件。
2. C 系统头文件。
3. C++ 标准库头文件。
4. 其他库头文件。
5. 本项目头文件。

`BasedOnStyle: Google` 负责排序和分组。项目保留 `.cpp`、`.h`、`#pragma once` 和异常，
不跟随 Google 的 `.cc`、include guard 和禁用异常规则。

源文件直接使用某个标准库类型时，必须包含对应头文件，不能依赖其他头文件的传递包含。
实现文件包含自身接口后，仍应直接包含它使用的标准库头文件。

## 工具

正文中的工具名、命令、参数、路径和标识符按 `quarto-docs` 的行内代码规则统一标记。不要只给部分工具加反引号。

编译并运行完整 C++ 示例：

```bash
# 校验 code/ 下全部 C++ 示例
& .agents/skills/agent-ops/scripts/run.ps1 verify
```

检查 C++ 格式：

```bash
# 追加 clang-format 与 clang-tidy 检查
& .agents/skills/agent-ops/scripts/run.ps1 verify --style
```

clang 配置源位于 `.agents/skills/cpp-content/assets/config/`，由 `.agents/skills/python-tools/scripts/scaffold/init_project.py` 复制到独立工程根目录。
`single` 与 `multi` 工程模板位于 `.agents/skills/cpp-content/templates/projects/`，示例工程应与模板结构保持一致。

Windows 下的编译校验会自动通过 WSL2 执行。日常修改后运行一次 `& .agents/skills/agent-ops/scripts/run.ps1 verify`。单章节构建使用 `& .agents/skills/agent-ops/scripts/run.ps1 build <part>/<chapter>`。默认只输出结论，失败时再追加 `--verbose` 查看诊断，避免无意义地展开完整编译日志。

## 示例

- `code/<part>/<name>.cpp` 使用 `-std=c++20 -Wall -Wextra`。
- 完整示例带 `int main`。片段首行使用 `// 片段` 标明。
- 每个代码块不超过 40 行，标识符使用 ASCII。

教程代码先展示能运行的最小版本，再按一个变化点逐步扩展。每次扩展都说明行为变化和验证方式，不把最终工程一次性倾倒给初学者。

## 源码注释合同

`code/**` 与 `cpp-content/templates/projects/**` 中的完整 `.h`、`.cpp`、`.sh` 和
`CMakeLists.txt` 使用“用途 + 重点”注释。首个有效行必须用语言原生注释说明文件职责。
Shell 首行是 shebang 时，用途注释紧随其后。文件要能脱离正文独立读懂，但不逐行翻译代码。

- C++ 头文件先说明接口职责。实现文件先说明它实现哪项声明。程序入口先说明程序做什么。
- C++ 只为接口契约、实现关系、首次出现的语言重点或非显然行为增加注释。不要重复注释
  `#include`、`main`、赋值和 `return`，也不要在文件用途注释之外再逐行解释入口。
- CMake 首行说明当前文件要构建的目标。顶层文件写工程组成，库子目录文件只写库自身。编译数据库注释说明生成的文件和实际用途，源文件收集注释说明收集范围与新增文件后的结果。每条注释只表达一个动作或因果关系，不把独立事实拼成两句。
- 每个 `add_executable()` 和 `add_library()` 前必须有一条独立注释说明目标职责。目标创建是工程结构边界，不因命令名直观而省略；后续选项仍按学习重点决定是否注释。
- Shell 首行说明脚本用途，并为 `set -euo pipefail` 等停止条件写短注释。
- 讲 `vector` 时只注释 `std::vector`、元素访问和迭代器等当前学习重点，不重复解释
  `iostream` 或 `std::cout`。CMake 命令和变量优先采用 CMake 官方中文文档术语。

inline `cpp`、`bash`、`powershell` 和 `cmake` 代码块仍按 `quarto-docs` 的
`terminal-validation.md` 控制总注释与子注释，不为满足文件合同机械增加注释。
`{{< include /code/... >}}` 引用的真实文件则按本节的独立阅读标准维护。注释只解释学习重点，
不引入正文尚未出现的比较对象。复杂原理、参数边界和背景放到正文或标识
`cpp-teaching-source-comments-v1` 的知识文件。

代码和终端输出左对齐，保留必要缩进，字段名与说明的对齐交给表格。Shell、CMake 和 C++ 示例禁止把长解释写成行尾注释。中文说明使用完整句子，代码语法中的标点不受正文标点规则影响。

网页中的 C++、CMake 和 Shell 代码统一使用 Quarto 的 GitHub Light / GitHub Dark 高亮。代码块中的括号、标点和普通文本不手工指定颜色。不要用位置选择器或命令名选择器修补高亮器产生的局部颜色。

## 异常

默认启用异常。构造失败抛异常。可预期失败用 `optional`/`expected`。资源靠 RAII。
