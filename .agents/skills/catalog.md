# Skills 目录索引

本文件只做短路由，控制在 3000 字符以内。普通任务先读命中的 `SKILL.md`，再按其中的局部路由读取必要 reference，不加载完整索引。

## skill 与 knowledge 的分工

同一个知识点只允许有一个出处：怎么做（流程、格式约定、硬约束）留 `references/`，为什么（领域结论与取舍依据）进
`knowledge/`。`references/` 优先写稳定 `kb_id`，确需检索时再给一行带 `--domain` 的 `run.ps1 kb-search`
入口，不复制知识正文。

新增或迁移 `knowledge/` 文件后运行 `kb-index`、`kb-check` 和 `kb-eval`。索引产物统一放在 `temp/`，缺失时脚本会自动重建。

## L1 入口（每次只读命中的那一个）

| Skill | 管什么 | 不适用时转交 |
|---|---|---|
| `agent-ops/SKILL.md` | Agent 运行入口、Skills 分层、MCP、仓库重构与统一验收 | 写正文转 `cpp-content`/`quarto-docs`，改样式转 `quarto-theme` |
| `code-review/SKILL.md` | Defect-First 只读审查 C++ 示例与文档 | 需要动手改文件时转对应内容 skill |
| `cpp-content/SKILL.md` | 中文 C++20 教程、示例与练习的正确性与递进 | 页面结构转 `quarto-docs`，样式转 `quarto-theme` |
| `github-ops/SKILL.md` | git 工作流、gh CLI、PR/Issue、Pages 发布与 CI 操作清单 | 正文与 skill 内容改动转对应 skill |
| `python-tools/SKILL.md` | 本仓库 Python 工具、知识库管道、脚手架与运行时选择 | 检查项编排转 `agent-ops`，知识正文转 `knowledge/` |
| `quarto-docs/SKILL.md` | `.qmd` 正文写法、Book 结构、中文技术文档格式 | 渲染参数取值转 `quarto-theme`，C++ 语义转 `cpp-content` |
| `quarto-theme/SKILL.md` | HTML 主题、设计令牌与布局契约 | 正文写法与 `.qmd` 结构转 `quarto-docs` |

## 详细路由

- part 与章节文件的命名约束以 `cpp-content/references/cpp/engineering.md` 为准；工程背景分册用短路径 `practice`、读者可见标题“工程应用”。

- `.agents/skills/cpp-content/references/tasks/<part>.md`：章节状态、读写边界和验收的唯一出处，由 `scope` 自动选中。
- `knowledge/README.md`：知识库规范和新增流程。新增或迁移知识后运行 `kb-index`、`kb-check` 和 `kb-eval`。
- `quarto-docs/references/zh/writing-principles.md`：所有中文文档任务的最高优先规则。
- `quarto-docs/references/zh/chapter-writing.md`：C++ 学习轨迹笔记页面骨架、术语门槛和新手成功路径。

普通任务只读取命中的 `SKILL.md`、目标文件和其中明确要求的 reference。需要了解知识文件规范时读取 `knowledge/README.md`，不维护第二份手工目录。
