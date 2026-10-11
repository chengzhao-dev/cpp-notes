---
name: writing-quarto
description: 编写结构清晰、可验证、适合 HTML 阅读的 Quarto 中文技术文档。涉及 QMD、README、章节润色和渲染时使用。
metadata:
  short-description: 编写可验证的中文 Quarto 文档
---
# Skill: writing-quarto
负责页面结构、中文表达与多文件协作。C++ 语义交给 `writing-cpp`，主题样式交给 `designing-theme`。按路由只读所需 reference，不整包加载。
## 适用场景

- 新写或润色 `.qmd` 正文、标题、代码块、终端命令、图表与 Callout，以及 `README.md`、`AGENTS.md` 体例。
- 全局环境约定只在入门分册声明一次，其它分册的首页与章节正文都不重复；自测题答案统一使用 `.answer`，由 Lua filter 默认收起。
- **不适用**：渲染参数取值与设计令牌（转 `designing-theme`）、C++ 语义正确性（转 `writing-cpp`）。

## 任务路由

| 要做的事 | 读取 |
| --- | --- |
| 所有中文文档任务（最高优先） | `references/zh/writing-principles.md` |
| 章节组织、页面骨架与新手术语门槛 | `references/zh/chapter-writing.md` |
| 正文结构、文档元素与终端命令块 | `references/quarto/authoring.md`、`references/quarto/terminal-validation.md`；递进片段合并等元素细则见知识 `cpp-quarto-qmd-element-cases-v1` |
| 小节密度、Callout 和排错结构 | 知识 `cpp-quarto-section-density-v1` |
| Book 结构、front matter、标题层级与 H2/H3 判定 | `references/quarto/basics.md` |
| HTML 取值与渲染排错（编号索引，按症状定位） | `references/quarto/rendering-and-output.md` |
| 页面组织、措辞、预算与全仓重构 | `run.py kb-search "页面结构 措辞" --domain quarto-writing`；预算见 `cpp-quarto-chapter-structure-v1`「分层上限」，全仓流程见 `references/quarto/repository-wide-refactor.md`。 |

## P0 硬约束
1. 标题只由 YAML `title:` 提供，页面内不再写同文本 `# H1`。小节从 `##` 开始，不手填序号，`##`/`###` 前不写 `---` 水平线。
2. 代码块用属性围栏 `{.cpp filename="main.cpp"}`。`filename` 写运行环境或真实文件名，正文不重复环境说明。完整源码必须直接内联在正文的带语言标注代码围栏中，禁止使用 `{{< include >}}`；`code/` 只供编译验证，不向 qmd 嵌入。递进依赖的同源片段必须合并为一个围栏；「片段 + 完整示例」成对与多源文件各一块是显式豁免，判定见知识 `cpp-quarto-qmd-element-cases-v1`。复杂关系若确需 Mermaid 才使用 `{mermaid}` 围栏；坐标轴类网格图仅当用户明确指定时走绘图助手加 `{python}` 单元（口径见知识 `cpp-coords-diagram-v1`），不用 Mermaid 硬画。
3. Callout 只用内置 5 类，自定义类会被静默丢弃。正文只承诺实际提供且能验证的内容，标题后第一句直接兑现承诺；一段只推进一个对象，对象切换必须新起段并用一句关系衔接。
4. 中文 `.qmd`、Skill 与主题 CSS 使用 UTF-8 无 BOM、LF，改后先跑编码检查。正文只呈现正确流程，warning/error 移入专门章节或短 callout。常见错误的完整格式以 `references/quarto/terminal-validation.md` 为准，本文件不复制三步模板。
5. `##` 下不强制写导语，首个段落或 `###` 可以直接开始任务，导语不得复述标题。代码块前的完整动作句用 `。`，使用“如下、以下、例如”直接引出块内容时用 `：`；围栏内 `//` / `#` 注释已写明的意图，块后正文不得同义复述，只写注释没覆盖的新信息（对照见知识 `cpp-quarto-chinese-style-v1`）。节导语与引用块限额由 `check_content_budget.py` 按知识 `cpp-quarto-chapter-structure-v1`「分层上限」执行。
6. 代码块与 `{mermaid}`/`{python}` 图之间必须有桥接正文（固定序列见 `references/quarto/authoring.md`「代码与图的桥接」）；有项目解释时解释紧跟代码块，不得插队到图后。图遵守一图一事、同主题相邻、不承载新信息，主题错位拆 `###`。正文写可观察对象与完整主谓句，禁用「契约链」「状态外壳」「地基」「闭环」「消费」等压缩隐喻与电报省略（对照见知识 `cpp-quarto-chinese-style-v1`）。
7. 跨仓外链默认零条：禁止「写法依据见」等突兀句挂 cpp-board-games；可选尾置「若要系统阅读…」（细则见 `references/zh/chapter-writing.md`）。正文禁课堂类比与「公共头」缩略，头文件指称写具体对象或「库对外头文件」（细则见同文件「叙事边界」）。

## 工作流程

1. 多文件修改先定页面角色：入口只回答「这是什么、从哪开始」，索引只安排顺序，正文负责一个可完成任务。
2. 跑 `run.ps1 scope <part>/<chapter>`，按路由读取该主题需要的 reference。章节骨架用 `../writing-cpp/templates/cpp-topic.qmd`。
3. 逐节核对围栏、标题层级、链接与输出一致性。删改正文后按 `authoring.md` 回读切口，检查动作、因果、指代和验收是否仍扣合。影响渲染时跑 `run.ps1 render`，日常收口只跑 `run.ps1 check`。
## 完成判据
- [ ] `run.ps1 check` 全通过（含 `docs`、`callouts`、`links` 与 `encoding`，有 `_book/` 时另含 `layout` 与 `dom`）。
- [ ] 交叉引用锚点可达、本地文件引用存在。术语、命令与详略在多文件间一致。
