# core 章节任务矩阵

本文件是 core 全部章节任务的唯一权威记录：一行一章，读写边界与验收在文件级统一，只有差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。

## 公共读写边界

- **必读**: `AGENTS.md`；本文件；`.agents/skills/cpp-content/references/cpp/cpp.md`；`.agents/skills/quarto-docs/references/quarto/authoring.md`；`.agents/skills/quarto-docs/references/zh/writing-style-core.md`
- **可写**: 本行「正文」与「示例」所列路径，以及 `_quarto.yml`（追加本章）
- **禁止**: `.agents/skills/quarto-theme/assets/theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

示例默认单文件 `code/<part>/<chapter>.cpp`；需要构建工程时改用同名子目录，产物落其 `build/`。

## 统一验收（每章完成时逐项确认）

- [ ] 正文符合体量预算，`run.py check` 与 `run.py render` 通过
- [ ] 示例经 `run.py verify --changed` 编译通过，正文承诺的输出与实测一致
- [ ] 本文件「状态」列已更新为 `done`

## 任务矩阵

| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `TASK-CORE-001` | intro | todo | `TASK-ENV-003` | `content/core/intro.qmd` | `code/core/intro.cpp` | — | — |
| `TASK-CORE-002` | variables | todo | `TASK-CORE-001` | `content/core/variables.qmd` | `code/core/variables.cpp` | — | — |
| `TASK-CORE-003` | operators | todo | `TASK-CORE-002` | `content/core/operators.qmd` | `code/core/operators.cpp` | — | — |
| `TASK-CORE-004` | control-flow | todo | `TASK-CORE-003` | `content/core/control-flow.qmd` | `code/core/control-flow.cpp` | — | — |
| `TASK-CORE-005` | functions | todo | `TASK-CORE-004` | `content/core/functions.qmd` | `code/core/functions.cpp` | — | — |
| `TASK-CORE-006` | arrays-strings | todo | `TASK-CORE-005` | `content/core/arrays-strings.qmd` | `code/core/arrays-strings.cpp` | — | — |
| `TASK-CORE-007` | structs-classes | todo | `TASK-CORE-006` | `content/core/structs-classes.qmd` | `code/core/structs-classes.cpp` | — | — |
| `TASK-CORE-008` | references | todo | `TASK-CORE-007` | `content/core/references.qmd` | `code/core/references.cpp` | — | — |
