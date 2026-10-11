---
kb_id: "cpp-coords-diagram-v1"
title: "坐标轴网格图的生成约定"
domain: "quarto-writing"
subdomain: "rendering"
tags: [coords, diagram, python-cell, svg, jupyter, quarto]
level_range: [0, 5]
dependencies: ["cpp-mermaid-conventions-v1"]
created: "2026-09-29"
updated: "2026-09-29"
chunk_strategy: "semantic_heading"
estimated_tokens: 700
---

# 坐标轴网格图的生成约定

坐标轴类网格图用共享绘图助手生成 SVG，不用 Mermaid 硬画网格。本仓与姊妹仓库 cpp-board-games 同口径；助手的完整 API、解释器与 CI 依赖见该仓标识 `bg-coords-diagram-v1` 的知识文件。

## 与 Mermaid 的分工

- 默认图是 `{mermaid}` flowchart，表达流程、分层与调用链（口径见标识 `cpp-mermaid-conventions-v1` 的知识文件）。
- 坐标轴类网格图只走绘图助手加 `{python}` 可执行单元；禁止用 Mermaid 拼棋盘或网格。
- Agent 作图边界：默认只生成 Mermaid 流程图；坐标图仅当用户明确指定时生成，且只改助手调用参数，不内联第二套 SVG 逻辑。

## 本仓的采用边界

- 本仓正文当前无可执行单元；引入坐标图时按姊妹仓同一约定写页面与单元。
- 页面 frontmatter 开 `engine: jupyter`，单元块首写 `#| echo: false`、`#| warning: false`，再写 `#| fig-cap: "图 N：…"` 与 `#| fig-align: center`；图注概括图意，图后正文不复述图注，也不用 `>` 引用块另起一套图注。
- 助手按程序坐标系作图（`axis=True` 默认开）：横轴 `col` 向右、纵轴 `row` 向下增长的带箭头轴，左上格外角带原点记号，与代码字段 `Position::row` / `Position::col` 对应；箭头与原点的语义以姊妹仓标识 `bg-coords-diagram-v1` 的知识文件为准。
- 解释器仍只认根目录 `config.toml` 的 python，经 `QUARTO_PYTHON` 注入（`run.py` 已处理）；首次引入单元时，在同一文件的 `quarto_python_packages` 声明依赖，并由 `run.py install-quarto-deps` 在 CI 与本地安装。
- token 预算口径与姊妹仓一致：代码围栏、`{mermaid}` 与 `{python}` 单元不计 token，行数上限见标识 `cpp-quarto-chapter-structure-v1` 的知识文件「分层上限」。
