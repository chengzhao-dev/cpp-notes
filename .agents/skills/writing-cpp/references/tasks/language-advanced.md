# language-advanced 章节任务矩阵

本文件是 language-advanced 全部章节任务的唯一权威记录：一行一章，读写边界与验收在文件级统一，只有差异写进行内。改状态只改本表「状态」列，仓库内不存在其它 INDEX 文件。

## 公共读写边界

- **必读**: `AGENTS.md`、本文件、`.agents/skills/writing-cpp/references/cpp/cpp.md`、`.agents/skills/writing-cpp/references/cpp/language-basics.md`、`.agents/skills/writing-quarto/references/quarto/authoring.md`、`.agents/skills/writing-quarto/references/zh/chapter-writing.md`
- **可写**: 本行「正文」与「示例」所列路径，以及 `_quarto.yml`（追加本章）
- **禁止**: `.agents/skills/designing-theme/assets/theme/`、`content/<其他 part>/`、示例目录下的 `build/`（CMake 产物）

示例默认单文件 `code/<part>/<chapter>.cpp`，由分册根 `code/language-advanced/CMakeLists.txt` 收集成同名可执行文件。正文不单设“示例源码与构建”小节，源码链接、构建入口和观察重点合并成 `## 本章回顾` 的一句正文。章节骨架固定为“任务序列 → `## 常见错误` → `## 自测问题` → `## 本章回顾`”。

## 统一验收（每章完成时逐项确认）

- [ ] 正文符合体量预算，`run.py check --profile fast` 与 `run.py render` 通过
- [ ] 示例经 `run.py verify --changed` 编译通过，正文承诺的输出与实测一致
- [ ] 本文件「状态」列已更新为 `done`

## 任务矩阵

| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `TASK-ADV-001` | strong-types | done | `TASK-LANG-012` | `content/language-advanced/strong-types.qmd` | `code/language-advanced/strong-types.cpp` | `.agents/skills/writing-cpp/references/cpp/language-basics.md` | 只讲聚合包装与其边界，构造函数与不变量留给自定义类型章节 |
