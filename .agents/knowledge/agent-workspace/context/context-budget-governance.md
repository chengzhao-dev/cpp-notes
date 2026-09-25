---
kb_id: "cpp-agent-context-budget-v1"
title: "内容增量与上下文预算治理"
domain: "governing-agents"
subdomain: "agent_runtime"
tags: [context_budget, token_budget, qmd, skill, knowledge, page_split, include, progressive_disclosure]
level_range: [0, 9]
dependencies: ["cpp-tooling-codex-context-v1", "cpp-agent-repository-navigation-v1"]
created: "2026-09-16"
updated: "2026-09-16"
chunk_strategy: "semantic_heading"
estimated_tokens: 900
---

# 内容增量与上下文预算治理

## 按加载路径控制而不是限制全库总量

仓库会持续增加章节、skill reference 和领域知识，因此不能用一个全库字符总配额判断是否健康。真正影响模型效果的是单次任务实际加载的文件、单次检索注入的 Parent 和稳定前缀的长度。预算应分别落在 `AGENTS.md`、L1、L2、教学 QMD 和知识检索单元上。

知识文件不需要整体读入。检索先通过元数据缩小范围，命中 Child 后回溯 Parent，并受 6000 Token 硬上限约束。只要 Parent 保持在默认 4000 Token 内，知识库就可以增加主题，而不必为了总量指标把完整概念拆散。

## QMD 超限后的拆页顺序

教学页超过 150 行或 5000 有效字符时，应按读者任务和工程变量拆成系列页。一个好的顺序是“单文件 → CMake → 多文件结构 → 静态库 → 动态库”，每页只引入一个新的主要变量，并独立给出构建与验证结果。

不要机械写成“上篇、中篇、下篇”，也不要把同一任务按篇幅切开。每一步都要能独立回答读者的问题，并在 `_quarto.yml`、part 索引和任务矩阵中登记顺序。每个页面使用自己的示例路径，避免一次任务为了一个页面读取整个系列。

## 代码与正文的预算边界

5000 有效字符排除围栏代码和 `{{< include >}}` 行。完整示例源码由 `code/` 单独维护、独立校验并按任务登记，如果再次计入页面字符会造成重复计量，也会迫使正文删掉必要的解释。长代码必须下沉到 `code/`，页面只保留真实文件名对应的 include。

行数仍按 QMD 原始源码计算，防止用超长内联代码块绕过页面预算。页面宏、标题、正文、列表、Callout 和行内代码仍计入有效字符，因为这些内容会随页面一起直接进入上下文。

## 增量准入

新增内容前先检查现有权威。skill reference 只写怎么做，knowledge 只写为什么；同一主题优先扩展现有文件，不建立平行副本。新增知识后要补评测查询并更新导览，新增 QMD 后要补任务矩阵、阅读顺序和示例路径。

超预算时先压缩措辞、合并相近主题和删除一次性案例，再拆页或拆 Parent。只有现有职责边界和预算都无法容纳时，才新增 skill、knowledge 文件或独立章节。
