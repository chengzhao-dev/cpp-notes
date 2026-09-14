# 重构与体量准则

重构以行为守恒和可验证契约为最终裁决：公共 CLI、MCP 工具名、`description`、参数 Schema 与返回结构保持兼容。

## 权威出处规则

- 分工边界与「同一知识点只允许一个出处」的权威定义在 `.agents/skills/catalog.md`「skill 与 knowledge 的分工」，其他文件只引用不复制。
- 迁移内容前先判定归属：「怎么做」留 `references/`，「为什么」进 `knowledge/`，两处都有时删掉非权威的一份。

## 三层加载契约

| 层 | 内容 | 预算 | 判定 |
| --- | --- | --- | --- |
| L0 `AGENTS.md` | 项目结构、命令、硬约束 | ≤65536 字节 | `check_skill_size.py` |
| L1 `*/SKILL.md` | 职责、适用场景、路由、P0、流程、判据 | ≤45 行且 ≤3000 字符 | 同上 |
| L2 `*/references/**/*.md` | 单一主题的 P1/P2 细则与按需知识 | ≤160 行且 ≤6000 字符 | 同上 |

`name` ≤64 字符、`description` ≤1024 字符、全部 skill 的 `name + description` ≤8000 字符。预算按字符为主、字节为次级护栏，理由见脚本头部说明。

## SKILL.md 统一骨架

必选段落按固定顺序出现，让 agent 用标题即可定位，不必通读：

1. H1 后一句职责与边界（负责什么、交给谁）。
2. `## 适用场景`：正向触发条件 + 明确的**不适用**去向。
3. `## 任务路由`：表格「要做的事 → 读哪个文件」，禁止整包加载。
4. `## P0 硬约束`：违反即返工，编号列表，不解释成因。
5. `## 工作流程`：动词开头的有序步骤，每步可验证。
6. `## 完成判据`：可执行命令或客观状态，不用「检查一下」收尾。
7. 可选 `## 输出格式`：仅在该 skill 有产物契约时保留。

P1 强制细则、P2 建议和反模式一律下沉 L2 或 `knowledge/`。

## 任务矩阵契约（L2 的特殊形态）

`.agents/skills/cpp-content/references/tasks/<part>.md` 一行一章，是章节路由与状态的唯一权威记录，格式由
`.agents/skills/agent-ops/scripts/scope.py` 解析、由 `generate_tasks.py` 生成、由
`check_task_matrix.py` 断言，三者必须同步：

1. 列顺序固定为 `ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注`，行以 `| \`TASK-` 开头且 8 格。
2. `—` 表示空。无内容占位写作 `—（不新建）`、`—（本章无示例）`，不留裸空白。
3. ID 前缀按 part 固定（ENV/CORE/STL/MEM/PERF/DBG/TOOL/CS），三位数字在 part 内连续。
4. 文件级读写边界只写一次（`## 公共读写边界` 的 `- **必读**` 行），行间只写差异。
   交集变化时先改生成表的章节数据，再 `generate_tasks.py --write`。
5. 状态只允许 `todo` / `done` / `merged`。merged 章不得留下同名正文。

## 重构执行纪律

- 修改前先检索入口、引用和测试，理解文件职责后再迁移或删除。
- 需要改名、提取或拆分时，先比较新旧职责，保留有效信息，完成后从整体复核术语、链接、顺序和重复内容。
- 相同职责只保留一个权威实现。公共逻辑放入对应 skill 的 `scripts/` 或 `references/`。
- 删除文件后移除空目录（`check_empty.py` 对空文件与空目录都判 FAIL）。
- Skill 目录与文件名使用 kebab-case 与 ASCII。`agents/openai.yaml` 是宿主 UI 元数据，不参与任务路由。
- 完成后运行 `& .agents/skills/agent-ops/scripts/run.ps1 check`。涉及知识库再跑 `kb-index`、`kb-check` 和 `kb-eval`。
