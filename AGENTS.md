# C++ Notes Agent 工作标准

本文件是 C++ Notes 的唯一项目级 Agent 入口。它先规定所有 Codex 和通用 Coding Agent 必须遵守的工作标准，再把这些标准落到本仓库的内容、代码、工具和验收边界。

## 工作标准

- 先理解目标、现状和约束。明确假设。存在多种解释时列出选项，不擅自扩大范围。
- 用最少、最清晰、可验证的改动解决问题。不做无关重构，不为一次性需求设计扩展框架。
- 修改前先定位入口、引用、测试和权威规则。保留用户已有改动，只清理由本次改动产生的孤儿代码。
- 把需求转成验收标准：先复现或建立检查，再实现，最后运行与风险匹配的验证。
- 默认简洁输出，说明做了什么、如何验证、未完成项和风险。不回显密钥、凭据、`.env` 或无关个人信息。
- 维护仓库规范时保持单一权威出处。流程和格式放 skill/reference，领域原因放 `knowledge/`。
- 构建配置和脚本的版本规则见 `cpp-content` 的代码风格 reference。QMD 代码块、`include` 文件和正文标点规则见 `quarto-docs` 对应 reference。

## C++ Notes 项目

这是面向初学者的中文 Linux C++ Quarto Book。正文在 `content/`，与章节对应的 C++ 示例和工程在 `code/`，领域依据在 `knowledge/`，Agent skills、脚本、主题资源和项目 MCP 在 `.agents/`。

| 路径 | 职责 |
| --- | --- |
| `content/<part>/` | Quarto 章节正文 |
| `code/<part>/` | 单文件示例或同名工程，`build/` 是产物 |
| `.agents/skills/` | Codex 项目 skills、references、任务矩阵和工具脚本 |
| `.agents/mcp/` | 项目级 MCP stdio server 与说明，由宿主显式配置，不假设自动发现 |
| `.agents/skills/quarto-theme/assets/theme/` | 页面主题、样式和字体资源 |
| `knowledge/` | 回答“为什么”的精简领域知识库 |
| `temp/` | 索引和分析产物，不入库 |

章节、示例和任务矩阵按相同的 part/chapter 对齐。任务矩阵 `.agents/skills/cpp-content/references/tasks/<part>.md` 是状态与读写边界的唯一出处。

## 常用命令

以下命令统一由 `.agents/manifest.json` 的 `mcp.command` 指定 Python 解释器执行。该字段是仓库唯一 Python 来源；缺失、不可执行或版本不足时立即停止，不回退到 PATH、环境变量或其他配置。

| 命令 | 用途 |
| --- | --- |
| `python .agents/skills/agent-ops/scripts/run.py scope <目标>` | 输出最小读取作用域 |
| `python .agents/skills/agent-ops/scripts/run.py check` | 批量运行编码、文档、主题和产物检查 |
| `python .agents/skills/agent-ops/scripts/run.py render` | 渲染 Book 并自动检查 |
| `python .agents/skills/agent-ops/scripts/run.py verify --changed` | 增量校验 C++ 示例 |
| `python .agents/skills/agent-ops/scripts/run.py build <part>/<chapter>` | 在 WSL 构建单章示例 |
| `python .agents/skills/agent-ops/scripts/run.py kb-index [--rebuild]` | 构建知识库索引 |
| `python .agents/skills/agent-ops/scripts/run.py kb-check` | 检查知识库结构与检索延迟 |

## 读取、编辑与验收边界

1. 每次任务先运行 `scope`，只读 UNIT、READ 和必要 reference。不整包读取 references。
2. 永不读取或索引 `_book/**`、`code/**/build/**`、`.quarto/**`、`.cache/**`、`.tmp/**`。产物检查交给脚本。
3. 预计读取超过 8 个文件或需要全仓检索时才派侦察代理。编辑回主线程完成。
4. 中文文件使用 UTF-8 无 BOM、LF。修改 `.qmd`、skill 或主题 CSS 后先跑编码检查。QMD 正文标点和句长遵循 `quarto-docs/references/zh/writing-principles.md`。
5. 修改 `.agents/skills/quarto-theme/assets/theme/**` 或 `_quarto.yml` 会触发整本渲染。确认代价后运行 `render`。
6. `AGENTS.md` 受 `project_doc_max_bytes = 65536` 约束。`.agents/skills/` 的 L1/L2 体量由 `check_skill_size.py` 强制。
7. 长任务每轮推进一个可验证子目标。上下文压缩后重读本文件与 `git status`。每轮用一次 `run.py check` 收口。
8. Git 对比服务于审查、冲突解决、发布和最近改动调试。普通文档任务不重复运行。

## Python 运行时

所有仓库脚本直接读取 `.agents/manifest.json` 中的 `mcp.command`。Skills、MCP 与维护命令不得另行读取 `CPP_MEMO_PYTHON`、`runtime.json.python`、PATH 或 `sys.executable` 作为项目 Python 来源。MCP 配置仍指向 `.agents/mcp/server.py`，由该 server 读取同一字段。

## 初始化兼容

Codex 或其他工具重新生成规则时必须合并本文件，不得覆盖项目结构、命令、安全约束和读取边界。`AGENTS.md` 是唯一项目级总入口，宿主专用文件只能引用它。
