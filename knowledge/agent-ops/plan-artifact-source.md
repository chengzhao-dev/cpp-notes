---
kb_id: "cpp-agent-plan-artifact-source-v1"
title: "Plan Mode 计划产物的来源与完整性"
domain: "agent-ops"
subdomain: "planning"
tags: [plan_mode, app_server, plan_item, markdown, completeness, stream_delta, context_compaction]
level_range: [0, 9]
dependencies: ["cpp-tooling-codex-context-v1"]
created: "2026-09-15"
updated: "2026-09-16"
chunk_strategy: "semantic_heading"
estimated_tokens: 880
---

# Plan Mode 计划产物的来源与完整性

本文解释计划为什么不会自动成为 Markdown，以及流式重建为什么可能缺内容。落盘步骤见
`.agents/skills/agent-ops/references/plan-artifacts.md`。

## Plan Mode 只产出协议计划项

官方 CLI 文档把 `/plan` 定义为切换计划模式并让 Codex 在修改前提出执行计划。它没有承诺生成计划文件，
计划默认停留在对话与协议事件中。

App Server 把计划表示为类型为 `plan` 的 ThreadItem，内容形状是 `{id, text}`。因此，计划能不能成为
`.md` 取决于客户端是否在最终事件到达后主动写入，而不是 Plan Mode 的自然产物。

依据见 [官方 CLI 命令文档](https://learn.chatgpt.com/docs/developer-commands.md?surface=cli)。

## 最终计划项才是权威来源

App Server 会发送 `item/plan/delta` 流式文本，但官方文档明确说明最终 `plan` 项不保证等于所有 delta
的简单拼接。`item/completed` 才是最终状态，最终计划项必须来自这里。

如果把 delta 当成完整计划，客户端通常只得到正文片段或无结尾的中途版本。用最终 agent 摘要再改写一次
也有同样风险，因为摘要只保留模型认为重要的部分，不能作为原文。

依据见 [官方 App Server 文档](https://learn.chatgpt.com/docs/app-server.md)。

## 进度事件不是计划正文

`turn/plan/updated` 服务于步骤状态变化，条目形状是步骤与 `pending`、`inProgress`、`completed` 状态。
它适合更新执行进度，不适合恢复计划的目标、接口、验收和假设。

原始计划与执行状态应分开保存。计划文件保持只读，执行日志单独记录完成项，这样才能在上下文压缩后
同时恢复“原本要做什么”和“已经做到哪里”。

## 批准不等于上传完成

计划批准、执行验证和版本控制上传是三个不同层次。批准让 agent 可以执行计划中明确列出的写入、提交
和推送；本地 `check`、`build` 或 `render` 成功只证明工作区产物可用；只有目标远端已经包含对应 commit，
并且约定的 CI/Pages 检查完成，计划中的上传才算闭合。

因此，批准计划中的交付收口必须同时给出暂存边界、提交信息、目标分支和远端核对方式。没有远端证据时，
本地 commit 不能写成“已推送”，也不能把成功日志当作交付完成。授权只覆盖计划列出的不可逆操作，不能
扩展成未经批准的范围或强行覆盖远端历史。

## 落盘后的完整性边界

完整计划进入磁盘后仍需回读校验。文件非空只能证明写入动作发生，不能证明 H2 章节、代码围栏或末尾内容
没有截断。验证必须比较来源计划的章节和结构，并以完成标记确认写入已经结束。

计划文件与独立执行日志属于 `temp/` 中的临时工作产物。它们可以降低上下文压缩造成的损失，但不替代
版本控制中的最终代码、文档和检查结果。
