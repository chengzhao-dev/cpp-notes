# 文档内容写作

本文件讲**内容怎么写**：代码块、终端命令、callout、表格、图表、交叉引用。中文措辞、术语、文风见 `../zh/writing-style.md`；项目结构与标题见 `basics.md`；样式实现（行号、明暗主题、callout 配色）见 `AGENTS.md` 与 `theme/css/` 组件 css。

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

## 章节横线（---）

每个 `##`（H2）/ `###`（H3）标题前，在 qmd 源里写一条 `---` 水平线（上下各空一行），形成 opencode 风格的分节。章节分隔由这条线承担，**标题本身不要再加下边框**（旧 `border-bottom` 已移除，由 CSS 处理）。首页 `index.qmd` 与 part 索引页（含 `.hero-eyebrow`）不写 `---`。

```markdown
## 第一个小节

正文……

---

## 第二个小节
```

- `---` 必须前后各空一行：若前一段与 `---` 之间没有空行，Pandoc 会把前一段解析成 setext 二级标题（见 `pitfalls.md` 第 11 条），导致结构错乱。
- `---` 是 Markdown 主题分隔线（thematic break），渲染为 `<hr>`；本仓库 CSS 把它做成每个小节标题前的细线（上方 3.375rem 留白）。

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

## 图表

**图表围栏必须加大括号**（`mermaid` / `dot` 是 Quarto 内置图表引擎，必须用可执行 cell 写法）。
mermaid 块首行还要加 `%%{init}%%` 指令：

- `fontFamily` 与站点 `--ui-font` 同序但**裸写不带引号**——带单引号会被 mermaid 指令解析器整条丢弃（已实测）；
  不写则按默认 trebuchet 测量、页面按 Inter/思源渲染，节点文字会折行并压到框底。
- `flowchart.wrappingWidth: 320` 让约 18 个汉字内的节点文案保持单行：

````markdown
```{mermaid}
%%{init: {"fontFamily": "Inter, Noto Sans SC, Microsoft YaHei, sans-serif", "flowchart": {"wrappingWidth": 320}}}%%
flowchart TD
  A[装好 WSL2] --> B[安装工具链]
```
````

（本仓库完整字体栈以 `theme/css/tokens.css` 的 `--ui-font` 为准去引号使用；`theme/css/mermaid.css` 的「排版守卫」段已把页面断行规则挡在 SVG 外，与该指令配套。）

带题注的 Markdown 图：

```markdown
![题注文本](images/架构图.png){#fig-arch}
参见 @fig-arch。
```

## 表格

```markdown
| 列1 | 列2 |
|-----|-----|
| 数据 | 数据 |

: 表题注。{#tbl-example}
```

引用：`参见 @tbl-example`。

默认各列等宽：Pandoc 按分隔行横杠生成等宽 `<colgroup>`，浏览器的内容自适应被其覆盖。需要侧重某列时，把分隔行横杠写成大致比例（横杠数量比 ≈ 列宽比，只影响当前表格，逐表手动设置）：

```markdown
| 适用状态 | 命令 | 作用 |
|:----|:--------|:---------|
```

上例约 19% / 38% / 43%。

## Callout 提示框

七类：`note`、`tip`、`warning`、`important`、`caution`、`best-practice`、`key-insight`（后两类为命名 callout）。

```markdown
::: {.callout-best-practice}
## 最佳实践
永远初始化变量。
:::

::: {.callout-key-insight}
## 关键洞察
现代 C++ 的核心心智模型是「把靠纪律保证的事，变成靠类型和编译器保证」。
:::
```

- **最佳实践**（绿）：给出「应该这样做」的规则。
- **关键洞察**（金）：点出核心心智模型，帮助理解而非死记。
- 简短提醒用 `>` 引用块而非 callout，首句以「注意：」起头：

```markdown
> 注意：`wsl --import` 不会保留原来的普通用户，首次进入会以 `root` 登录。
```

  - 自定义「验证结果」块 `.callout-verify`（绿色 ✓，标注「通过/已验证」语义）为预留组件（当前内容未使用），按需启用。
  - 所有 callout 渲染为 opencode aside 风：**无边框、无左侧色条、无圆角**，仅彩色低饱和底 + 加粗小标题（标题 uppercase，中文无影响）+ 略小正文；视觉规范见 `AGENTS.md` 与 `theme/css/` 组件 css。

## 交叉引用

```markdown
## 章节 {#sec-intro}
见 @sec-intro；图 @fig-plot；表 @tbl-data。
```

## Divs 与 Spans

```markdown
::: {.callout-tip .content-box}
自定义 div 内容。
:::

这是[重要文本]{.highlight}。
```

## 标题命名（面向新手）

标题要让人一眼看懂在做什么：优先用「目标/结果」式表述（「迁移 WSL 系统到其他磁盘」），避免堆砌操作动作（「导出备份与导入迁移」）。命名前先问：读者只看标题，能否知道这一节要解决什么问题？
