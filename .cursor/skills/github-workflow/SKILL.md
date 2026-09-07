---
name: github-workflow
description: 维护 GitHub Actions 自动化工作流、Pages 部署流水线与 CI 校验环境。
---

# Skill: github-workflow

负责维护和调试仓库中的 GitHub Actions 工作流、持续集成（CI）检查与 GitHub Pages 自动化发布流水线。

## 任务路由

CI 检查与本地校验对齐读 `references/ci-check.md`；常规分支操作与 PR 管理转交 `github-ops`。

## 工作流原则

- **快速反馈**：PR 触发的 `render-check.yml` 保持轻量，只执行 `quarto render`、`defer-mermaid.py` 与 C++ 示例校验。
- **安全与幂等**：部署到 `gh-pages` 分支使用 `force_orphan: true`，不累积历史产物；Pages 源配置纠正具备幂等容错机制。
- **本地与 CI 对齐**：CI 中运行的所有脚本入口必须与本地 .cursor/tools/run.py 驱动的脚本完全一致。
