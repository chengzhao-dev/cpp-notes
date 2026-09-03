# 文档内容写作

> **何时读我**：写或改任何 `.qmd` 的正文结构、代码块、终端命令块时。
> **读我之前不需要读别的**。页面元素（图表 / 表格 / Callout / FAQ / 交叉引用）
> 见同目录 `authoring-elements.md`。

本文件讲**内容怎么写**：正文结构、代码块、终端命令。
图表 / 表格 / Callout / FAQ / 交叉引用见同目录 `authoring-elements.md`。中文见 `../zh/writing-style-core.md`；结构见 `basics.md`。

> 速查：`title:` 提供标题、不写 `# H1` · 代码块标 `cpp` · 终端全站 `$` · callout 七类 · 交叉引用 `@sec-/@tbl-/@fig-`

## 章节标题与开篇

- 章节标题由 YAML `title:` 提供，**不要**再写同文本 `# H1`（见 `basics.md`）。
- 页面内小节从 `##`（H2）开始。
- 普通章节**不要写** `description:`（仅 `index.qmd` 封面可见）；开篇可见引言写**正文普通段落**（不套引用块/特殊样式），动机 + 目标 1–3 句，不预演小节：

```markdown
---
title: "章节标题"
---

欢迎！这一章我们一起来……（动机 + 目标，1–3 句正文段落）。

## 第一个小节
```

章节分隔使用 **Quarto/Bootstrap 默认的 h2 下边框**，qmd 源里**不要**在小节前写 `---` 水平线。

## 代码块

普通语言围栏，**不要加大括号 `{…}`**（`cpp` / `powershell` / `bash` 都不是 Quarto 执行引擎，写成 `{.cpp}` / `{cpp}` 会被当可执行 cell 而渲染异常）。文件名/说明写在代码块上方的正文段落。

````markdown
这段代码用 `std::vector` 存三个整数并依次打印：

```cpp
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v{1, 2, 3};
    for (int x : v) std::cout << x << "\n";
}
```
````

- 示例必须是**可编译/可运行的完整片段**（或显式标注「片段」），统一 `-std=c++20 -Wall -Wextra`。
- 每块代码上方用一句中文说明它做什么。

### 配置文件代码块（CMake 等）

`CMakeLists.txt`、`*.yml`、`Dockerfile` 等**声明式/配置型**文件，逐行说明直接写在代码块**内部**用其原生注释符（CMake 用 `#`），且注释写在**对应行上方独立一行**（`# 说明` 换行 `语句`），不在代码块下方用 bullets 逐行解释。CMake 注释的措辞以官方中文文档为准（参考 `https://cmake.com.cn/cmake/help/latest` 下对应 command / variable 页面），平实中性、不渲染警示语气。若展示仓库中真实存在的文件（如 `code/` 下的示例），优先用 `{{< include /code/.../file >}}` 引用真实文件，保证文档与代码库唯一来源、永不失配；上面注释约定仍然适用。

````markdown
下面是与上面等价的最小 `CMakeLists.txt`：

```cmake
# 要求的最低 CMake 版本；低于 3.31 直接报错，保证所有人行为一致
cmake_minimum_required(VERSION 3.31)

# 项目名 app，语言用 C++
project(app LANGUAGES CXX)

# 默认按 C++20 标准构建
set(CMAKE_CXX_STANDARD 20)
# 强制必须支持 C++20，编译器不支持就报错（而不是悄悄降级）
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 固定把可执行文件输出到 build/bin/（和一键脚本约定一致，方便直接用）
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# 用 first-program.cpp 生成名为 app 的可执行文件
add_executable(app first-program.cpp)
```
````

理由：这类文件的「说明」本身就是配置语义，放块内更贴近读者视线、与仓库 C++ 参考（`cpp-content` 的 `toolchain.md`）及 bash 约定保持一致；块下 bullets 既重复又割裂。注释只讲该行为什么存在，不延伸长篇原理。

## 终端命令约定

**指令块（只给要敲的命令）**：不加 `$` / `PS>` 前缀，保证复制按钮只复制纯命令；多行命令每行一条、命令之间空一行；shell 由语言围栏 + 上方正文说明标明。

```markdown
在 PowerShell（管理员）中执行：

```powershell
wsl --shutdown

wsl --export Ubuntu "D:\ProgramData\WSL\ubuntu-backup.tar"

wsl --unregister Ubuntu
```
```

**演示块（命令 + 预期输出）**：统一用 `$` 作为唯一提示符，`$` 后跟命令、输出紧跟其后，与命令同块；PowerShell 与 Bash 演示块均用 `$`（全站只有 `$` 一种提示符，不出现 `PS>`）。

```markdown
装好后用 `wsl --status` 确认默认分发与版本：

```powershell
$ wsl --status
默认分发: Ubuntu
默认版本: 2
```
```

- **查看类命令**（`--version`、`--status` 等只读查看）默认逐条独立展示，并在附近正文说明看输出里的哪些字段。
- **性质相近的命令合并演示块**：同一主题、性质相近的多条命令（如多个 `--version` 验证、多条状态查询）可合并到一个演示块，每条命令上方用 `#` 注释标明身份或作用（如 `# g++：编译器版本`），命令对之间空一行；正文只负责介绍（判据 + 挑代表演示），不为每条命令单独铺正文或分块：

```bash
# g++：编译器版本
$ g++ --version
g++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0

# cmake：构建系统版本
$ cmake --version
cmake version 4.2.3
```

- **多命令操作块**（安装/迁移/构建序列）只在「连续操作步骤」时同块；命令间空一行。
- **场景共用代码块**：同一主题的两个使用场景可合用一个代码块，用 `#` 注释区分场景（如「一步迁移」与「重装后指定位置」），正文一段带出两个场景，不再分写两段。
- 需要逐条说明时，在每条指令上方用 shell 注释符（`#`）加一句中文说明作用；只对易误解/关键/顺序敏感的指令加注释。
- **多包安装逐包注释**：一条命令装多个包时，每个包在命令上方用一行 `# 包名：核心用途` 注释，只讲核心用途不延伸细节，代码块后不再用 bullet 逐包解释。
- 不写 `title=`、不用 `.console` div、不手写 `PS>`——文件名/环境名用正文段落说明。
