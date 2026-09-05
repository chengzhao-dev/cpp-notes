# TASK-ENV-002 · 安装工具链

- **状态**: merged（并入 TASK-ENV-001）

## 结论

工具链安装已作为「安装 C++ 构建工具链」一节写进
[`content/getting-started/setup-wsl2.qmd`](../../../../content/getting-started/setup-wsl2.qmd)，
不单列成章：装 WSL2 与装编译器本就是同一次动手过程，拆两章会让新手在两页之间来回跳。

**不要再为本章新建** `content/getting-started/install-toolchain.qmd`。后续若工具链内容膨胀
（多编译器对照、版本管理、离线安装），再按「进阶/迁移独立成章」的规则拆出。
- **Skill**: cpp-content + quarto-docs
- **依赖**: TASK-001

## 读写边界

- **必读**: [`AGENTS.md`](../../AGENTS.md)；本文件；`.cursor/skills/quarto-docs/references/quarto/authoring.md`；`.cursor/skills/quarto-docs/references/quarto/authoring-elements.md`；`.cursor/skills/quarto-docs/references/zh/writing-style-core.md`；`.cursor/skills/cpp-content/references/cpp/toolchain.md`
- **可写**: `content/getting-started/install-toolchain.qmd`；示例 `code/getting-started/install-toolchain.cpp`（单文件 `*.cpp`，需构建工程则用同名子目录，产物落其 `build/`）；`_quarto.yml`（追加本章）
- **禁止**: `theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

## 验收

- [ ] qmd 符合体量预算
- [ ] verify_examples.py 通过
- [ ] quarto render 通过
- [ ] INDEX.md 更新为 done

## Cursor 提示词

> 本任务已并入 TASK-ENV-001，不单独执行。
