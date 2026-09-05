---
name: quarto-theme
description: Quarto Book HTML 主题与设计系统。涉及 theme/scss、theme/css、includes、设计令牌、布局校验时使用。默认中文。
---

# Skill: quarto-theme

明暗双主题采用 GitHub Light / GitHub Dark 色板，保留适合教程阅读的三栏布局。

## 任务路由

| 任务 ID | 可写 |
|---|---|
| TASK-THEME-001 | `tokens.css`、`theme/scss/*` |
| TASK-THEME-002 | `nav.css`、`sidebar.css` |
| TASK-THEME-003 | `content.css`、`code.css` |
| TASK-THEME-004 | `callouts.css`、`landing.css` |
| TASK-THEME-005 | `mermaid.css`、`includes/` |
| TASK-THEME-006 | 跑 `run.py check` |

必读：`references/design-tokens.md` + **目标那一个** css 文件（不要通读整个 `theme/css/`）。
改样式的代价与流程见 `handbook/operations/agent-operations.md`（会触发整本重渲染）。

## 已固化的产物契约

`scripts/agent/check_dom_contracts.py` 断言：复制按钮 hover 作用域必须是 `.code-copy-outer-scaffold`
（Quarto 1.10 起按钮与 `div.sourceCode` 是兄弟）；`@media print` 不得隐藏 scaffold 本身；
触屏 `@media (hover: none)` 兜底；favicon 注入与发布；Mermaid 必须输出 SVG 而不是源码块。改 DOM 相关样式前后都跑一次。

## 代码高亮约定

- 亮色使用 `github-light`，暗色使用 `github-dark`，配置唯一来源是 `_quarto.yml`。
- 语义颜色由 Pandoc/Quarto 的 token 提供，CSS 只负责背景、布局、字体和稳定的基础色。
- 不按字符内容、DOM 位置或 Bash/PowerShell 命令名覆盖颜色；括号、标点、`$`、版本号和普通输出必须保持连续的基础色。
- `text` 代码块用于命令输出和纯文本演示，不启用语言高亮，但必须与 `cpp`、`cmake`、`bash` 和 `powershell` 使用相同的代码字体、字号、行高和字重。
- 所有代码块左对齐；代码字体为统一的等宽字体并保留缩进，字段对齐交给表格，不用 CSS 或空格制造伪表格。
- `text`、语言代码块和 `include` 代码共用字体、字号、行高、内边距、边框和 `--code-*` 令牌；页面明暗颜色使用 GitHub 中性灰、蓝色链接和绿色状态色。
## 结构

| 路径 | 职责 |
|---|---|
| `theme/scss/theme-*.scss` | Bootstrap 变量 |
| `theme/css/*.css` | 组件规则（颜色走 `tokens.css`） |
| `theme/assets/` | 自托管字体 + 站点图标（整目录发布） |
