---
name: github-ops
description: GitHub 仓库操作与发布。涉及 git、gh CLI、Pages、Actions、PR/Issue 时使用。默认中文。
---

# Skill: github-ops

Git 工作流、Pages 发布、CI。Book 产物目录 `_book/`。

## 任务路由

| 任务 | 参考 |
|---|---|
| git 日常 / 提交前 | `references/git-workflow.md` |
| 发布 Pages、部署排错 | `references/github-pages.md` |
| Actions / CI | `references/actions.md` |
| gh CLI | `references/gh-cli.md` |
| PR / Issue | `references/issues-releases.md` |

## 要点

- **禁止**：未明确要求时不 commit / push / 建 PR；不 force-push main
- 只 `git add` 显式路径：工作区常混有用户既有未提交改动，禁止 `git add -A` 裹挟
- 远端仅 `main` + `gh-pages`；Actions 用 peaceiris 把 `_book/` 推到 `gh-pages`（`force_orphan`）
- 推 main → `.github/workflows/pages.yml` 自动部署；PR → `render-check.yml` 跑渲染与示例校验
