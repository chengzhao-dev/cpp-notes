---
name: quarto-theme
description: Quarto Book HTML 主题与设计系统。涉及 theme/scss、theme/css、includes、设计令牌、布局校验时使用。默认中文。
---

# Skill: quarto-theme

明暗双主题，基准 [Cursor 文档](https://cursor.com/cn/docs) 三栏布局 + Cursor 橙强调。

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
改样式的代价与流程见 `docs/agent/ops.md`（会触发整本重渲染）。

## 已固化的产物契约

`scripts/agent/check_dom_contracts.py` 断言：复制按钮 hover 作用域必须是 `.code-copy-outer-scaffold`
（Quarto 1.10 起按钮与 `div.sourceCode` 是兄弟）；`@media print` 不得隐藏 scaffold 本身；
触屏 `@media (hover: none)` 兜底；favicon 注入与发布。改 DOM 相关样式前后都跑一次。

## 结构

| 路径 | 职责 |
|---|---|
| `theme/scss/theme-*.scss` | Bootstrap 变量 |
| `theme/css/*.css` | 组件规则（颜色走 `tokens.css`） |
| `theme/assets/` | 自托管字体 + 站点图标（整目录发布） |
