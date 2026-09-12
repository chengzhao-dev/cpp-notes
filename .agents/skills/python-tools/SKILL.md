---
name: python-tools
description: 当任务需要运行、维护或迁移本仓库 Python 工具、知识库管道、维护脚本或其配置时触发。
metadata:
  short-description: 运行与维护仓库 Python 工具链
---

# Skill: python-tools

管本仓库 Python 脚本、知识库管道与运行时选择。检查项编排交给 `agent-ops`，知识正文交给 `knowledge/`。

## 适用场景

- 运行或修改 `scripts/` 下的知识库管道、脚手架与维护脚本，调整 Python 版本与格式化配置。
- **不适用**：检查顺序与子命令编排（转 `agent-ops`）、领域结论（转 `knowledge/`）。

## 任务路由

| 要做的事 | 读取 |
| --- | --- |
| 知识库管道（分块 / 索引 / 检索 / 评测 / 体检） | `scripts/`，规范见 `../../../knowledge/README.md` |
| Python 版本与格式化配置 | `assets/config/pyproject.toml` |
| 新建章节工程脚手架 | `scripts/scaffold/init_project.py` |
| 重建或校验章节任务矩阵 | `scripts/maintenance/generate_tasks.py --check`（漂移时 `--write`） |

## P0 硬约束

1. 仓库检查一律走 `.agents/skills/agent-ops/scripts/run.py`，不绕过它直接串脚本。
2. 运行时只读取 `.agents/manifest.json` 的 `mcp.command`；不得使用 `CPP_MEMO_PYTHON`、`runtime.json.python`、PATH 或 `sys.executable` 回退。字段缺失、路径不可执行或 Python 版本不足时立即中止，不伪造结果。
3. 知识库正文只在根 `knowledge/`。所有项目临时产物（包括脚本测试、测量和基准的中间文件）统一写在 `temp/<用途>/`，索引产物写在 `temp/knowledge-index/`（均不入库）。
4. 作用域、检索和索引统一跳过构建产物、Quarto 缓存、依赖目录、Python 缓存与密钥文件。规则来源是根目录 `.gitignore`，不再依赖 `.agents/ignore` 或 `.agents/indexingignore`。
5. 脚本改动后同步更新 `AGENTS.md` 命令表与 `run.py` 子命令说明。

## 工作流程

1. 先确认脚本归属目录（`scripts/`、`scripts/render/`、`scripts/scaffold/`、`scripts/maintenance/`）。
2. 用受控 Python 运行最小复现命令，失败才加 `--verbose`。
3. 改知识库管道后依次跑 `kb-index --rebuild`、`kb-check`、`kb-eval`。

## 完成判据

- [ ] `python -m compileall .agents` 通过，`run.py check` 全通过。
- [ ] 相关 `test_*.py` 通过。未新增顶层脚本目录或空目录。
