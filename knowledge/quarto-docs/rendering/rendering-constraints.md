---
kb_id: "cpp-tooling-quarto-render-v2"
title: "Quarto 渲染行为与失效模式"
domain: "quarto-docs"
subdomain: "rendering"
tags: [quarto, render, yaml, callout, include, encoding, troubleshooting]
level_range: [0, 9]
dependencies: ["cpp-tooling-build-chain-v2"]
created: "2026-09-09"
updated: "2026-09-09"
chunk_strategy: "semantic_heading"
estimated_tokens: 900
---

# Quarto 渲染行为与失效模式

## 配置与产物

Book 默认输出 `_book/`，发布产物路径必须与项目类型匹配。YAML 层级、缩进或作用域错误可能不报错而静默失效；修改后应渲染并检查生成页面。

## 提示框与包含文件

Quarto 只识别内置提示框类型；自定义提示框类可能退化为普通章节。包含真实代码文件时使用带语言标记的代码围栏，否则代码中的 Markdown 字符会被当作正文解析。

## 编码与路径

中文文件使用 UTF-8 无 BOM 与 LF。路径或文件名含非 ASCII 特殊字符时，Windows 工具链可能在编码或索引阶段失败；仓库路径名保持 ASCII。
