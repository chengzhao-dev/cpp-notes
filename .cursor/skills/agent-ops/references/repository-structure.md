# 仓库结构

`content/` 保存 Quarto 章节，`code/` 保存对应 C++ 示例；`.cursor/skills/` 按职责提供工作流、脚本和资源，`knowledge/` 保存领域依据，`temp/` 保存索引与重构产物。

章节按 `content/<part>/<chapter>.qmd`、`code/<part>/<chapter>`（单文件 `.cpp` 或同名工程目录）和 `.cursor/skills/cpp-content/references/tasks/<part>.md` 矩阵里的一行对齐。构建、渲染和缓存目录不入上下文或提交。

运行入口统一为 `.cursor/skills/agent-ops/scripts/run.py`；知识库管道脚本归 `python-tools/scripts/`，主题资源归 `quarto-theme/assets/theme/`，C++ 配置归 `cpp-content/assets/config/`。

## Agent 运行约定
统一入口是 `.cursor/skills/agent-ops/scripts/run.py`。先用 `scope` 确定读取边界，再按需运行 `check`、`verify`、`render` 或 `kb-*` 子命令。

`_book/`、`.quarto/`、`code/**/build/`、`.cache/` 和 `.tmp/` 是生成物或缓存；不要手动编辑、读取或提交。重构报告写入 `temp/refactor/`，知识库索引写入 `temp/knowledge-index/`。
