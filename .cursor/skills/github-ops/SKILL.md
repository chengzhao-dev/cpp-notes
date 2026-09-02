---
name: github-ops
description: GitHub 仓库操作与发布。涉及 git、gh CLI、Pages、Actions、PR/Issue 时使用。默认中文。
---

# Skill: github-ops

Git 工作流、Pages 发布、CI。Book 产物目录 `_book/`。

## 任务路由（[docs/tasks/INDEX.md](../../../docs/tasks/INDEX.md)）

| 任务 | 参考 |
|---|---|
| TASK-INFRA-005 | `references/actions.md` |
| 发布 Pages | `references/github-pages.md` |
| git 日常 | `references/git-workflow.md` |
| gh CLI | `references/gh-cli.md` |
| PR/Issue | `references/issues-releases.md` |

**禁止**：未明确要求时不 commit/push/建 PR。

## 要点

- 只在用户明确要求时提交；不 force-push main
- 远端仅 `main` + `gh-pages`；Actions 用 peaceiris 推 `_book/` 到 `gh-pages`
- 推送 main → `.github/workflows/pages.yml` 自动部署
