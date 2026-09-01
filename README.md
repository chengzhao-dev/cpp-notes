# C++ 备忘录

基于 [Quarto Book](https://quarto.org/docs/books/) 的 C++ 编程备忘文档，渲染为 HTML 并发布到 GitHub Pages。

## 环境

- 默认环境：**Windows 上的 WSL2** 开发环境，详见 `content/environment/`。
- 示例源码统一放在 `code/` 目录。

## 本地渲染

```bash
quarto render      # 渲染整本 Book，输出到 _book/
quarto preview     # 本地实时预览
git push           # 推送即自动部署（Actions 渲染 → gh-pages 分支 → Pages）
```

> 改 `theme/scss/`（主题 `*.scss`）、`theme/css/`（组件 `*.css`）或 `theme/includes/fonts.html`（全局）会整本重渲染，较慢；`quarto preview` 在 Windows 上偶发卡死，清理方式见 `AGENTS.md`。

## 结构

```
├── _quarto.yml               # Book 配置
├── index.qmd                 # 首页入口
├── content/                  # 备忘录章节（.qmd）
├── code/                     # C++ 示例源码（code/<主题>/<小写下划线>.cpp）
├── theme/                    # 主题：scss/（明暗主题变量）、css/（按域拆分组件规则）、includes/（fonts/footer）
├── scripts/                  # 仓库级构建/CI 脚本（defer-mermaid.py、python.json 本机解释器）
└── .opencode/                # opencode 配置与 skills（agent 工具在各 skill 的 scripts/，均为 Python）
```

## 发布

- 推送到 `main` 后由 `.github/workflows/pages.yml` 自动 `quarto render`，并把 `_book/` 编译产物（纯 HTML/CSS/JS）推到 `gh-pages` 分支发布到 GitHub Pages；`gh-pages` 由工作流维护，不要手动编辑。
- 发布前把 `_quarto.yml` 里的 `repo-url` / `site-url` 占位地址替换为真实仓库。
