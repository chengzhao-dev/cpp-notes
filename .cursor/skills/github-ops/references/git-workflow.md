# git 工作流

通用 git 操作规范。默认环境：Windows + PowerShell。**只在用户明确要求时才提交/推送/建 PR。**

## skills 上传策略

- **必传**：`.cursor/skills/**`（Cursor 项目 skills：规则、案例、脚本、模板，clone 后即用）。
- **必不传**：`/.config/python/runtime.json`（本机解释器，clone 后按 AGENTS.md 解析协议重建）、
  `_book/`、`.quarto/`、`node_modules/`（根 `.gitignore` 覆盖）。
- **忽略规则统一放仓库根 `.gitignore`**，不要在嵌套目录用「自忽略 `.gitignore`」。

自检命令（首传前跑一次）：

```powershell
git check-ignore -v .config/python/runtime.json _book .quarto node_modules
# 每个路径都应命中一条忽略规则；.cursor/skills 不应出现在输出里
```

## 仓库格式统一（.gitattributes）

- 仓库内文本**一律 LF**：`.gitattributes` 写 `* text=auto eol=lf`（跨平台 + Actions ubuntu +
  clang-format 兼容），二进制扩展名（png/jpg/ico/woff…）显式 `binary`，`*.bat`/`*.cmd` 保持 CRLF。
- 编码**一律 UTF-8 无 BOM**；PowerShell 5.1 的 `utf8` 参数会写 BOM，需要无 BOM 时用
  `[System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))`。
- 中文文件禁止经过系统代码页或 GBK 往返转换；修改后运行 `python scripts/agent/check_encoding.py`，检查 UTF-8、BOM、LF 和常见乱码特征。
- 首次提交用 `git add --renormalize .` 把行尾策略一次性落地；后续无需再管。

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

- 只暂存目标文件，不提交密钥/生成产物（`_book/`、`.quarto/` 已在 `.gitignore`）。
- commit message 简洁、对齐仓库现有风格。

## 大更新的提交方式

先查看 `git status --short`、`git diff --stat` 和 `git diff --name-only`，再按逻辑分组暂存，例如文档正文、校验工具、主题样式和仓库配置。每组使用显式路径执行 `git add`，随后检查 `git diff --cached --check` 与 `git diff --cached --stat`。

提交前优先运行 `python scripts/agent/run.py verify --changed`、`python scripts/agent/run.py check` 和 `git diff --check`。只有改动主题或 Quarto 全局配置时才整本渲染；只有改动 C++ 全局配置或校验器时才需要全量 C++ 验证。不要让 `build/`、`.cache/`、`.tmp/` 和其他生成物触发校验。Python 解释器选择规则见 [`handbook/operations/agent-operations.md`](../../../../handbook/operations/agent-operations.md)。

推荐提交信息前缀：`docs:` 用于文档与写作规范，`feat:` 用于新增功能或章节，`fix:` 用于行为修复，`refactor:` 用于不改变行为的结构调整，`chore:` 用于配置和维护。多个文件若属于同一个不可分割的行为变更，可放在同一提交；否则拆成可独立回滚的提交。未明确要求时不 commit、push 或创建 PR。

## 日常流程

```powershell
git add <file>...            # 只 add 要提交的文件
git commit -m "描述"          # 简洁描述本次改动
git push                      # 推送到远端
```

## 分支与协作

**远端只保留两个分支**：`main`（源码）与 `gh-pages`（Quarto `_book/` 产物）。仓库 Ruleset `block-extra-branches` 禁止创建其它远端分支（含仓库管理员；紧急时需在 Settings → Rules 临时关掉该规则）。

- 本地可建临时分支做实验，**不要** `git push -u origin <feat-branch>`。
- 改动直接提交并推到 `main`；合并/推送后本地临时分支可删。
- `gh-pages` 仅由 Actions（`peaceiris/actions-gh-pages`）更新，勿手工推源码上去。`protect-gh-pages` 禁止删除该分支；`protect-main` 禁止删除与 force-push `main`。

```powershell
git branch <name>             # 本地临时分支
git switch <name>             # 切换分支
git switch -c <name>          # 建并切换
git merge <name>              # 合并进当前分支（通常是 main）
git push origin main          # 只推 main
git branch -d <name>          # 删本地临时分支
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

## 文档兼容性

README 面向 GitHub 阅读，保留徽章、图片和外部链接的标准 Markdown 写法，并为图片提供替代文字。Skill、`handbook/` 和 `AGENTS.md` 以纯文本、表格、编号步骤和代码块为主；默认不放 Mermaid 或图片，复杂流程确有必要时需同时提供文字结论。修改 Markdown 后运行统一文档检查，避免把 GitHub 专用语法误判为 Quarto 错误。

代码、命令和终端输出统一左对齐。只有一两条且不需要上下文的短命令直接写在正文中；需要说明顺序或用途的命令才放入代码块，并把简短注释放在对应命令上方。代码块与 transcript 使用 GitHub 风格的明暗色板和统一字体，transcript 不使用语言高亮。
