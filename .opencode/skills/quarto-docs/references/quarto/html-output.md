# HTML 输出配置

所有 HTML 外观选项都放在 YAML 的 `format: html:` 之下。**本仓库的真实样式实现（行号、提示符配色、文件名条、明暗主题变量）在 `AGENTS.md` 与 `theme/css/` 组件 css 中**，本文件只讲 Quarto 提供的选项与本项目约定，不重复承载样式片段。

> 速查：`toc`/`theme`/`code-fold`/`embed-resources` 都嵌套在 `format: html:` 下 · 单文件用 `embed-resources` · 自包含数学加 `self-contained-math`

## 常用选项

| 选项 | 作用 |
|---|---|
| `toc: true` | 生成目录（TOC）；`toc-depth`、`toc-location`（left/right/body）、`toc-title` 可调 |
| `theme` | 主题：25 个内置 Bootswatch 主题（`cosmo`、`flatly`、`darkly` 等）；明暗双主题 `theme: {light: cosmo, dark: darkly}`；可追加自定义 `.scss`。本书用 `light: [cosmo, theme/scss/theme-light.scss]` + `dark: [darkly, theme/scss/theme-dark.scss]` |
| `grid` | 页面栅格：`sidebar-width` / `body-width` / `margin-width` / `gutter-width`（本书已设具体值，见 `basics.md`） |
| `number-sections` | 章节自动编号（**本书设为 `false`**） |
| `code-copy: true` | 代码块加"复制"按钮 |
| `code-line-numbers: true` | 代码块显示行号；**本仓库不使用行号**（保持简洁），如需要再全局开启 |
| `code-fold: true` | 代码块折叠为可展开的 "Code" 按钮 |
| `code-tools: true` | 文档级 Code 菜单（显示/隐藏全部代码、查看 .qmd 源码） |
| `embed-resources: true` | 生成**单一自包含 HTML**，所有图片/CSS/JS 内嵌（data URI），可单独分享 |
| `self-contained-math: true` | 配合 `embed-resources` 将数学库（MathJax/KaTeX）也内嵌 |
| `html-math-method` | 数学渲染方式：`mathjax`、`katex` 等 |

## 代码块显示

```yaml
format:
  html:
    echo: false        # 隐藏代码只显示输出（可对单个 chunk 用 #| echo: false）
    code-fold: true    # 折叠代码
    code-overflow: wrap # 长行自动换行
```

### 本仓库代码块/终端约定（引用实现）

- 本仓库**不使用行号**：代码块保持简洁；如日后需要，用 `code-line-numbers: true` 全局开启。
- 终端命令块：指令块无提示符、演示块用 `$`（见 `authoring.md`）。
- 上述样式的具体 CSS 实现见 **`theme/css/` 组件 css（按域拆分）**，约定说明见 **`AGENTS.md`**；修改样式应改这两处，而不是在文档里内联。

## embed-resources（重点）

- **`self-contained: true` 已弃用**，请用 `embed-resources: true`（见 `pitfalls.md`）。
- 默认渲染产生 `文档_files/` 依赖目录；`embed-resources: true` 把一切内嵌为单个 `.html`。
- 适合：发邮件、归档、单文件分享。
- 网站/多页面场景建议**不开启**，让各页共享外部资源以利用缓存。
- 含数学时如需离线查看，再加 `self-contained-math: true`。

## 示例：完整文档配置

```yaml
---
title: "C++ 指南"
lang: zh
format:
  html:
    toc: true
    toc-depth: 3
    theme: cosmo
    code-copy: true
    code-fold: false
    embed-resources: true
---
```

## 验证

渲染后检查：

- 单一文件场景：确认没有遗留 `文档_files/` 依赖目录。
- 主题/TOC 不生效：浏览器硬刷新（Ctrl+Shift+R）排除缓存；确认选项嵌套在 `format: html:` 下而非顶层。
- TOC 为空：确认正文使用真实的 `##` 级别 Markdown 标题（加粗文本或 `<h2>` 不会进入 TOC）。
- 本仓库样式（行号/提示符/明暗）异常：检查 `theme/css/` 组件 css 与 `AGENTS.md`，而非本文件。
