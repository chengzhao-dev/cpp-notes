---
kb_id: "cpp-quarto-project-tree-diagram-focus-v1"
title: "工程目录树与图表的事实边界"
domain: "quarto-docs"
subdomain: "writing"
tags: [project_tree, hidden_config, build_output, cache, information_architecture]
level_range: [0, 5]
dependencies: ["cpp-quarto-chapter-pattern-v1", "cpp-quarto-section-focus-density-v1"]
created: "2026-09-11"
updated: "2026-09-12"
chunk_strategy: "semantic_heading"
estimated_tokens: 1250
---

# 工程目录树与图表的事实边界

本文解释工程目录和流程图为什么要分层呈现。具体操作规则见 `quarto-docs` 的工程目录树 reference。页面块序列见 `cpp-quarto-chapter-pattern-v1`，小节主线见 `cpp-quarto-section-focus-density-v1`。

## 目录树必须先尊重磁盘事实

文件名、大小写和层级是读者复制命令、定位配置和理解构建产物的依据。目录树若凭想象添加文件，读者会在实际工程中找不到它。若把所有缓存照搬进来，读者又会把生成物误认为需要维护的项目文件。因此先从磁盘确认，再筛选当前任务需要的教学视图。

`.cache/`、日志和对象文件通常没有独立教学任务，可以省略。`build/` 虽然也是生成目录，但其中的可执行文件和 `compile_commands.json` 能证明构建闭环或解释 `clangd`，因此是否展开取决于当前任务。精确文件清单与注释由 `project-tree-and-diagram-focus` reference 维护。

## 展示顺序服务于工程心智模型

磁盘枚举顺序是事实来源，不一定是最佳阅读顺序。展示顺序要让读者形成“工程配置 → 生成结果 → 工具配置 → 自动执行 → 构建规则 → 源码”的心智模型，具体顺序由写作 reference 维护。同类配置只展示一部分会制造错误的必需性判断，因此筛选边界必须在当前任务内有明确理由。

## 正式 C++ 章节以标题和文字衔接

目录树、源码、命令和输出分别服务结构、阅读、操作和验收。目录树标题到树为止，源码阅读另起任务标题。这样读者不必在同一小节内切换多种阅读模式。

正式 C++ 教学章节不使用 Mermaid 演示“源码 → 构建 → 运行”的线性主线，改用标题和因果文字衔接。复杂数据流或状态转换若确实难以用文字表达，才使用独立图表并给出一句结论。
