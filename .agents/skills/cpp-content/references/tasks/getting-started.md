# getting-started 章节任务矩阵

本文件是 getting-started 全部章节任务的唯一权威记录：一行一章，读写边界与验收在文件级统一，只有差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。

## 公共读写边界

- **必读**: `AGENTS.md`、本文件、`.agents/skills/quarto-docs/references/quarto/authoring.md`、`.agents/skills/quarto-docs/references/zh/chapter-writing.md`
- **可写**: 本行「正文」与「示例」所列路径，以及 `_quarto.yml`（追加本章）
- **禁止**: `.agents/skills/quarto-theme/assets/theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

示例默认单文件 `code/<part>/<chapter>.cpp`，需要构建工程时优先使用同名子目录；单入口 `main.cpp` 位置、`app/` 与库目录的布局边界以 `.agents/skills/cpp-content/references/cpp/engineering.md` 为准。一章需要多个独立工程时，在「示例」列登记全部路径，产物分别落各工程的 `build/`。

## 统一验收（每章完成时逐项确认）

- [ ] 正文符合体量预算，`run.py check --profile fast` 与 `run.py render` 通过
- [ ] 示例经 `run.py verify --changed` 编译通过，正文承诺的输出与实测一致
- [ ] 本文件「状态」列已更新为 `done`

## 任务矩阵

| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `TASK-ENV-001` | setup-wsl2 | done | — | `content/getting-started/setup-wsl2.qmd` | —（本章无示例） | `.agents/skills/cpp-content/references/cpp/engineering.md` | — |
| `TASK-ENV-002` | install-toolchain | merged | `TASK-ENV-001` | —（不新建） | — | — | 已并入 ENV-001 的「安装 C++ 构建工具链」一节，勿再新建同名 qmd |
| `TASK-ENV-003` | first-program | done | `TASK-ENV-001` | `content/getting-started/first-program.qmd` | `code/getting-started/first-program/` | `.agents/skills/cpp-content/references/cpp/cpp.md` | 目录含源码和一键脚本。脚本只使用 clang++ 直接编译单文件，不引入工程构建 |
| `TASK-ENV-004` | minimal-program-structure | done | `TASK-ENV-003` | `content/getting-started/minimal-program-structure.qmd` | `code/getting-started/minimal-program-structure/` | `.agents/skills/cpp-content/references/cpp/engineering.md`、`cpp-cpp-preprocessing-headers-linking-v1` | 用两源文件示例拆开 main、include、声明、实现、编译和链接 |
| `TASK-ENV-005` | cmake-project | done | `TASK-ENV-004` | `content/getting-started/cmake-project.qmd` | `code/getting-started/cmake-project/` | `.agents/skills/cpp-content/references/cpp/cmake-teaching.md` | 用 CMake 配置并构建单入口工程 |
| `TASK-ENV-006` | multi-file-project | done | `TASK-ENV-005` | `content/getting-started/multi-file-project.qmd` | `code/getting-started/multi-file-project/` | `.agents/skills/cpp-content/references/cpp/engineering.md` | 单个 app 目标。使用 include/ 与 src/ 组织多文件工程 |
| `TASK-ENV-007` | static-library | done | `TASK-ENV-006` | `content/getting-started/static-library.qmd` | `code/getting-started/static-library/` | `.agents/skills/cpp-content/references/cpp/engineering.md` | greeting/ 拥有静态库目标，根 main.cpp 构建消费它的 app |
| `TASK-ENV-008` | shared-library | done | `TASK-ENV-007` | `content/getting-started/shared-library.qmd` | `code/getting-started/shared-library/` | `.agents/skills/cpp-content/references/cpp/engineering.md` | greeting/ 拥有动态库目标，根 main.cpp 构建消费它的 app |
