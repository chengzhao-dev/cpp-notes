---
kb_id: "cpp-tooling-quarto-html-v2"
title: "Quarto HTML 输出选项与生效边界"
domain: "writing-quarto"
subdomain: "html_output"
tags: [quarto, html, toc, theme, grid, syntax_highlight, code_fold, navigation]
level_range: [0, 9]
dependencies: ["cpp-tooling-quarto-render-v2"]
created: "2026-09-09"
updated: "2026-09-09"
chunk_strategy: "semantic_heading"
estimated_tokens: 800
---

# Quarto HTML 输出选项与生效边界

## 作用域

项目级配置提供默认值，格式级配置覆盖输出行为，页面 frontmatter 只应用于当前页面。外观配置集中在主题资源。同一选项不要同时在多层定义。

## 导航与代码块

目录深度、导航和交叉引用由 HTML 输出配置控制。代码折叠、语法高亮和主题配色应按实际输出格式设置。修改后检查 HTML，而不是只检查 YAML。
