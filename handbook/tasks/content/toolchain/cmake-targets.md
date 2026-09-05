# TASK-TOOL-001 · CMake 目标

- **状态**: todo
- **Skill**: cpp-content + quarto-docs
- **依赖**: TASK-ENV-004

## 读写边界

- **必读**: [`AGENTS.md`](../../AGENTS.md)；本文件；`.cursor/skills/quarto-docs/references/quarto/authoring.md`；`.cursor/skills/quarto-docs/references/quarto/authoring-elements.md`；`.cursor/skills/quarto-docs/references/zh/writing-style-core.md`；`.cursor/skills/cpp-content/references/cpp/engineering.md`
- **可写**: `content/toolchain/cmake-targets.qmd`；示例 `code/toolchain/cmake-targets.cpp`（单文件 `*.cpp`，需构建工程则用同名子目录，产物落其 `build/`）；`_quarto.yml`（追加本章）
- **禁止**: `theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

## 验收

- [ ] qmd 符合体量预算
- [ ] verify_examples.py 通过
- [ ] quarto render 通过
- [ ] INDEX.md 更新为 done

## Cursor 提示词

> 执行 TASK-TOOL-001。只读「读写边界」所列文件；完成验收清单。
