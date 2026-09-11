---
kb_id: "cpp-quarto-inline-code-boundaries-v1"
title: "技术文档行内代码标记边界"
domain: "quarto-docs"
subdomain: "writing"
tags: [inline-code, backticks, commands, identifiers, consistency]
level_range: [0, 9]
dependencies: ["cpp-quarto-chinese-style-v1"]
created: "2026-09-11"
updated: "2026-09-11"
chunk_strategy: "semantic_heading"
estimated_tokens: 600
---

# 技术文档行内代码标记边界

## 反引号标记什么

反引号的作用是告诉读者“这段文字需要逐字识别或复制”。因此命令、工具、参数、文件名、路径、配置键、API、标识符和包名应统一标记，例如 `g++`、`clangd`、`gdb`、`CMake`、`Ninja` 和 `CMakeLists.txt`。

## 普通名称不自动标记

Ubuntu、Windows 和 VS Code 作为平台或产品名称时属于自然语言，不必加反引号；当它们出现在命令、路径或精确标识中时再标记。链接文本直接使用链接，不用反引号包住链接地址。

## 一致性是可读性约束

同一章节中同一对象的标记方式必须一致。只给部分工具加反引号会让新手误以为标记本身代表不同类别，增加扫描和复制命令时的判断成本。写作 skill 的检查器负责发现关键工具的漏标记；本文件记录判断依据。
