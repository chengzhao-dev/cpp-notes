# 重构与维护准则

重构以行为守恒和可验证契约为最终裁决：公共 CLI、MCP 工具名、description、参数 Schema 与返回结构保持兼容。

- 修改前先检索入口、引用和测试，理解文件职责后再迁移或删除。
- 相同职责只保留一个权威实现；公共逻辑放入对应 Skill 的 `scripts/` 或 `references/`。
- Skill 使用 kebab-case 目录名与 YAML frontmatter；细节放入按需读取的 `references/`。
- 完成后运行 `python .cursor/skills/agent-ops/scripts/run.py check`，涉及知识库再运行 `kb-index`、`kb-check` 和 `kb-eval`。
