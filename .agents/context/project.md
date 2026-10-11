---
kb_id: "cpp-project-overview-v1"
title: "项目现状与范围"
domain: "agent-workspace"
subdomain: "overview"
tags: [project, scope, parts, milestones]
level_range: [0, 5]
dependencies: []
created: "2026-10-11"
updated: "2026-10-11"
chunk_strategy: "semantic_heading"
estimated_tokens: 900
---

# 项目现状与范围

本文件回答「这个仓库现在是什么、写到哪、公开面怎么定」。读者面的完整解释统一维护在 `content/**/*.qmd`；命名与顺序的取舍依据记录在标识 `cpp-agent-repository-navigation-v1` 的知识文件。当前进度与状态以本文件为权威，改动现状时先改这里。

## 项目定位

- 本仓库是中文 C++ 学习轨迹笔记，用 Quarto Book 发布到 GitHub Pages（`chengzhao-dev.github.io/cpp-notes`）。内容从 Linux 开发环境开始，走通单文件编译、最小程序结构、CMake、多文件工程和库，再进入语言基础。
- 每章配套可运行示例：单文件示例是 `code/<part>/<chapter>.cpp`，工程示例是同名工程目录。语言机制的工程用法由姊妹仓库 cpp-board-games 承担，跨仓读者链接用 GitHub 绝对 URL。
- 仓库根 `README.md` 面向读者给入口与阅读顺序；`.agents/` 只保留 Agent 判断所需的事实与取舍。

## 当前分册范围

`content/` 当前有六个 part：`getting-started`（入门与构建）、`language-basics`（语言基础）、`language-advanced`、`standard-library`、`toolchain`、`practice`（工程应用）。part 导航页固定为 `index.qmd`。阅读顺序的唯一执行来源是 `_quarto.yml`，面向读者的顺序说明由各 part 的 `index.qmd` 承担；章节文件不使用数字前缀。

`getting-started` 当前覆盖 WSL2 环境、第一个程序、最小程序结构、CMake 工程与多文件工程；`language-basics` 覆盖类型与变量、函数、分支和循环、const、constexpr、常量关键词与类；`practice` 覆盖静态库、动态库与 Android 影像交付形态。分册命名与页面分层见标识 `cpp-quarto-practice-pattern-v1` 的规范文件。

## 公开面与发布

- 上库内容 = `main` 未被 `.gitignore` 排除的源码 + `gh-pages` 上 Actions 推的 `_book/`；部署源类型与发布闸门见 `shipping-github` 技能与标识 `cpp-tooling-pages-deploy-v1` 的知识文件。
- CI 由 `.github/workflows/pages.yml` 承担渲染与部署；渲染通过不等于可发布，发布判据见 `shipping-github` 技能。

## 能力口径

- 站点形态维持 Quarto Book HTML 与现有主题资产；导航标题可调，目录 slug 稳定不改名。
- 新 part 或新章节先登记任务矩阵（`writing-cpp` 技能 `references/tasks/<part>.md`），可运行示例与正文同批交付，不预先创建空目录。
- 语言机制新章节只写本仓教学事实；井字棋工程事实只进 cpp-board-games，不在两仓复制条文。
