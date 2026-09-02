# 渲染与预览运维

日常命令见根 [`AGENTS.md`](../AGENTS.md)。本节只收录排错步骤。

## 基本原则

- 改 `theme/scss/`、`theme/css/` 或 `theme/includes/fonts.html` 会触发整本重渲染（明暗两套 SASS 各编译一次）。
- 日常查看优先 `quarto render` 后直接打开 `_book/index.html`；只有需要热更新时才开 `quarto preview`。
- **不要每次 preview 都清缓存**；下面「彻底清缓存」只在改完主题/`_quarto.yml` 后样式仍不生效时才用。
- `_book/`、`.quarto/` 是生成产物，不要手动编辑。
- **mermaid 懒加载**：`scripts/build/defer-mermaid.py` 在 CI 渲染后执行（见 `.github/workflows/pages.yml`），本地 render 不自动跑。

## quarto preview 在 Windows 上卡死

```powershell
Get-Process quarto,deno -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item -LiteralPath .quarto -Recurse -Force
quarto preview
```

## 改 _quarto.yml 主题后样式不生效

SASS 缓存落在 `.quarto/` 与全局目录：

```powershell
Get-Process quarto,deno -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item -LiteralPath .quarto -Recurse -Force
Remove-Item -LiteralPath $env:LOCALAPPDATA\quarto -Recurse -Force
Remove-Item -LiteralPath $env:USERPROFILE\.cache\quarto -Recurse -Force
quarto render --to html
```

## 校验 grid 布局是否生效

不要对压缩 CSS 做宽模式全串扫描。确认 `grid.sidebar-width`：

```powershell
Get-ChildItem _book\site_libs\bootstrap -Filter *.min.css | Select-String -SimpleMatch 'minmax(30px, 60px)' | Measure-Object
Get-ChildItem _book\site_libs\bootstrap -Filter *.min.css | Select-String -SimpleMatch 'minmax(60px, 180px)' | Measure-Object
```

或用 `python .cursor/skills/quarto-theme/scripts/check_layout.py`（需先 render）。
