---
name: python-tools
description: 当任务需要运行、维护或迁移本仓库 Python 工具、知识库管道、维护脚本或其配置时触发。
---

# Python 工具

- 使用 `scripts/` 中的脚本；统一通过 `.cursor/skills/agent-ops/scripts/run.py` 调用仓库检查入口。
- 运行时优先使用 `CPP_MEMO_PYTHON`，其次使用 `assets/config/runtime.json`（本机文件不入库），最后回退到 PATH。
- Python 版本要求和格式化配置见 `assets/config/pyproject.toml`。
- 知识库正文位于根目录 `knowledge/`，索引产物位于 `temp/knowledge-index/`。
