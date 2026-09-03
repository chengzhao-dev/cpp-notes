# 文档元素：图表 · 表格 · Callout · FAQ · 交叉引用

> **何时读我**：章里要放 mermaid 图、表格、Callout 提示框、FAQ 或小节交叉引用时。
> **读我之前不需要读别的**。正文结构与代码块约定见同目录 `authoring.md`。

## 图表

**图表围栏必须加大括号**。mermaid 字体由 `theme/css/mermaid.css` 控制，块内不必写超长 `%%{init}%%`：

````markdown
```{mermaid}
flowchart TD
  A[步骤一] --> B[步骤二]
```
````

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

**只能用 Quarto 内置的 5 类**：`note`、`tip`、`warning`、`important`、`caution`。

> 注意：Quarto 不识别自定义 callout 类。写 `::: {.callout-best-practice}` 时，该未知类会被**静默丢弃**，整块退化成一个带 `<h2>` 的普通 `<section>`：既没有提示框样式，又会混进右侧目录。附加在其他类上的 `.callout-*` 同样被丢弃。

本仓库的三层读者语义，用「内置类型 + 显式 `## 中文标题`」表达：

| 语义层 | 写法 | 外观 | 给谁 |
|---|---|---|---|
| 补充说明 | `::: {.callout-note}` + 默认标题「注意」 | 蓝 | 新人 |
| **最佳实践** | `::: {.callout-tip}` + `## 最佳实践` | 绿 | 学过但不深：给出「应该这样做」的规则 |
| **关键洞察** | `::: {.callout-warning}` + `## 关键洞察` | 金 | 学过但不深：点出核心心智模型 |
| **深入** | `::: {.callout-important}` + `## 深入` | 紫 | 大师：标准措辞、复杂度、优化器与 ABI 行为、corner case、旧标准差异 |
| 危险写法 | `::: {.callout-caution}` + 默认标题「危险」 | 红 | 所有人：会造成 UB / 数据竞争的代码 |

```markdown
::: {.callout-tip}
## 最佳实践
永远初始化变量。
:::

::: {.callout-warning}
## 关键洞察
现代 C++ 的核心心智模型是「把靠纪律保证的事，变成靠类型和编译器保证」。
:::

::: {.callout-important}
## 深入
`CMAKE_CXX_STANDARD 20` 默认生成 `-std=gnu++20`；需严格贴合 ISO 时设 `CMAKE_CXX_EXTENSIONS OFF`。
:::
```

标题必须写在块内首行 `## …`（Quarto 取首个标题作 callout 标题）。简短提醒用 `>` 引用块而非 callout，首句以「注意：」起头：

```markdown
> 注意：`wsl --import` 不会保留原来的普通用户，首次进入会以 `root` 登录。
```

  - 所有 callout 渲染为 docs 左条风：**左 3px 色条 + 浅底 + 小圆角**；视觉规范见 `quarto-theme` skill 与 `theme/css/callouts.css`。
  - 渲染后自检：`python .cursor/skills/quarto-docs/scripts/check_callouts.py`（先 `quarto render`），抓退化 callout 与非内置类型。

## 常见问题（FAQ）

章末 `## 常见问题` 用 `###` 症状/报错作标题（≤3 条），每条内给**编号排查步骤**，结尾给一句**验证判据**（「排查完成后运行 X，看到 Y 即成功」）。完整可套用的示例见 `../zh/cases/caution-faq.md`。

```markdown
## 常见问题

### g++: command not found

1. 确认编译器已装：`g++ --version`。
2. 若未安装，回到环境章重装 `build-essential`。

装好后再跑 `g++ --version`，能看到版本号即成功。
```

不要写成「`**问题？** 答案一句」的加粗内联段——那会丢失层级、难以扫读。

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
