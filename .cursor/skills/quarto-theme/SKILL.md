---
name: quarto-theme
description: Quarto Book HTML 主题与设计系统。涉及 theme/scss、theme/css、includes、设计令牌、布局校验时使用。默认中文。
---

# Skill: quarto-theme

明暗双主题，基准 [Cursor 文档](https://cursor.com/cn/docs) 三栏布局 + Cursor 橙强调。

## 任务路由（[docs/tasks/INDEX.md](../../../docs/tasks/INDEX.md)）

| 任务 ID | 可写 |
|---|---|
| TASK-THEME-001 | `tokens.css`、`theme/scss/*` |
| TASK-THEME-002 | `nav.css`、`sidebar.css` |
| TASK-THEME-003 | `content.css`、`code.css` |
| TASK-THEME-004 | `callouts.css`、`landing.css` |
| TASK-THEME-005 | `mermaid.css`、`includes/` |
| TASK-THEME-006 | 跑 `check_layout.py` |

必读：`references/design-tokens.md` + 目标 css 文件。渲染命令见 `docs/agent/render-ops.md`。

## 结构

| 路径 | 职责 |
|---|---|
| `theme/scss/theme-*.scss` | Bootstrap 变量 |
| `theme/css/*.css` | 组件规则（颜色走 `tokens.css`） |

改样式先找对应域 css 文件。
