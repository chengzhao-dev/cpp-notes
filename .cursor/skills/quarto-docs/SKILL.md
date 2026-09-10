---
name: quarto-docs
description: 编写结构清晰、可验证、适合 HTML 阅读的 Quarto 中文技术文档。涉及 QMD、README、章节润色和渲染时使用。
metadata:
  short-description: 编写可验证的中文 Quarto 文档
---

# Skill: quarto-docs

负责页面结构、中文表达与多文件协作；C++ 语义交给 `cpp-content`，主题样式交给 `quarto-theme`。按路由只读所需 reference，不整包加载。

## 适用场景

- 新写或润色 `.qmd` 正文、标题、代码块、终端命令、图表与 Callout，以及 `README.md`、`AGENTS.md` 体例。
- **不适用**：渲染参数取值与设计令牌（转 `quarto-theme`）、C++ 语义正确性（转 `cpp-content`）。

## 任务路由

| 要做的事 | 读取 |
| --- | --- |
| 所有中文文档任务（最高优先） | `references/zh/writing-principles.md` |
| 正文结构、文档元素与终端命令块 | `references/quarto/authoring.md`、`references/quarto/terminal-validation.md` |
| 章节组织 / C++ 章节专项 | `references/zh/writing-style-core.md`、`references/zh/cpp-chapter-writing.md` |
| Book 结构、front matter、标题层级 | `references/quarto/basics.md` |
| HTML 取值与渲染排错（编号索引，按症状定位） | `references/quarto/rendering-and-output.md` |
| 措辞、案例与页面组织依据（为什么这么排） | `run.py kb-search "块序列"`、`"卡片"`、`"措辞"`，均加 `--domain quarto-docs` |

## P0 硬约束

1. 标题只由 YAML `title:` 提供，页面内不再写同文本 `# H1`；小节从 `##` 开始，不手填序号，`##`/`###` 前不写 `---` 水平线。
2. 代码块用普通语言围栏 `cpp`/`bash`/`powershell`/`cmake`；Mermaid 必须用 `{mermaid}` 围栏；`{{< include >}}` 整体放进带语言名的围栏。
3. Callout 只用内置 5 类，自定义类会被静默丢弃。
4. 正文只承诺实际提供且能验证的内容，标题后第一句直接兑现承诺。
5. 中文 `.qmd`、Skill 与主题 CSS 使用 UTF-8 无 BOM、LF，改后先跑编码检查。

## 工作流程

1. 多文件修改先定页面角色：入口只回答「这是什么、从哪开始」，索引只安排顺序，正文负责一个可完成任务。
2. 跑 `run.py scope <part>/<chapter>`，按路由读取该主题需要的 reference；章节骨架用 `../cpp-content/templates/cpp-topic.qmd`。
3. 逐节核对围栏、标题层级、链接与输出一致性；影响渲染时跑 `run.py render`，日常收口只跑 `run.py check`。

## 完成判据

- [ ] `run.py check` 全通过（含 `docs`、`callouts`、`links`、`encoding`）。
- [ ] 交叉引用锚点可达、本地文件引用存在；术语、命令与详略在多文件间一致。
