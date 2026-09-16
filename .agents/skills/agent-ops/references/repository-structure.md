# 仓库结构

`content/` 保存 Quarto 章节，`code/` 保存对应 C++ 示例。`.agents/skills/` 按职责提供工作流、脚本和资源，`knowledge/` 保存领域依据，`temp/` 保存索引与重构产物。

章节按 `content/<part>/<chapter>.qmd`、任务矩阵里登记的示例路径和 `.agents/skills/cpp-content/references/tasks/<part>.md` 中的一行对齐。需要重复编译运行的章节使用 `code/<part>/<chapter>/`，并至少提供源码和一个 `build-and-run.sh`。一章需要多个独立工程时，可以在矩阵「示例」列登记多个路径。part 与章节使用简短、无重复语义的 ASCII kebab-case，目录 slug 保持稳定，读者可见的 part 标题可以随内容范围调整。章节文件不加数字前缀，阅读顺序只在 `_quarto.yml` 与各 part 的 `index.qmd` 维护。命名依据见标识 `cpp-agent-repository-navigation-v1`。构建、渲染和缓存目录不入上下文或提交。

运行入口统一为 `.agents/skills/agent-ops/scripts/run.py`。知识库管道脚本归 `python-tools/scripts/`，主题资源归 `quarto-theme/assets/theme/`，C++ 配置归 `cpp-content/assets/config/`。

## 页面体量预算

行数用于控制单页认知负荷，超出上限时先拆分主题而不是压缩文字。

| 页面类型 | 预算 | 说明 |
| --- | --- | --- |
| 教学正文（content/**/*.qmd） | 60–150 行且 ≤5000 有效字符 | 有效字符排除围栏代码和 `{{< include >}}` 行；超限按读者任务拆成系列页 |
| 入口与卡片页（index.qmd） | ≤45 行 | 只做定位，不承担讲解 |
| 根 README.md | ≤90 行 | 路线与仓库结构，细节指向文档站与 skills |

页面预算由 `check_skill_size.py` 强制。QMD 拆页、代码 include 与知识库 Token 的决策依据见标识 `cpp-agent-context-budget-v1`；两类页面的组织依据见 `cpp-quarto-chapter-pattern-v1` 与 `cpp-quarto-landing-pattern-v1`。

## Agent 运行约定
统一入口是 `.agents/skills/agent-ops/scripts/run.py`。先用 `scope` 确定读取边界，再按改动域运行 `check --profile fast|book|knowledge|python`，跨域或发布时运行 `full`。`render` 默认只跑 `book` profile，需要完整浏览器矩阵时加 `--require-browser`。

`_book/`、`.quarto/`、`code/**/build/`、`.cache/`、`.tmp/` 和 `temp/` 是生成物或缓存。不要手动编辑、读取或提交。新的项目中间文件统一写入 `temp/<用途>/`，例如计划写入 `temp/plans/`，重构报告写入 `temp/refactor/`，知识库索引写入 `temp/knowledge-index/`。`.tmp/` 仅作为历史残留兼容忽略目录，不再生成。
