# Issue / Pull Request / Release 流程

## Issue

- 用 `gh issue create` 或网页新建，写清现象、复现步骤、期望/实际结果。
- 标题一句话点明问题；正文用 Markdown，代码/命令用代码块。
- 与维护者沟通保持简洁、友善。

## Pull Request

1. 从 `main` 拉新分支：`git switch -c feature/xxx`。
2. 提交改动并 `git push -u origin feature/xxx`。
3. `gh pr create --title "..." --body "..."` 建 PR。
4. 描述里写：做了什么、为什么、如何验证。
5. 等 CI 通过 + 评审；按反馈补提交（无需重开 PR）。

## Release

- 打 tag：`git tag v1.0.0` 然后 `git push --tags`。
- `gh release create v1.0.0 --notes "..."` 生成 release。

## 协作礼仪

- 一个 PR 只做一件事，便于评审。
- 不直接 push 到 `main`（团队仓库），走 PR。
- 提交信息用祈使句、现在时（如 `Add setup chapter`）。
