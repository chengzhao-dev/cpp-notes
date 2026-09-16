# git 工作流（操作清单）

通用 git 操作规范。默认环境：Windows + PowerShell。**只在用户明确要求，或最终批准计划包含 `### 交付收口` 时才提交/推送/建 PR。**

为什么这样归一化行尾、为什么远端只留两个分支、提交按什么边界切分，都在知识库，一条命令取用：

```powershell
& .agents/skills/agent-ops/scripts/run.ps1 kb-search "仓库一致性与分支保护依据" --domain github-ops
```

## 硬约束

- 未明确要求且批准计划没有交付收口时不 commit、push、创建 PR。不 force-push main。不建空 commit。
- 批准计划中的交付收口只授权该节列出的路径组、提交和推送；不扩展到未列改动、`git add -A`、amend、改 remote 或额外分支。
- 不用 `git commit --amend`（除非修复刚失败且未推送的 commit）。不用 `-i` 交互式。不跳过 hooks。不更新 `git config`（除非明确要求）。
- 只 `git add` 显式路径，禁止 `git add -A` 裹挟用户既有未提交改动。
- 提交信息使用中文分类前缀，例如“文档：”“修复：”“维护：”，让读者不看 diff 就能判断影响面与是否需要跑检查。整句保持中文，只有没有合适中文译名时才保留 `CMake`、`Ninja`、`clangd` 等技术标识。
- 必传 `.agents/skills/**`。必不传本机运行时配置、`_book/`、`.quarto/`、`node_modules/`。项目 Python 唯一来源为已提交的 `.agents/manifest.json`，不得新增第二份解释器路径。忽略规则统一放根 `.gitignore`，不在嵌套目录放「自忽略 `.gitignore`」。

## Git 对比频率

Git 对比服务于当前任务，不要在每个步骤重复运行 `git status`、`git diff` 或 `git log`。

| 场景 | 是否需要频繁对比 Git |
| --- | --- |
| 写文档、查资料、数据分析、生成文案、普通问答 | 不需要 |
| Code Review、提交信息生成、变更总结、冲突解决、发布说明 | 需要，但通常只在执行时查一次或几次 |
| 调试“最近改动导致的问题” | 可能需要，查最近 diff/log 即可 |
| 维护 skills 仓库本身 | 用 Git 管理即可，不必运行时频繁对比 |

执行 Git 操作前读取一次足够的状态即可。只有任务范围变化、出现冲突或验证失败时才重新检查。

## 仓库格式基线

文本一律 LF、编码一律 UTF-8 无 BOM。二进制扩展名显式声明为 binary，`*.bat`/`*.cmd` 保持 CRLF。
中文文件禁止经过系统代码页或 GBK 往返转换。改动 `.qmd` 或规范文档后先跑编码检查。

```powershell
git check-ignore -v .agents/skills/python-tools/assets/config/runtime.json _book .quarto node_modules/
# 每个路径都应命中一条忽略规则；.agents/skills 不应出现在输出里
```

## 首次上传（init → 建仓 → push）

```powershell
git init -b main
git add --renormalize .
git status --porcelain        # 核验：无 node_modules/_book/.quarto/runtime.json/plans 条目
git commit -m "初始提交：…"
gh repo create <owner>/<repo> --public --source . --push   # 建仓 + 设 remote + 推 main 一步完成
```

纯 git 备选（无 gh）：在 github.com 手动 New repository（**不要**勾选初始化 README/license）→
`git remote add origin https://github.com/<owner>/<repo>.git` → `git push -u origin main`。
建仓前先把 `_quarto.yml` 的 `repo-url`/`site-url` 占位换成真实地址，避免二次提交。

## 提交前必做

```powershell
git status
git diff
git log --oneline -10
```

以上检查仅适用于确实涉及提交、变更总结、审查、冲突解决或发布说明的任务。普通文档、资料、分析和问答不需要例行运行。

再按改动范围跑检查：`run.ps1 verify --changed`、`run.ps1 check --profile ...`、`git diff --check`。
只有改主题或 Quarto 全局配置才整本渲染。只有改 C++ 全局配置或校验器才全量验证。不要让 `build/`、`.cache/`、`.tmp/` 触发校验。

`check`、`verify`、`build` 和 `render` 只证明本地改动可用，不是上传完成。批准计划含交付收口时，必须继续完成显式暂存、提交、`git fetch`、必要 rebase、推送、远端 SHA 和 CI/Pages 核对；其中任一项失败都不得报告任务完成。

## 大更新怎么分组

先看 `git status --short`、`git diff --stat`、`git diff --name-only`，再按可独立回滚的边界分组暂存，每组显式路径 `git add`，随后检查 `git diff --cached --check` 与 `git diff --cached --stat`。

前缀：`文档：` 表示文档与写作规范，`功能：` 表示新增功能或章节，`修复：` 表示行为修复，`重构：` 表示不改变行为的结构调整，`维护：` 表示配置与维护。一次任务通常 3–5 个提交，按实际边界决定，不为拆分而拆分。

## 日常流程与分支

```powershell
git add <file>...            # 只 add 要提交的文件
git commit -m "描述"          # 简洁描述本次改动
git push origin main          # 远端只推 main
git pull                      # 拉取并合并
```

远端只保留 `main`（源码）与 `gh-pages`（`_book/` 产物）。Ruleset `block-extra-branches` 禁止新建其它远端分支（管理员同样受限，紧急时在 Settings → Rules 临时关闭）。本地临时分支可随意建、合并后用 `git branch -d` 删除，**不要** `git push -u origin <feat-branch>`。`gh-pages` 仅由 Actions 更新，勿手工推源码。

## 回滚

```powershell
git restore <file>            # 丢弃工作区改动
git restore --staged <file>   # 取消暂存
git reset --soft HEAD~1       # 撤销最近一次 commit（保留改动）
```

## 文档兼容性

README 面向 GitHub 阅读，保留徽章、图片和外部链接的标准 Markdown 写法并为图片提供替代文字。Skill、`knowledge/` 和 `AGENTS.md` 以纯文本、表格、编号步骤和代码块为主，默认不放 Mermaid 或图片。改完 Markdown 跑统一文档检查，避免把 GitHub 专用语法误判为 Quarto 错误。
