# Agent 工作区命名规范

本规范适用于 `.agents/` 下 `skills/`、`knowledge/`、`memory/`、`incidents/` 及技能内部目录。结构规则见同技能下的 `structure.md`；两者冲突时，命名以本文件为准，结构以 `structure.md` 为准。

## 1. 核心原则

- 默认 **kebab-case**：全小写 + 连字符，如 `writing-readme`。
- 固定入口文件用大写：`AGENTS.md`、`SKILL.md`、`KNOWLEDGE.md`、`MEMORY.md`、`INDEX.md`、`README.md`。
- 名称有语义：能看出「是什么」或「做什么」，禁用 `utils`、`misc`、`temp`、`new`、`final`。
- 技能目录名 ≤ 20 字符，动作 + 对象（如 `shipping-github`）。
- 字符集仅 `a-z`、`0-9`、`-`、`_`、`.`；禁止连续连字符；文档路径一律纯 ASCII，中文只出现在文件内容里。
- 技能内可导入 Python 用 `snake_case`（`check_health.py`）；Shell 用 kebab-case（`run-xxx.sh`）。

## 2. 各类命名

| 类型 | 规则 | 示例 |
| --- | --- | --- |
| 技能目录 | 动作+对象 kebab-case，≤20 | `governing-agents`、`shipping-github` |
| 知识领域 | 领域名词 kebab-case | `agent-workspace`、`cpp-teaching` |
| 记忆 / 事故领域 | 领域名词 kebab-case | `quarto-render`、`git-github` |
| 普通 Markdown | kebab-case + `.md` | `retrieval-governance.md` |
| 领域索引 | `<domain>/index.md` | `agent-workspace/index.md` |
| 每日记忆 | `daily/YYYY-MM-DD.md` | `2026-09-24.md` |
| 技能内参考 | `<topic>.md`，可按性质分子夹 | `.agents/skills/writing-quarto/references/zh/writing-principles.md` |
| Python 脚本 | `<action>_<target>.py` | `check_health.py` |

## 3. 一致性要求

- 技能目录名必须与 `SKILL.md` 的 `name` 字段一致。
- 知识文件 frontmatter 的 `domain` 字段取同名领域目录值。
- 同一层级、同一类资源保持同一种命名风格；改名时同步所有引用，不留旧名孤儿路径。
