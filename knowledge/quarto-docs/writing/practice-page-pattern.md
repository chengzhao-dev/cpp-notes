---
kb_id: "quarto-practice-page-pattern-v1"
title: "工程应用分册的页面分层"
domain: "quarto-docs"
subdomain: "writing"
created: "2026-09-16"
updated: "2026-09-16"
chunk_strategy: "semantic_heading"
---

# 工程应用分册的页面分层

## 分册首页与正文

分册首页说明范围、顺序和全局环境约定；章节正文只说明当前主题的动作、背景和边界。Ubuntu 等约定不在每个页面重复。

## Callout 与折叠问答

Callout 只承载可跳过的提醒，并使用 Quarto 内置类型。章末答案紧跟问题，源文件使用 `::: {.answer}`，由 Lua filter 渲染成默认收起且可键盘访问的原生 `details`。
