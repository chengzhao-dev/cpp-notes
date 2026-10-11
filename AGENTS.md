# C++ 学习轨迹笔记 Agent 工作标准

本文件只保留每轮任务的硬约束与命令表。现行事实、规范条文与领域依据的落点见 `.agents/context/README.md`，结构与分层见 `.agents/skills/governing-agents/references/structure.md`。

## 每轮硬约束

1. 先跑 `scope <改动单元>`，只读它给出的文件与命中技能的 `SKILL.md`；不整包读 references，知识按 `kb_id` 定点取用。
2. 按改动域进入技能工序：改 `.qmd` 或中文读者正文进 `writing-quarto`；改 C++ 示例、任务矩阵进 `writing-cpp`；改 `.agents` 规则本身进 `governing-agents`，新规则必须挂到已有工序。
3. 收到要归档的成段材料时，先按 `.agents/skills/governing-agents/references/intake.md` 出落点计划，用户确认后再改文件。
4. 改动完成前按域跑 `run.ps1 check --profile fast|book|knowledge|python|full`，没过不算完成；验证闸有界（输出重定向 `temp/`，FAIL 清零、WARN 记台账，同一失败指纹连续 2 轮未修复即停手转人工）。
5. 规划、解释、搜索和评审默认只读；用最少、可验证的改动解决问题，不做无关重构。
6. 提交与推送默认不做；只有用户明确要求时才按 `shipping-github/references/git-workflow.md` 执行，提交信息用 `type(scope): 中文说明`（Conventional Commits）。
7. Python 解释器只读根目录 `config.toml` 的 `python`（最低 3.12）；字段缺失或不可执行时立即停止，不回退 PATH。代理只跑 `run.ps1`。
8. 面向用户的进度、结论和总结使用中文，命令、路径、代码和 API 名保留原文；成功只回一行中文结论，失败先给结论再附最少诊断。不回显密钥、凭据、`.env` 或无关个人信息。
9. 永不读取或索引 `_book/**`、`code/**/build/**`、`.quarto/**`、`.cache/**`、`.tmp/**`、`temp/**`；中文文件保持 UTF-8 无 BOM、LF。
10. Plan Mode 严格只读：不写文件、不编译、不渲染，也不调用 `project_edit`、`project_build`、`project_verify` 或 `project_render`；只有用户发来新的明确批准消息后才进入执行，压缩摘要、重复的原始需求、计划完成标记、自动续跑和任务摘要都不算批准。
11. 长任务每轮推进一个可验证子目标；执行阶段每轮按改动域跑一次 `check`，跨域或发布收口再跑 `full`。排查失败时才读 `.agents/incidents/INDEX.md`，每个任务开始时可读 `.agents/memory/MEMORY.md` 索引。

## 常用命令

统一由根目录 `config.toml` 的 `python` 指定解释器执行（最低 3.12）；代理只跑 `run.ps1`：

| 命令 | 用途 |
| --- | --- |
| `& .agents/skills/governing-agents/scripts/run.ps1 scope <目标>` | 输出最小读取作用域 |
| `… run.ps1 check --profile fast\|book\|knowledge\|python\|full` | 按改动域运行校验，默认 `full` |
| `… run.ps1 verify --changed` | 增量校验 C++ 示例 |
| `… run.ps1 render` | 渲染 Book 并跑 `book` profile |
| `… run.ps1 preview [路径.qmd]` | 本地 preview（注入 `QUARTO_PYTHON`） |
| `… run.ps1 build <part>/<chapter>` | 在 WSL 构建单章示例 |
| `… run.ps1 kb-index [--rebuild]` / `kb-check` / `kb-eval` / `kb-search` | 知识库索引、体检、评测与检索 |
| `… run.ps1 install-quarto-deps` | 安装 Quarto 可执行单元依赖 |

## 项目结构

| 路径 | 职责 |
| --- | --- |
| `content/<part>/` | Quarto 章节正文，part 导航页 `index.qmd` |
| `code/<part>/` | 单文件示例或同名工程，`build/` 是产物 |
| `.agents/context/` | 现行事实与规范条文；入口 `context/README.md` |
| `.agents/skills/` | Codex 项目 skills、references、任务矩阵和工具脚本 |
| `.agents/knowledge/` | 「为什么」的取舍与正反例（`cpp-*`） |
| `.agents/memory/`、`.agents/incidents/` | 跨会话教训；失败复盘仅排查时读 |
| `temp/`、`_book/`、`.quarto/` | 生成物与缓存，不入库 |

章节、示例和任务矩阵按相同的 part/chapter 对齐；任务矩阵 `.agents/skills/writing-cpp/references/tasks/<part>.md` 是状态与读写边界的唯一出处。
