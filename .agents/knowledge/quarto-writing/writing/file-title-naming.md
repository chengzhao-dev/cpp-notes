---
kb_id: "cpp-quarto-file-title-naming-v1"
title: "QMD 文件名与中文标题命名依据"
domain: "quarto-docs"
subdomain: "writing"
tags: [qmd, filename, title, kebab_case, naming, chapter, navigation, readability]
level_range: [0, 5]
dependencies: ["cpp-quarto-chapter-pattern-v1"]
created: "2026-09-18"
updated: "2026-09-18"
chunk_strategy: "semantic_heading"
estimated_tokens: 700
---

# QMD 文件名与中文标题命名依据

## 文件名与标题的职责分工

### 文件名与 title 的职责分工

英文文件名服务于稳定路径、版本控制和链接；中文 title 服务于读者理解和目录阅读。两者相关但不必逐字翻译：文件名应稳定，标题可以随着教学表达优化。

文件名使用 ASCII `kebab-case`，表达页面的核心主题或任务，不使用中文、空格和数字前缀。例如 `minimal-program-structure.qmd` 比 `03-minimal-program-structure.qmd` 更稳定。章节顺序由 `_quarto.yml` 和入口页负责，不由文件名中的数字承担；调整教学顺序时不必批量重命名链接。

## 中文 title 的写法

中文标题使用单行、简短、面向读者任务的表达，优先写动作或结果，避免把“教程”“详解”“学习”等泛化词堆进标题。标题应让读者预先知道这一页要完成什么，而不是只知道一个宽泛主题。

推荐使用“动作 + 对象 + 结果”的结构，但不强求固定模板：

| 文件名 | 推荐 `title` | 命名理由 |
| --- | --- | --- |
| `first-program.qmd` | `编译并运行第一个 C++ 程序` | 直接说明验证动作和产物 |
| `minimal-program-structure.qmd` | `拆分最小 C++ 程序结构` | 突出从单文件到职责分离的动作 |
| `static-library.qmd` | `构建静态库并链接程序` | 同时说明构建结果和使用方式 |
| `shared-library.qmd` | `构建动态库并运行程序` | 提醒读者还要验证运行期加载 |

不要用标题替代页面结构：一个页面只保留一个 YAML `title`，正文从 `##` 开始；标题层级、任务顺序和入口页卡片分别承担不同导航职责。

## 命名检查

改名时先确认 `_quarto.yml`、入口页、交叉引用和任务矩阵中的路径，再决定是否真的需要改文件名。若只是中文表达不够准确，优先只改 `title`。只有主题边界、页面职责或稳定语义发生变化时才改文件名，并同步所有引用。
