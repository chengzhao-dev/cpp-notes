# 仓库结构

`content/` 保存 Quarto 章节，`code/` 保存对应 C++ 示例；`.agents/skills/` 按职责提供工作流、脚本和资源，`knowledge/` 保存领域依据，`temp/` 保存索引与重构产物。

章节按 `content/<part>/<chapter>.qmd`、`code/<part>/<chapter>`（单文件 `.cpp` 或同名工程目录）和 `.agents/skills/cpp-content/references/tasks/<part>.md` 矩阵里的一行对齐。构建、渲染和缓存目录不入上下文或提交。

运行入口统一为 `.agents/skills/agent-ops/scripts/run.py`；知识库管道脚本归 `python-tools/scripts/`，主题资源归 `quarto-theme/assets/theme/`，C++ 配置归 `cpp-content/assets/config/`。

## 页面体量预算

行数用于控制单页认知负荷，超出上限时先拆分主题而不是压缩文字。

| 页面类型 | 预算 | 说明 |
| --- | --- | --- |
| 教学正文（content/**/*.qmd） | 60–170 行 | 下限保证任务与验证完整，上限保证一次读完不必翻页 |
| 入口与卡片页（index.qmd） | ≤45 行 | 只做定位，不承担讲解 |
| 根 README.md | ≤90 行 | 路线与仓库结构，细节指向文档站与 skills |

两类页面的组织依据是知识库 `quarto-docs` 域的两个条目，分别查询（多词短语会整体匹配不到，必须单 token）：`python .agents/skills/agent-ops/scripts/run.py kb-search "块序列" --domain quarto-docs` 与 `python .agents/skills/agent-ops/scripts/run.py kb-search "卡片" --domain quarto-docs`。

## Agent 运行约定
统一入口是 `.agents/skills/agent-ops/scripts/run.py`。先用 `scope` 确定读取边界，再按需运行 `check`、`verify`、`render` 或 `kb-*` 子命令。

`_book/`、`.quarto/`、`code/**/build/`、`.cache/`、`.tmp/` 和 `temp/` 是生成物或缓存；不要手动编辑、读取或提交。新的项目中间文件统一写入 `temp/<用途>/`，例如重构报告写入 `temp/refactor/`，知识库索引写入 `temp/knowledge-index/`。`.tmp/` 仅作为历史残留兼容忽略目录，不再生成。
