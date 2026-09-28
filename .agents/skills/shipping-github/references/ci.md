# CI 与 Actions（操作清单）

## GitHub Actions

本仓库工作流：`.github/workflows/pages.yml`（发布）、`render-check.yml`（PR 渲染检查）。CI 只覆盖文档渲染与文档后处理脚本；C++ 示例编译不进 CI，只在本地按需运行 `.agents/skills/writing-cpp/scripts/verify_examples.py`。

### pages.yml

- 触发：`push` 到 `main`，或 `workflow_dispatch`
- 步骤：checkout → setup Quarto → setup Python → `quarto render` → `.agents/skills/maintaining-python/scripts/render/defer_mermaid.py` → `peaceiris/actions-gh-pages` 推 `_book/` 到 `gh-pages`（`force_orphan`）→ 可选校正 Pages source
- 权限：`contents: write`（推分支）、`pages: write`（调 Pages API）
- Pages 设置：Deploy from a branch → `gh-pages` / `(root)`（见 `github-pages.md` 方式四）

### render-check.yml

- 触发：PR 到 `main` 与 `workflow_dispatch`
- 步骤：render + defer-mermaid（同时验证后处理脚本本身可用）
- 范围边界：C++ 示例编译验证留在本地，不作为 CI 门禁。

## CI 持续集成与检查规范
官方依据：[GitHub Actions workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)、[GITHUB_TOKEN 权限](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication)与 [Pages deployment](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

### 核心工作流清单

1. **render-check.yml**（Pull Request 门禁）：
   - 依赖环境：Ubuntu 最新版、Quarto 运行环境、Python 3.12。
   - 执行阶段：
     - quarto render：检查文档语法、YAML 配置与跨文件引用。
     - python3 .agents/skills/maintaining-python/scripts/render/defer_mermaid.py：验证渲染后处理脚本。
   - 范围边界：只做文档渲染与后处理；C++ 示例编译不进 CI。
2. **pages.yml**（Main 分支发布）：
   - 具备单并发控制（concurrency: pages），避免多任务并发覆盖。
   - 生成完整静态网站产物，推送到 gh-pages 分支。

### 调试与排错

- CI 失败时先在本地用 `run.py check --profile full` 复现，C++ 示例问题另跑 `verify_examples.py`；禁止盲目推 commit 试错。
- 每个 workflow 显式声明最小 `permissions`。新增步骤只申请实际需要的权限，并为部署步骤单独说明写权限来源。
