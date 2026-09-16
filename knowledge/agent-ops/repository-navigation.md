---
kb_id: "cpp-agent-repository-navigation-v1"
title: "仓库 part 与章节命名决策依据"
domain: "agent-ops"
subdomain: "repository"
tags: [repository, navigation, part, chapter, filename, naming, ordering, quarto, yaml, kebab_case, semantic_name, display_title, stable_slug]
level_range: [0, 9]
created: "2026-09-15"
updated: "2026-09-15"
chunk_strategy: "semantic_heading"
estimated_tokens: 460
---

# 仓库 part 与章节命名决策依据

## Part 名称

顶层 part 使用描述性英文目录，依次为 `getting-started`、`language-basics`、`standard-library`、`memory`、`performance`、`debugging`、`toolchain` 和 `reference`。名称表达读者获得的知识范围，不复述站点的写作规范，也不使用 `core` 这类离开上下文后含义不稳定的短词。

目录名全部使用 ASCII kebab-case。`getting-started` 保留为已经公开的稳定入口。`core`、`stl` 和 `cheatsheet` 在内容尚未发布前分别迁移为 `language-basics`、`standard-library` 和 `reference`，把重命名成本限制在任务矩阵和生成脚本。

目录 slug 与读者可见的 part 标题承担不同职责。slug 稳定后同时影响 URL、代码路径、任务矩阵和自动路由，不应仅为匹配内容扩展而改名。导航标题可以随页面范围调整，但要覆盖整个 part 的读者任务。`getting-started` 的目录保持不变，显示标题从“配置环境”扩展为“入门与构建”，因为环境搭建之后还包含直接编译、CMake、多文件工程和库链接。

## 章节文件

章节文件使用简短 kebab-case，优先写具体主题或读者任务，例如 `setup-wsl2`、`first-program`、`multi-file-project`。名称不重复父 part 已表达的类别，所以 `standard-library` 下使用 `vector`，不写 `stl-vector`。也不使用 `chapter-`、`intro-` 等没有新增信息的词。

part 导航页固定为 `index.qmd`。各 part 的正文使用 `content/<part>/<chapter>.qmd`，示例使用 `code/<part>/<chapter>.cpp` 或同名工程目录。只有文件名本身无法承载章节顺序表，因此 Codex 路由和 Quarto 配置仍读取任务矩阵与 `_quarto.yml`。

## 排序与编号

阅读顺序的唯一执行来源是 `_quarto.yml`，面向读者的顺序说明由各 part 的 `index.qmd` 承担。章节文件不增加 `000-` 这类数字前缀，因为数字会成为第二套顺序来源。插入、移动或合并章节时，还要同时维护文件名、链接、示例目录、任务矩阵和构建命令，容易产生与 YAML 不一致的漂移。

语义文件名在跨页面链接和搜索结果中比编号更稳定。若确实需要批量排序，可以由生成脚本根据 `_quarto.yml` 输出检查结果，而不是把顺序编码进入路径。该策略让 URL 和文件身份只表达内容，让顺序表达放在唯一配置中。
