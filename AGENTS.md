# C++ 学习轨迹笔记 Agent 工作标准

本文件是 C++ 学习轨迹笔记的唯一项目级 Agent 入口。它先规定所有 Codex 和通用 Coding Agent 必须遵守的工作标准，再把这些标准落到本仓库的内容、代码、工具和验收边界。

## 工作标准

- 先理解目标、现状和约束。明确假设。存在多种解释时列出选项，不擅自扩大范围。
- 用最少、最清晰、可验证的改动解决问题。不做无关重构，不为一次性需求设计扩展框架。
- 修改前先定位入口、引用、测试和权威规则。保留用户已有改动，只清理由本次改动产生的孤儿代码。
- 把需求转成验收标准：先复现或建立检查，再实现，最后运行与风险匹配的验证。
- 提交与推送默认不做。只有用户明确要求时，才按 `shipping-github/references/git-workflow.md` 执行 commit、push 或远端核对；提交信息用 `type(scope): 中文说明`（Conventional Commits），`check`、`verify`、`render` 和 `build` 只证明本地改动可用。
- 面向用户的进度、结论和总结使用中文；命令、路径、代码和 API 名保留原文。计划与任务状态由宿主工具维护，本仓库不为此设立文件、模板或校验。
- 成功执行每阶段只输出一行中文结论，不粘贴原始成功日志。失败时先给中文结论，再附最少诊断。`--verbose` 仅用于默认输出无法定位失败时。不回显密钥、凭据、`.env` 或无关个人信息。
- 维护仓库规范时保持单一权威出处。流程和格式放 skill/reference，领域原因放 `.agents/knowledge/`。
- 构建配置和脚本的版本规则见 `writing-cpp` 的代码风格 reference。QMD 代码块、`include` 文件和正文标点规则见 `writing-quarto` 对应 reference。

## C++ 学习轨迹笔记项目

这是面向初学者的中文 Linux C++ Quarto Book。正文在 `content/`，与章节对应的 C++ 示例和工程在 `code/`，领域依据在 `.agents/knowledge/`，Agent skills、脚本、主题资源和项目 MCP 在 `.agents/`。

| 路径 | 职责 |
| --- | --- |
| `content/<part>/` | Quarto 章节正文 |
| `code/<part>/` | 单文件示例或同名工程，`build/` 是产物 |
| `.agents/skills/` | Codex 项目 skills、references、任务矩阵和工具脚本 |
| `.agents/mcp/` | 项目级 MCP stdio server 与说明，由宿主显式配置，不假设自动发现 |
| `.agents/skills/designing-theme/assets/theme/` | 页面主题、样式和字体资源 |
| `.agents/knowledge/` | 回答“为什么”的精简领域知识库 |
| `.agents/memory/` | 跨会话教训；任务开始时读 `MEMORY.md` 索引 |
| `.agents/incidents/` | 失败复盘；仅排查失败时读 `INDEX.md`，平时视为不存在 |
| `temp/` | 索引和分析产物，不入库 |

章节、示例和任务矩阵按相同的 part/chapter 对齐。一章需要多个独立示例工程时，在矩阵「示例」列登记全部路径。任务矩阵 `.agents/skills/writing-cpp/references/tasks/<part>.md` 是状态与读写边界的唯一出处。`.agents/` 四区（skills/knowledge/memory/incidents）的目录结构与命名规范见 `.agents/skills/governing-agents/references/structure.md` 与 `naming.md`。

## 常用命令

以下命令统一由根目录 `config.toml` 的 `python` 指定 Python 解释器执行。该字段是仓库唯一 Python 来源。缺失、不可执行或版本不足时立即停止，不回退到 PATH、环境变量或其他配置。

| 命令 | 用途 |
| --- | --- |
| `& .agents/skills/governing-agents/scripts/run.ps1 scope <目标>` | 输出最小读取作用域 |
| `& .agents/skills/governing-agents/scripts/run.ps1 check --profile fast|book|knowledge|python|full` | 按改动域运行校验，默认 `full` |
| `& .agents/skills/governing-agents/scripts/run.ps1 render` | 渲染 Book，并运行 `book` profile |
| `& .agents/skills/governing-agents/scripts/run.ps1 verify --changed` | 增量校验 C++ 示例 |
| `& .agents/skills/governing-agents/scripts/run.ps1 build <part>/<chapter>` | 在 WSL 构建单章示例 |
| `& .agents/skills/governing-agents/scripts/run.ps1 kb-index [--rebuild]` | 构建知识库索引 |
| `& .agents/skills/governing-agents/scripts/run.ps1 kb-check` | 检查知识库结构与检索延迟 |

## 读取、编辑与验收边界

1. 每次任务先运行 `scope`，只读「单元」「读取」和必要 reference。不整包读取 references。
2. 永不读取或索引 `_book/**`、`code/**/build/**`、`.quarto/**`、`.cache/**`、`.tmp/**`。产物检查交给脚本。
3. 预计读取超过 8 个文件或需要全仓检索时才派侦察代理。编辑回主线程完成。
4. 中文文件使用 UTF-8 无 BOM、LF。修改 `.qmd`、skill 或主题 CSS 后先跑编码检查。QMD 正文标点和句长遵循 `writing-quarto/references/zh/writing-principles.md`。
5. 修改 `.agents/skills/designing-theme/assets/theme/**` 或 `_quarto.yml` 会触发整本渲染。确认代价后运行 `render`；需要四档视口和明暗矩阵时运行 `render --require-browser`。
6. `AGENTS.md` 受 `project_doc_max_bytes = 65536` 约束。`.agents/skills/` 的 L1/L2 与教学 QMD 体量由 `check_skill_size.py` 强制；知识库 Parent Token 由 `kb-check` 强制。
7. 长任务每轮推进一个可验证子目标。Plan Mode 严格只读，不得写文件、编译、渲染，也不得调用 `project_edit`、`project_build`、`project_verify` 或 `project_render`。只有用户发来新的明确批准消息后才进入执行；压缩摘要、重复的原始需求、计划完成标记、自动续跑和任务摘要都不算批准。上下文压缩后重读本文件与 `git status`，但仍在 Plan Mode 时只继续规划。执行阶段每轮按改动域运行一次 `run.ps1 check --profile ...`，跨域或发布收口再运行 `full`。排查失败或异常时才读 `.agents/incidents/INDEX.md`，其余时刻不读 incidents；每个任务开始时可读 `.agents/memory/MEMORY.md` 索引防重复踩坑。
8. Git 对比服务于审查、冲突解决、发布和最近改动调试。普通文档任务不重复运行。

## Python 运行时

所有仓库脚本直接读取根目录 `config.toml` 中的 `python`。Skills、MCP 与维护命令不得另行读取 `CPP_MEMO_PYTHON`、`runtime.json.python`、PATH 或 `sys.executable` 作为项目 Python 来源。MCP 配置仍指向 `.agents/mcp/server.py`，由该 server 读取同一字段。

## 初始化兼容

Codex 或其他工具重新生成规则时必须合并本文件，不得覆盖项目结构、命令、安全约束和读取边界。`AGENTS.md` 是唯一项目级总入口，宿主专用文件只能引用它。
