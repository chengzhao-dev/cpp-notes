---
kb_id: "cpp-architecture-overview-v1"
title: "现行架构"
domain: "agent-workspace"
subdomain: "overview"
tags: [architecture, layout, parts, chapters, quarto]
level_range: [0, 5]
dependencies: []
created: "2026-10-11"
updated: "2026-10-11"
chunk_strategy: "semantic_heading"
estimated_tokens: 700
---

# 现行架构

本文件回答「仓库现在怎么组织、各部分住在哪」。命名决策与被否决的替代方案记录在标识 `cpp-agent-repository-navigation-v1` 的知识文件。

## 目录结构

```text
content/<part>/<chapter>.qmd   # 章节正文，part 导航页为 index.qmd
code/<part>/<chapter>.cpp      # 单文件示例；工程示例用同名工程目录
.quarto.yml                    # 阅读顺序与站点配置的唯一执行来源
.agents/context/               # 现行事实与规范条文；入口 README.md
.agents/knowledge/             # 为什么与正反例；入口 KNOWLEDGE.md
.agents/skills/                # 工序；命中技能才读 SKILL.md
```

顶层 part 依次为 `getting-started`、`language-basics`、`language-advanced`、`standard-library`、`toolchain`、`practice`。章节文件名用简短 kebab-case，不重复父 part 已表达的类别（`standard-library` 下写 `vector`，不写 `stl-vector`）。

## 顺序与命名的唯一来源

阅读顺序只由 `_quarto.yml` 表达，章节文件不增加数字前缀，不建第二套顺序来源。插入、移动或合并章节时同时维护文件名、链接、示例目录、任务矩阵和构建命令。任务矩阵是 `writing-cpp` 技能 `references/tasks/<part>.md`，`scope` 按它反查最小读取集。

## 示例与正文同批交付

每个章节的可运行示例与正文同批维护：单文件示例直接放 `code/<part>/`，多文件示例建同名工程目录并带自己的构建说明；构建链与诊断边界见 `development.md`。示例代码只服务教学，不引入仓库级 CMake 工程。

## 两仓分工

cpp-notes 讲语言机制与写作规范；井字棋工程事实只进 cpp-board-games。跨仓读者链接用 GitHub 绝对 URL，不在两仓复制对方条文。
