# git 工作流

通用 git 操作规范。默认环境：Windows + PowerShell。**只在用户明确要求时才提交/推送/建 PR。**

## .opencode 目录的上传策略

`.opencode/` 里有 skills 本体，也有安装产物——**分清必传与必不传**：

- **必传**：`.opencode/skills/**`（规则、案例、脚本、模板——知识库本体，clone 后即用）、
  `.opencode/package.json` + `package-lock.json`（<1KB，锁定 `@opencode-ai/plugin` 版本，重建一致）。
- **必不传**：`.opencode/node_modules/`（安装产物，仓库根 `.gitignore` 的 `node_modules/` 为任意层级规则，
  自动覆盖；clone 后 `cd .opencode; npm install` 重建）、`.opencode/plans/`（会话级计划草稿）、
  `/scripts/python.json`（本机解释器指定，clone 后按 AGENTS.md 解析协议重建）。
- **嵌套 `.gitignore` 不自忽略自身**：`.opencode/.gitignore` 若把 `.gitignore` 自己列入忽略清单，
  该文件就不会入库、clone 后没有规则——忽略规则统一放仓库根 `.gitignore` 管理。

自检命令（首传前跑一次）：

```powershell
git check-ignore -v .opencode/node_modules .opencode/plans scripts/python.json _book .quarto
# 每个路径都应命中一条忽略规则；package.json / skills 不应出现在输出里
```

## 仓库格式统一（.gitattributes）

- 仓库内文本**一律 LF**：`.gitattributes` 写 `* text=auto eol=lf`（跨平台 + Actions ubuntu +
  clang-format 兼容），二进制扩展名（png/jpg/ico/woff…）显式 `binary`，`*.bat`/`*.cmd` 保持 CRLF。
- 编码**一律 UTF-8 无 BOM**；PowerShell 5.1 的 `utf8` 参数会写 BOM，需要无 BOM 时用
  `[System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))`。
- 首次提交用 `git add --renormalize .` 把行尾策略一次性落地；后续无需再管。

## 首次上传（init → 建仓 → push）

```powershell
git init -b main
git add --renormalize .
git status --porcelain        # 核验：无 node_modules/_book/.quarto/python.json/plans 条目
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

- 只暂存目标文件，不提交密钥/生成产物（`_book/`、`.quarto/` 已在 `.gitignore`）。
- commit message 简洁、对齐仓库现有风格。

## 日常流程

```powershell
git add <file>...            # 只 add 要提交的文件
git commit -m "描述"          # 简洁描述本次改动
git push                      # 推送到远端
```

## 分支与协作

```powershell
git branch <name>             # 建分支
git switch <name>             # 切换分支
git switch -c <name>          # 建并切换
git merge <name>              # 合并
git pull                      # 拉取并合并
```

## 回滚

```powershell
git restore <file>            # 丢弃工作区改动
git restore --staged <file>   # 取消暂存
git reset --soft HEAD~1       # 撤销最近一次 commit（保留改动）
```

## 禁忌

- 不用 `git commit --amend`（除非修复刚失败且未推送的 commit）。
- 不用 `-i` 交互式、不跳过 hooks、不 force-push、不建空 commit（除非明确要求）。
- 不更新 `git config`（除非明确要求）。
