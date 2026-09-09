---
name: agent-ops
description: 维护 Agent 运行入口、Skills、MCP 与仓库重构时使用，统一脚本、路由和验收。
metadata:
  short-description: 维护 Agent 入口与 Skills 结构
---

# Skill: agent-ops

统一承载 Agent 运行入口、Skills 分层、MCP 与仓库级验收；只回答「怎么组织与维护」，领域结论交给 `knowledge/`。

## 适用场景

- 新建、合并、重构、改名或删除 skill、reference、MCP 工具与脚本入口。
- 用 `scope` 确定读取边界，用 `check`（含 `tasks` 矩阵一致性）收口验收。
- **不适用**：写章节正文（转 `cpp-content` 或 `quarto-docs`）、改样式（转 `quarto-theme`）。

## 任务路由

| 任务 | 读取 |
| --- | --- |
| 改 skill 结构、体量、任务矩阵格式与 ID 规则 | `references/refactor-guidelines.md` |
| 目录关系、章节路线图、运行边界与诊断逃生舱 | `references/repository-structure.md` |
| skill 全景与分工权威 | `../catalog.md` |

## P0 硬约束

1. 每条规则只有一个权威出处，禁止把同一条规则复制进两个文件。
2. L1 只保留路由与硬约束，L2 只承载单一主题的按需知识；越界先瘦身再合并，不得放宽 `check_skill_size.py` 的预算常量。
3. 目录、文件名、命令、版本和路径以磁盘实测为准；确认不了就不写、不伪造。
4. 重构默认在原文件上局部进行，不因「重构」删除后重写，除非用户明确要求或原结构已无法安全修复。
5. 任务矩阵、`scope.py` 与 `generate_tasks.py` 三者同格式；改任一处必须跑 `run.py check`（含 `tasks` 一致性检查）。

## 工作流程

1. 先读 `../catalog.md`、目标 skill 和 `check_skill_size.py --verbose`，量清当前余量。
2. 搜索相近规则，优先并入职责最接近的现有文件，同时删除重复表述。
3. 超预算时按序处理：压缩措辞 → 合并相近主题 → 移除一次性案例 → 新增 L2 → 新增 L1。
4. 同步更新父级 `SKILL.md`、`../catalog.md` 与路由说明；删文件后移除随之变空的目录。

## 完成判据

- [ ] `python .cursor/skills/agent-ops/scripts/run.py check` 全通过，`git diff --check` 干净。
- [ ] 每条规则都能指向唯一出处，L1/L2 均在预算内。
- [ ] 保留用户既有改动，`content/`、`code/` 无回归。
