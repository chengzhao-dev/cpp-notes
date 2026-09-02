---
name: quarto-docs
description: 用 Quarto Book 编写与发布技术文档。涉及 .qmd、_quarto.yml、章节写作、中文润色、渲染排查时使用。C++ 见 cpp-content，主题见 quarto-theme，GitHub 见 github-ops。默认中文。
---

# Skill: quarto-docs

Quarto Book 写作方法论。参照 [learncpp.com](https://www.learncpp.com/)。

## 任务路由（[docs/tasks/INDEX.md](../../../docs/tasks/INDEX.md)）

| 任务 | 必读 |
|---|---|
| 写/改章节 | `references/quarto/authoring.md` + `references/zh/writing-style-core.md` |
| 润色 | + `references/zh/avoid-words.md` |
| 改 Book 结构 | `references/quarto/basics.md` |
| HTML 选项 | `references/quarto/html-output.md` |
| 渲染排错 | `references/quarto/pitfalls.md`；运维见 `docs/agent/render-ops.md` |
| 案例（按需） | `references/zh/cases/*.md` |

**禁止**：写章时读 `theme/css/*`。

## 常见错误（Do / Don't）

| ✗ | ✓ |
|---|---|
| YAML `title:` + 同文本 `# H1` | 只用 `title:`，小节从 `##` |
| 代码块 `{.cpp}` | 普通围栏 `cpp` |
| 终端用 `PS>` | 演示块统一 `$` |
| 普通章写 `description:` | 仅 index/part 封面 |
| 漏 `---` 分节线 | 每 ##/### 前 `---`（上下空行） |

## 脚本

- `scripts/check_ascii_names.py` — 文件名 ASCII
- `scripts/check_skill_links.py` — skill 内链

章节骨架：`.cursor/skills/cpp-content/templates/cpp-topic.qmd` + `scaffold_chapter.py`。

## 分工

C++ → `cpp-content`；脚手架 → `scripts/cpp/init_project.py`；主题 → `quarto-theme`；Git → `github-ops`。
