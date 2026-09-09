---
name: python-tools
description: 当任务需要运行、维护或迁移本仓库 Python 工具、知识库管道、维护脚本或其配置时触发。
metadata:
  short-description: 运行与维护仓库 Python 工具链
---

# Skill: python-tools

管本仓库 Python 脚本、知识库管道与运行时选择；检查项编排交给 `agent-ops`，知识正文交给 `knowledge/`。

## 适用场景

- 运行或修改 `scripts/` 下的知识库管道、脚手架与维护脚本，调整 Python 版本与格式化配置。
- **不适用**：检查顺序与子命令编排（转 `agent-ops`）、领域结论（转 `knowledge/`）。

## 任务路由

| 要做的事 | 读取 |
| --- | --- |
| 知识库管道（分块 / 索引 / 检索 / 评测 / 体检） | `scripts/`，规范见 `../../../knowledge/README.md` |
| 忽略规则与索引边界 | `references/ignore-rules.md` |
| Python 版本与格式化配置 | `assets/config/pyproject.toml` |
| 新建章节工程脚手架 | `scripts/scaffold/init_project.py` |

## P0 硬约束

1. 仓库检查一律走 `.cursor/skills/agent-ops/scripts/run.py`，不绕过它直接串脚本。
2. 运行时按固定顺序：`CPP_MEMO_PYTHON` → `assets/config/runtime.json`（可选的本机文件，已被 `.gitignore` 忽略）→ PATH；候选全部不可用时立即中止，不伪造结果。
3. 知识库正文只在根 `knowledge/`，索引产物只在 `temp/knowledge-index/`（不入库）。
4. 脚本改动后同步更新 `AGENTS.md` 命令表与 `run.py` 子命令说明。

## 工作流程

1. 先确认脚本归属目录（`scripts/`、`scripts/render/`、`scripts/scaffold/`、`scripts/maintenance/`）。
2. 用受控 Python 运行最小复现命令，失败才加 `--verbose`。
3. 改知识库管道后依次跑 `kb-index --rebuild`、`kb-check`、`kb-eval`。

## 完成判据

- [ ] `python -m compileall .cursor` 通过，`run.py check` 全通过。
- [ ] 相关 `test_*.py` 通过；未新增顶层脚本目录或空目录。
