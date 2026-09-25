---
kb_id: cpp-retrieval-governance-v1
title: Agent 资源分层与统一检索协议
domain: governing-agents
subdomain: retrieval
tags: [skill, knowledge, memory, registry, retrieval, mcp]
dependencies: []
created: 2026-09-24
updated: 2026-09-24
chunk_strategy: semantic_heading
estimated_tokens: 900
---

# Agent 资源分层与统一检索协议

## 资源职责边界

Agent 资源按回答的问题分层，而不是按文件格式分层。项目硬约束和路径边界属于 instruction；任务流程、入口、格式和可执行硬约束属于 skill/reference；稳定领域事实、设计理由、权衡与失败模式属于 knowledge；跨会话的历史经验属于 memory。生成的 registry、速查表和数据库只负责定位或加速，不能成为事实唯一来源。

当 skill 需要依据时，应通过 `kb_id` 或一次 `kb-search` 入口指向 knowledge，而不是复制知识正文。knowledge 可以解释为什么采用某个流程，但不应重新定义必须执行的命令。这样既能避免两处内容漂移，也能让检索器根据资源类型和状态过滤结果。

## 统一检索请求

两个仓库可以保留不同的领域内容和索引实现，但检索请求应表达相同的意图：`repository`、`query`、`kind`、`domain`、`scope`、`status`、`top_k`、`token_budget` 和 `explain`。未指定 `repository` 时只允许在明确的聚合入口中跨库查询；普通仓库入口必须拒绝隐式跨库，避免同名 skill 或 knowledge 互相污染。

## 统一检索响应

每个结果至少包含 `repository`、`id`、`kind`、`path`、`title`、`heading_path`、`score`、`match_type`、`content`、`source`、`updated`、`status` 和 `rank`。`source` 必须能回到唯一事实文件；`status` 用于排除 superseded 或 deprecated 内容。条目级 registry 命中只能声明为定位结果，不能伪装成段落级语义召回。

## 分层检索策略

轻量 registry 适合 L1 路由：用短摘要、触发词、路径和资源 ID 快速找到目标正文。内容问题使用 L2/L3 检索：先做作用域和元数据过滤，再用精确标识符与 BM25 召回，必要时加入概念关联、融合排序、Parent 回溯和 Token 预算。代码、路径和 C++ 标识符必须保留精确匹配能力，不能只依赖语义相似度。

MCP 是结构化调用和安全边界，不是知识库事实源，也不规定分块、排序或评测算法。MCP 可以暴露 `scope`、`search`、`read`、`health` 等只读能力；编辑、构建和渲染能力必须单独标明副作用并接受宿主授权。

## 公平评测原则

对不同检索器的比较必须固定同一 corpus snapshot、查询集、相关性标注、Top-K、Token 估算口径、Python 解释器和硬件。冷缓存、热缓存、全量构建、增量构建、查询延迟和上下文注入分别报告，不能只比较一方的预生成索引与另一方的全量扫描。

至少记录 Recall@1/@3/@5/@10、MRR、nDCG@K、无答案准确率、active/superseded 版本正确率、来源可追溯率、P50/P95 查询延迟、索引和增量构建时间、注入 Token、跨仓库误召回率及越界/敏感文件泄露率。检索质量和 Agent 最终生成质量应分开评测。

## 当前选型

在同语料实测证明前，不引入远程 MCP、向量数据库或外部运行时依赖。推荐形态是 L1 registry 路由加 L2/L3 的 SQLite FTS5/BM25、精确标识符、概念关联和 Parent 预算检索；两个仓库共享协议、来源格式和评测集，各自保留领域内容及索引生命周期。
