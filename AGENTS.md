# AGENTS.md

**C++ 笔记** Quarto Book：面向新手的 Linux C++ 渐进式中文教程。框架见 [`docs/structure.md`](docs/structure.md)。

## Skills（`.cursor/skills/`）

| 领域 | Skill |
|---|---|
| 写作 / qmd | `quarto-docs` |
| C++ 内容与示例 | `cpp-content` |
| HTML 主题 | `quarto-theme` |
| GitHub / 发布 | `github-ops` |

## 常用命令

```bash
quarto render          # → _book/
quarto preview         # 热更新（Windows 偶发卡死，见 docs/agent/render-ops.md）
git push               # Actions → Pages
```

## Python 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/cpp/init_project.py` | 最小 CMake 工程（bare/simple） |
| `scripts/build/defer-mermaid.py` | CI：mermaid 懒加载 |

解释器：`scripts/config/python.json` → `CPP_MEMO_PYTHON` → 自动搜索（≥3.9）。格式用 Black，细则 [`docs/agent/python-scripts.md`](docs/agent/python-scripts.md)。

Skill 内脚本：`verify_examples.py`、`scaffold_chapter.py`、`check_*`。

## 目录职责

| 路径 | 职责 |
|---|---|
| `content/` | 章节 `.qmd` |
| `code/` | 示例 `.cpp` |
| `theme/` | SCSS + CSS + includes + 自托管字体 |
| `scripts/` | 仓库级 Python（`cpp/`、`build/`、`maint/`、`config/`） |
| `docs/` | 框架、任务清单、Agent 运维细则 |
| `.cursor/skills/` | Cursor 项目 skills |

## 任务清单

按章隔离写作：[`docs/tasks/INDEX.md`](docs/tasks/INDEX.md)。

## 规范指针

写作 → `quarto-docs` · 主题 → `quarto-theme` · C++ → `cpp-content` · Git → `github-ops`

渲染排错 → [`docs/agent/render-ops.md`](docs/agent/render-ops.md)

## 仓库格式

文本 LF、UTF-8 无 BOM（`.gitattributes`）。
