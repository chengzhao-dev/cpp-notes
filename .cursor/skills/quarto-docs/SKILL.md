---
name: quarto-docs
description: 用 Quarto Book 编写与发布技术文档。涉及 .qmd、_quarto.yml、章节写作、中文润色、渲染排查时使用。C++ 见 cpp-content，主题见 quarto-theme，GitHub 见 github-ops。默认中文。
---

# Skill: quarto-docs

Quarto Book 写作方法论。体例参照 [learncpp.com](https://www.learncpp.com/)。
全部 reference 的全景索引见 `../_CATALOG.md`；**一次任务只读路由指向的那一个文件**。

## 任务路由

| 任务 | 必读 |
|---|---|
| 写/改章节正文 | `references/quarto/authoring.md` + `references/zh/writing-style-core.md` |
| 章里放图/表/Callout/FAQ/交叉引用 | `references/quarto/authoring-elements.md` |
| 润色 | + `references/zh/avoid-words.md` |
| 改 Book 结构 / front matter | `references/quarto/basics.md` |
| HTML 输出选项 | `references/quarto/html-output.md` |
| 渲染排错 | `references/quarto/pitfalls.md`；运维见 `docs/agent/ops.md` |
| 需要范例 | `references/zh/cases-index.md`，再按需读单个 `cases/*.md` |

**禁止**：写章时读 `theme/css/*`；整包读 references；为「了解一下」而多读。

## 常见错误（Do / Don’t）

| ✗ | ✓ |
|---|---|
| YAML `title:` + 同文本 `# H1` | 只用 `title:`，小节从 `##` |
| 代码块 `{.cpp}` | 普通围栏 `cpp` |
| 终端用 `PS>` | 演示块统一 `$` |
| 普通章写 `description:` | 仅 index/part 封面 |
| 在 `##`/`###` 前写 `---` 水平线 | H2 靠默认下边框分隔，小节前不写 `---` |
| `::: {.callout-best-practice}` 等自定义类 | 内置 5 类 + 块内 `## 标题`；自定义类会被静默丢弃（`pitfalls.md` #12） |

## 脚本

- `scripts/check_ascii_names.py` — 文件名 ASCII
- `scripts/check_skill_links.py` — skill 内链
- `scripts/check_callouts.py` — 产物 callout 结构（需先渲染）
- 章节骨架：`../cpp-content/templates/cpp-topic.qmd` + `../cpp-content/scripts/scaffold_chapter.py`

批量校验统一走 `python scripts/agent/run.py check`，不要逐个脚本分别调用。
