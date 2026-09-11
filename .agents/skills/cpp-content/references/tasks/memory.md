# memory 章节任务矩阵

本文件是 memory 全部章节任务的唯一权威记录：一行一章，读写边界与验收在文件级统一，只有差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。

## 公共读写边界

- **必读**: `AGENTS.md`；本文件；`.agents/skills/cpp-content/references/cpp/modern-cpp.md`；`.agents/skills/quarto-docs/references/quarto/authoring.md`；`.agents/skills/quarto-docs/references/zh/writing-style-core.md`
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
| `TASK-MEM-001` | stack-heap | todo | `TASK-CORE-007` | `content/memory/stack-heap.qmd` | `code/memory/stack-heap.cpp` | — | — |
| `TASK-MEM-002` | raii | todo | `TASK-MEM-001` | `content/memory/raii.qmd` | `code/memory/raii.cpp` | — | — |
| `TASK-MEM-003` | smart-pointers | todo | `TASK-MEM-002` | `content/memory/smart-pointers.qmd` | `code/memory/smart-pointers.cpp` | — | — |
| `TASK-MEM-004` | move-semantics | todo | `TASK-MEM-003` | `content/memory/move-semantics.qmd` | `code/memory/move-semantics.cpp` | — | — |
