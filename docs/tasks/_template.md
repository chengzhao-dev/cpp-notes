# TASK-<PART>-<NNN> · <中文标题>

- **状态**: todo
- **Skill**: cpp-content + quarto-docs
- **依赖**: TASK-<前置 ID>

## 读写边界

- **必读**: [`AGENTS.md`](../../AGENTS.md)；本文件；`.cursor/skills/quarto-docs/references/quarto/authoring.md`；`.cursor/skills/quarto-docs/references/quarto/authoring-elements.md`；`.cursor/skills/quarto-docs/references/zh/writing-style-core.md`；`.cursor/skills/cpp-content/references/cpp/<topic>.md`
- **可写**: `content/<part>/<chapter>.qmd`；`code/<part>/<chapter>.cpp`
  （需构建工程则改用同名子目录 `code/<part>/<chapter>/`，其 `build/` 为产物：不入库、不读、不校验）；`_quarto.yml`（仅追加本章一行）
- **禁止**: `theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）、`.github/`（除非任务 ID 明确允许）

## 验收

- [ ] qmd 符合 authoring 约定与章节体量预算（见 `docs/structure.md`）
- [ ] `python .cursor/skills/cpp-content/scripts/verify_examples.py` 通过
- [ ] `quarto render` 无阻塞警告
- [ ] `docs/tasks/INDEX.md` 状态更新为 done

## Cursor 提示词

> 执行 TASK-<PART>-<NNN>。只读「读写边界」所列文件；完成验收清单。
