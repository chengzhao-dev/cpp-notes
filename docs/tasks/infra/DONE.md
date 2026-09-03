# 基建任务（已完成）

TASK-INFRA-001 ~ 007 全部完成，逐条任务单不再单独保留（内容已被后续重构覆盖，保留只会让 agent 误读过期边界）。要点记录如下，细节以 `git log` 与现行文件为准。

| ID | 任务 | 关键产出 |
|---|---|---|
| INFRA-001 | Skill 迁移 | 建立 `.cursor/skills/` 四域；cases 合并；`writing-style-core.md` |
| INFRA-002 | 删除 opencode | 移除 `.opencode/` 与其引用 |
| INFRA-003 | docs 框架 | `structure.md`、`tasks/INDEX.md`、`agent/` |
| INFRA-004 | 脚本收尾 | `init_project.py` bare/simple；取消 cpp-project skill |
| INFRA-004b | Python 规范 | Black + 中文注释约定（现并入 `docs/agent/ops.md`） |
| INFRA-005 | CI 校验 | `render-check.yml` 跑 `verify_examples.py` |
| INFRA-006 | 精简合并 | 删 assets 与 full 模板；misc.css 并入 base.css |
| INFRA-007 | 内容精简 | `writing-style-core`；setup-wsl2 ≤180 行 |

## 2026-09 增补（Skills 重构 v4）

- 三层加载契约：`AGENTS.md`（L0 路由）→ `SKILL.md`（L1）→ `references/*`（L2 原子），体积由 `scripts/agent/check_skill_size.py` 强制。
- 任务作用域解析器 `scripts/agent/scope.py`：一次给出 UNIT/READ/DENY，`code/**/build/` 永不入上下文。
- 命令统一入口 `scripts/agent/run.py`：批处理校验、terse 输出、绕开 PowerShell 引号/GBK 重试。
- 产物契约 `scripts/agent/check_dom_contracts.py`：复制按钮 hover、触屏兜底、打印不隐藏、favicon。
- 开发环境落地：根 `.editorconfig` / `.clang-format` / `.clangd` / `.vscode/`。
- `authoring.md`（239 行）拆为 `authoring.md` + `authoring-elements.md`；`render-ops.md` + `python-scripts.md` 合并为 `ops.md`；删除死模板 `chapter.qmd`、`api-doc.qmd`。