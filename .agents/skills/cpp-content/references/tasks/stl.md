# stl 章节任务矩阵

本文件是 stl 全部章节任务的唯一权威记录：一行一章，读写边界与验收在文件级统一，只有差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。

## 公共读写边界

- **必读**: `AGENTS.md`、本文件、`.agents/skills/cpp-content/references/cpp/stl.md`、`.agents/skills/quarto-docs/references/quarto/authoring.md`、`.agents/skills/quarto-docs/references/zh/writing-style-core.md`
- **可写**: 本行「正文」与「示例」所列路径，以及 `_quarto.yml`（追加本章）
- **禁止**: `.agents/skills/quarto-theme/assets/theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

示例默认单文件 `code/<part>/<chapter>.cpp`，需要构建工程时改用同名子目录，产物落其 `build/`。

## 统一验收（每章完成时逐项确认）

- [ ] 正文符合体量预算，`run.py check` 与 `run.py render` 通过
- [ ] 示例经 `run.py verify --changed` 编译通过，正文承诺的输出与实测一致
- [ ] 本文件「状态」列已更新为 `done`

## 任务矩阵

| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `TASK-STL-001` | intro-stl | todo | `TASK-CORE-005` | `content/stl/intro-stl.qmd` | `code/stl/intro-stl.cpp` | — | — |
| `TASK-STL-002` | vector | todo | `TASK-STL-001` | `content/stl/vector.qmd` | `code/stl/vector.cpp` | — | — |
| `TASK-STL-003` | map-set | todo | `TASK-STL-002` | `content/stl/map-set.qmd` | `code/stl/map-set.cpp` | — | — |
| `TASK-STL-004` | iterators | todo | `TASK-STL-002` | `content/stl/iterators.qmd` | `code/stl/iterators.cpp` | — | — |
| `TASK-STL-005` | algorithms | todo | `TASK-STL-004` | `content/stl/algorithms.qmd` | `code/stl/algorithms.cpp` | — | — |
