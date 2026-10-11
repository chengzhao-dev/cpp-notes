# practice 章节任务矩阵

本文件登记“工程应用”分册。Android 背景页只解释交付职责，没有对应的可构建示例。

## 公共读写边界

- **必读**: `AGENTS.md`、本文件、`.agents/skills/writing-quarto/references/quarto/authoring.md`
- **可写**: 本表所列正文路径，以及 `_quarto.yml`
- **禁止**: `code/**/build/`、`_book/`、`.quarto/`、`.cache/`

| ID | 章节 | 状态 | 前置 | 正文 | 示例 | 专项必读 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `TASK-APP-001` | static-library | done | `TASK-ENV-006` | `content/practice/static-library.qmd` | `code/practice/static-library/` | `.agents/skills/writing-cpp/references/cpp/engineering.md` | greeting/ 拥有静态库目标，根 main.cpp 构建消费它的 app |
| `TASK-APP-002` | shared-library | done | `TASK-APP-001` | `content/practice/shared-library.qmd` | `code/practice/shared-library/` | `.agents/skills/writing-cpp/references/cpp/engineering.md` | greeting/ 拥有动态库目标，根 main.cpp 构建消费它的 app |
| `TASK-APP-003` | android-imaging | done | `TASK-APP-002` | `content/practice/android-imaging.qmd` | —（背景页无示例） | `.agents/knowledge/cpp-teaching/toolchain/library-and-executable-linking.md` | 只讲可执行文件仿真和动态库 SDK 交付边界 |
