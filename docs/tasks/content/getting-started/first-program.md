# TASK-ENV-003 · 第一个程序

- **状态**: done
- **Skill**: cpp-content + quarto-docs
- **依赖**: TASK-002

## 读写边界

- **必读**: [`AGENTS.md`](../../AGENTS.md)；本文件；`.cursor/skills/quarto-docs/references/quarto/authoring.md`；`.cursor/skills/quarto-docs/references/quarto/authoring-elements.md`；`.cursor/skills/quarto-docs/references/zh/writing-style-core.md`；`.cursor/skills/cpp-content/references/cpp/cpp.md`
- **可写**: `content/getting-started/first-program.qmd`；示例 `code/getting-started/first-program/`（`first-program.cpp` + `CMakeLists.txt` + `build-and-run.sh`）；`_quarto.yml`（追加本章）
- **禁止**: `theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

## 范围说明

本章覆盖两种跑法：先用 `g++ -std=c++20 -Wall -Wextra` 直接编译 Hello World，再写最小 `CMakeLists.txt` 用 CMake 构建同样的程序。多文件/目标/库的深入内容留给 `cmake-intro`。

## 验收

- [x] qmd 符合体量预算
- [x] verify_examples.py 通过
- [x] quarto render 通过
- [x] INDEX.md 更新为 done

## Cursor 提示词

> 执行 TASK-ENV-003。只读「读写边界」所列文件；完成验收清单。
