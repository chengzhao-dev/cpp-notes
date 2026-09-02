# Python 脚本规范

仓库 agent 工具脚本均为 Python ≥ 3.9，**运行时仅用标准库**。格式用 [Black](https://black.readthedocs.io/)（见 `scripts/pyproject.toml`）。

## 脚本位置

| 路径 | 用途 |
|---|---|
| `scripts/cpp/` | C++ 工程脚手架（`init_project.py` + `templates/`） |
| `scripts/build/` | 渲染后处理（`defer-mermaid.py`） |
| `scripts/maint/` | 文档维护（`gen_tasks.py`） |
| `scripts/config/` | 本机解释器（`python.json`，不入库） |
| `.cursor/skills/*/scripts/` | 领域校验：编译、脚手架、链接检查等 |

**新建脚手架/校验 → 写 Python 脚本，不新建 skill。**

## Black

```bash
pip install black
black --config scripts/pyproject.toml scripts/ .cursor/skills/*/scripts/
black --check --config scripts/pyproject.toml scripts/ .cursor/skills/*/scripts/   # CI
```

## 中文注释约定

| 位置 | 要求 |
|---|---|
| 模块 `"""…"""` | 中文：做什么、用法一行、退出码 |
| `argparse` help | 中文 |
| 用户可见 `print` | 中文 |
| 行内 `#` | 仅非显然逻辑（协议分支、WSL 路径、幂等等） |

**禁止**：逐行翻译式注释、大段英文 docstring、重复模块说明。

## 解释器

见 [`AGENTS.md`](../AGENTS.md)「运行 Python 脚本」：`scripts/config/python.json` → 环境变量 → 自动搜索。

## 新脚本 Checklist

- [ ] 放对目录（`scripts/<域>/` 或 skill `scripts/`）
- [ ] 模块 docstring + 中文 argparse help
- [ ] 仅标准库依赖
- [ ] `black` 格式化
- [ ] 在 `docs/structure.md` 或对应 skill 中登记用途
