# Agent 运行约定

统一入口是 `.cursor/skills/agent-ops/scripts/run.py`。先用 `scope` 确定读取边界，再按需运行 `check`、`verify`、`render` 或 `kb-*` 子命令。

`_book/`、`.quarto/`、`code/**/build/`、`.cache/` 和 `.tmp/` 是生成物或缓存；不要手动编辑、读取或提交。重构报告写入 `temp/refactor/`，知识库索引写入 `temp/knowledge-index/`。
