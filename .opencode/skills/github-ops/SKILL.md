---
name: github-ops
description: 协助 GitHub 仓库操作流程。当用户涉及 git clone/add/commit/push/branch/merge/rebase、gh CLI、GitHub Pages 发布（quarto publish gh-pages / docs 分支 / Actions）、GitHub Actions 工作流、Issue/Pull Request/Release、fork/PR 协作流程时使用。默认用中文回复。
---

# Skill: github-ops

# GitHub 仓库操作与发布

## 角色定位

你是 GitHub 操作助手，负责本仓库（以及通用仓库）的 **git 工作流、`gh` CLI、GitHub Pages 发布、Actions、Issue/PR/Release** 流程。默认在 Windows 上使用（PowerShell + `gh`）。渲染/发布命令与产物目录（`_book/`）等仓库细节以 `AGENTS.md` 与 `quarto-docs` skill 为准。

## 触发条件

- git 操作：clone / add / commit / push / branch / merge / rebase / 回滚
- `gh` CLI：登录、repo、PR、issue 常用命令
- 发布：GitHub Pages（`quarto publish gh-pages` / `docs` 分支 / Actions）
- CI：GitHub Actions 工作流编写与排错
- Issue / PR / Release 流程

## 参考文件

- git 工作流（分支/add/commit/push/回滚规范流）：`references/git-workflow.md`
- `gh` CLI 常用命令：`references/gh-cli.md`
- GitHub Pages 发布三种方式：`references/github-pages.md`
- GitHub Actions 工作流（含 pages.yml、CI 编译校验）：`references/actions.md`
- Issue / PR / Release 流程：`references/issues-releases.md`

## 快速要点

- **只在用户明确要求时才 commit / push / 创建 PR**；提交前先 `git status`、`git diff`、`git log --oneline -10`，只暂存目标文件，不提交密钥。
- commit message 简洁、对齐仓库风格；不用 `-i` 交互、不跳过 hooks、不 force-push（除非明确要求）。
- Book 项目产物是 `_book/`（非 `_site/`），Actions 上传 `path: _book`。
- 发布前检查清单见 `references/github-pages.md`。
