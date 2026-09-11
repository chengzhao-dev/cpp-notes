# getting-started 章节任务矩阵

本文件是 getting-started 全部章节任务的唯一权威记录：一行一章，读写边界与验收在文件级统一，只有差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。

## 公共读写边界

- **必读**: `AGENTS.md`；本文件；`.agents/skills/quarto-docs/references/quarto/authoring.md`；`.agents/skills/quarto-docs/references/zh/writing-style-core.md`
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
| `TASK-ENV-001` | setup-wsl2 | done | — | `content/getting-started/setup-wsl2.qmd` | —（本章无示例） | `.agents/skills/cpp-content/references/cpp/engineering.md` | — |
| `TASK-ENV-002` | install-toolchain | merged | `TASK-ENV-001` | —（不新建） | — | — | 已并入 ENV-001 的「安装 C++ 构建工具链」一节，勿再新建同名 qmd |
| `TASK-ENV-003` | first-program | done | `TASK-ENV-001` | `content/getting-started/first-program.qmd` | `code/getting-started/first-program/` | `.agents/skills/cpp-content/references/cpp/cpp.md` | 先 g++ 直编，再最小 CMakeLists；多文件与目标留给 cmake-intro |
| `TASK-ENV-004` | cmake-intro | todo | `TASK-ENV-003` | `content/getting-started/cmake-intro.qmd` | `code/getting-started/cmake-intro.cpp` | `.agents/skills/cpp-content/references/cpp/engineering.md` | — |
