---
name: github-ops
description: GitHub 仓库操作与发布。涉及 git、gh CLI、Pages、Actions、PR/Issue 时使用。默认中文。
metadata:
  short-description: Git 操作、Pages 发布与 CI
---

# Skill: github-ops

管 git 工作流、Pages 发布与 CI 操作清单。配置成因与平台限制从知识库检索。Book 产物目录 `_book/`。

## 适用场景

- 分支、提交、推送、PR/Issue、gh CLI、Pages 部署与 CI 排错。
- **不适用**：正文与 skill 内容改动（转对应 skill 后再回来提交）。

## 任务路由

| 任务 | 读取 |
| --- | --- |
| git 日常 / 提交前 | `references/git-workflow.md`（依据：`kb-search "仓库一致性"`） |
| Pages 发布与部署排错 | `references/github-pages.md`（依据：`kb-search "Pages 部署方式"`） |
| Actions / CI | `references/ci.md` |
| Git 对比频率 | `references/git-workflow.md`（取舍：知识库 `cpp-tooling-repo-hygiene-v1`） |

## P0 硬约束

1. commit、push、建 PR 与任何远端修改默认不做；只在用户明确要求时执行，范围只覆盖用户指定的路径组与目标分支。不对 `main` force-push。
2. 只 `git add` 显式路径，禁止 `git add -A` 裹挟用户既有未提交改动。
3. 远端只维护 `main` 与 `gh-pages`。Actions 用 peaceiris 把 `_book/` 以 `force_orphan` 推到 `gh-pages`。
4. 行尾 LF、UTF-8 无 BOM，忽略规则集中在根 `.gitignore`。
5. Git 状态、diff 和 log 只在任务需要时检查，禁止为了轮询而频繁重复对比。

## 工作流程

1. 先跑 `& .agents/skills/agent-ops/scripts/run.ps1 status --all` 看清工作区，确认不覆盖他人改动。
2. 按路由读取对应 reference，再执行操作。
3. 提交信息使用中文分类前缀（如“文档：”“修复：”“维护：”）说明动机与影响，一次提交只做一件事。整句保持中文，仅在没有合适中文译名时保留技术标识。
4. 推 `main` 触发 `.github/workflows/pages.yml` 部署。PR 触发 `render-check.yml` 跑渲染与示例校验。

## 完成判据

- [ ] `git status` 只显示预期文件，`git log -1` 与远端状态符合预期。
- [ ] 未暴露密钥、令牌或个人路径。CI 结果已确认。
