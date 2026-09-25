---
kb_id: cpp-retrieval-audit-2026-09-24-v1
title: Agent 资源职责与检索统一审计
domain: governing-agents
subdomain: retrieval
tags: [audit, retrieval, benchmark, mcp]
dependencies: [cpp-retrieval-governance-v1]
created: 2026-09-24
updated: 2026-09-24
chunk_strategy: semantic_heading
estimated_tokens: 700
---

# Agent 资源职责与检索统一审计

日期：2026-09-24

## 结论

`skills/`、`knowledge/` 和 MCP 不应合并为一个目录或一个事实源。`skills/` 负责怎么做，`.agents/knowledge/` 负责稳定事实、设计理由和失败模式，MCP 负责宿主的结构化受限调用。`chengzhao-dev` 的 registry 适合条目级 L1 路由，`cpp-notes` 的 SQLite FTS5/BM25、概念关联和 Parent 回溯适合 L2/L3 正文检索。

本轮新增 `.agents/knowledge/agent-workspace/retrieval-governance.md` 作为统一职责和协议的领域依据；没有把现有 knowledge 搬进 skills，也没有删除 MCP。

## 文件级决策

| 区域 | 当前处理 | 依据 |
|---|---|---|
| `.agents/skills/governing-agents/references/catalog.md` | 保留短路由，补充统一治理知识入口 | 不复制领域正文 |
| `.agents/skills/maintaining-python/SKILL.md` | 保留管道执行与运行时硬约束，链接统一协议 | 流程归 skill |
| `.agents/knowledge/` | 保留领域依据，新增治理知识 | 稳定事实归 knowledge |
| `.agents/mcp/server.py` | 保留受限 MCP，增加只读 `knowledge_search` | MCP 是安全适配层 |
| `chengzhao-dev/.agents/tools/` | 新增条目级统一响应适配器 | 保留 registry 定位语义 |

## MCP 工程价值

现有 MCP 有固定 Python、路径穿越/符号链接检查、敏感文件过滤、输出截断、精确 SHA-256 编辑和执行工具授权标记。仓库内部主入口仍是 `run.py/run.ps1`；MCP 不提供任意 shell、删除、commit 或 push，因此没有证据支持整体删除。新增 `knowledge_search` 只读工具，将检索结果转换为统一响应，不取代底层索引器。

## 统一协议

请求字段：`repository`、`query`、`kind`、`domain`、`scope`、`status`、`top_k`、`token_budget`、`explain`。

响应结果字段：`repository`、`id`、`kind`、`path`、`title`、`heading_path`、`score`、`match_type`、`content`、`source`、`updated`、`status`、`rank`。

## 同语料 benchmark

控制变量为同一 `cpp-notes/.agents/knowledge` 语料、5 条查询、Top-5、同一 `kb_common.estimate_tokens` 口径和同一 Python 解释器。registry 基线只看标题/frontmatter 条目定位；hybrid 使用现有知识库检索。报告写入 `temp/retrieval/fair-benchmark.json`，不入库。

首次结果：registry 条目定位 Recall@5 为 0.0，P50/P95 约 7.6/8.1 ms；hybrid 内容检索 Recall@5 为 0.6，P50/P95 约 18.9/20.2 ms，平均注入约 336 tokens。该小样本不能替代正式评测，但说明两种方案测量对象不同：registry 快而轻，混合检索更适合正文问题。

现有 cpp-notes 正式评测：108 个样本，Top-5 召回 94.4%，P50/P95 约 12.8/17.3 ms，注入峰值 2307 tokens，达到当前 92%、200 ms、6000 tokens 门槛。知识健康检查：27 个文件、357 个 live chunks、格式/未索引/陈旧/孤立/重复/Parent 超限均为 0；62 个冲突候选属于待人工确认提示，不是失败。

## 选型

当前推荐“L1 registry 路由 + L2/L3 FTS5/BM25/概念关联/Parent 预算检索”，两个仓库共享协议、来源格式、排除规则和评测格式，各自保留内容与索引生命周期。只有同语料正式评测证明 embedding 或 reranker 有净收益时，才考虑增加外部模型或服务。
