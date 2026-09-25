---
kb_id: "quarto-practice-page-pattern-v1"
title: "工程应用分册的页面分层"
domain: "writing-quarto"
subdomain: "writing"
created: "2026-09-16"
updated: "2026-09-16"
chunk_strategy: "semantic_heading"
---

# 工程应用分册的页面分层

## 分册首页与正文

分册首页说明范围、顺序和本分册的阅读入口；章节正文只说明当前主题的动作、背景和边界。全书环境约定（WSL2 Ubuntu）只在入门分册声明一次，其它分册的首页和正文都不重复。

## Callout 与折叠问答

Callout 只承载可跳过的提醒，并使用 Quarto 内置类型。章末答案紧跟问题，源文件使用 `::: {.answer}`，由 Lua filter 渲染成默认收起且可键盘访问的原生 `details`。
