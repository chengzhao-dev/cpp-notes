# gh CLI 常用命令

GitHub 官方命令行工具 `gh`。Windows 上装好并 `gh auth login` 后可用。

## 认证

```powershell
gh auth login          # 交互式登录（选 GitHub.com + HTTPS）
gh auth status         # 查看登录状态
```

## 仓库

```powershell
gh repo create <name> --public --source . --push   # 把当前目录推到新仓库
gh repo view <owner>/<repo> --web                   # 浏览器打开仓库
gh repo clone <owner>/<repo>                        # 克隆
gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow   # Pages Source 设为 GitHub Actions（一次性）
gh run watch                                        # 跟踪当前触发的 workflow 运行
```

> `gh api` 设置 Pages 前仓库必须已存在；等价的手动路径是 Settings → Pages → Build and
> deployment → Source 选 **GitHub Actions**。

## PR

```powershell
gh pr create --title "..." --body "..."   # 建 PR
gh pr list                                # 列出 PR
gh pr view                                # 查看当前 PR（web 用 --web）
gh pr checkout <number>                   # 检出 PR 分支
gh pr merge <number> --squash             # 合并
```

## Issue

```powershell
gh issue create --title "..." --body "..."  # 建 issue
gh issue list                               # 列出 issue
gh issue close <number>                     # 关闭
```

## Release

```powershell
gh release create <tag> --notes "..."       # 建 release
```
