# 仓库结构

`content/` 保存 Quarto 章节，`code/` 保存对应 C++ 示例；`.cursor/skills/` 按职责提供工作流、脚本和资源，`knowledge/` 保存领域依据，`temp/` 保存索引与重构产物。

章节按 `content/<part>/<chapter>.qmd`、`code/<part>/<chapter>/` 和 `cpp-content/references/tasks/<part>/<chapter>.md` 对齐。构建、渲染和缓存目录不入上下文或提交。

运行入口统一为 `.cursor/skills/agent-ops/scripts/run.py`；知识库管道脚本归 `python-tools/scripts/`，主题资源归 `quarto-theme/assets/theme/`，C++ 配置归 `cpp-content/assets/config/`。
