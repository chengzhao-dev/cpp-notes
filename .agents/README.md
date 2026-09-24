# Agent 工作区

`.agents/` 是本项目 Agent 资源的唯一工作区。根目录 `AGENTS.md` 只保留项目级硬约束；本文件负责定位，不重复规则。

## 按任务进入

| 任务 | 入口 |
| --- | --- |
| 运行检查、维护脚本、调整 MCP 或重构 Agent 目录 | `skills/agent-ops/SKILL.md` |
| 编写或验证 C++ 示例、工程和任务矩阵 | `skills/cpp-content/SKILL.md` |
| 运行知识库索引、检索、评测和 Python 工具 | `skills/python-tools/SKILL.md` |
| 编写 Quarto 文档和检查 Markdown/QMD | `skills/quarto-docs/SKILL.md` |
| 调整主题、布局和页面资源 | `skills/quarto-theme/SKILL.md` |
| GitHub、提交和发布边界 | `skills/github-ops/SKILL.md` |
| 只读代码审查 | `skills/code-review/SKILL.md` |

完整短路由见 `skills/catalog.md`。

## 目录职责

```text
.agents/
├── knowledge/       # 稳定领域事实与“为什么”，按 skill/domain 组织
├── mcp/             # 项目级 MCP server 与说明
├── skills/          # 可复用流程；每个 skill 的脚本只放在其 scripts/ 下
│   └── <skill>/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
└── README.md        # 本导航
```

知识库索引产物写入根目录 `temp/knowledge-index/`，不进入 `.agents/`，也不入库。不要把临时计划、构建产物或缓存放进本目录。

## 运行入口

统一入口是 `skills/agent-ops/scripts/run.ps1`，Python 解释器唯一来源是根目录 `config.toml` 的 `python`。常用命令：

```powershell
& .agents/skills/agent-ops/scripts/run.ps1 scope <目标>
& .agents/skills/agent-ops/scripts/run.ps1 check --profile fast|knowledge|python|full
& .agents/skills/agent-ops/scripts/run.ps1 kb-index [--rebuild]
& .agents/skills/agent-ops/scripts/run.ps1 kb-search <查询>
```

脚本不得从当前工作目录推断仓库根；移动或新增脚本后，必须检查 `Path(__file__)` 的根目录解析，并更新所有统一入口、测试和文档引用。
