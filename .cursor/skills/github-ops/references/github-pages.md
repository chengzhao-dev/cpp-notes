# 发布到 GitHub Pages

三种发布方式，按需选择。

> **Book 输出目录**：Quarto Book 项目（`project: type: book`）渲染默认输出到 `_book/`（website 是 `_site/`）。发布产物对应 `_book/`，GitHub Actions 上传的 `path` 也相应用 `_book`。

## 方式一：`quarto publish gh-pages`（最简单）

```bash
quarto publish gh-pages 文档.qmd
# 或发布整个 Book 项目：
quarto publish gh-pages
```

- 交互式选择目标 GitHub 仓库后，Quarto 渲染并把产物推送到 `gh-pages` 分支。
- 前提：仓库已在 GitHub；首次运行会引导授权 GitHub。
- 适合：单文档/小站点/Book、快速发布。

## 方式二：渲染到 `docs/` + 分支部署（无 Actions）

1. 在 `_quarto.yml` 设置输出目录（Book 默认 `_book/`，改为 `docs/` 以适配分支部署）：

```yaml
project:
  type: book
  output-dir: docs
```

2. 提交 `docs/` 到仓库（通常推送到 `main`）。
3. 仓库 Settings → Pages → Build and deployment 选择 **Deploy from a branch** → 分支 `main`、目录 `/docs`。

适合：想直接在源码仓库里看到产物、不需要额外工作流。

## 方式三：GitHub Actions（推荐，自动化）

1. Settings → Pages → Build and deployment 选择 **GitHub Actions**。
2. 创建 `.github/workflows/pages.yml`：

```yaml
name: "quarto build & deploy"

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: quarto render
      - run: python3 scripts/build/defer-mermaid.py
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: _book
      - id: deployment
        uses: actions/deploy-pages@v4
```

> Book 项目的产物是 `_book/`，上传 `path` 用 `_book`；website 项目用 `_site`。

适合：多章节 Book、持续集成、团队协作、与 CI 检查（编译/测试）合并。

## 方式四：Actions 渲染 + 推 `gh-pages` 产物分支（本仓库现行模式）

1. Pages 设置选 **Deploy from a branch** → 分支 `gh-pages`、目录 `/ (root)`（可由工作流内调用 Pages API 自动设置，见下）。
2. 工作流渲染后用 `peaceiris/actions-gh-pages@v4` 把 `_book/` 推到 `gh-pages` 分支：

```yaml
permissions:
  contents: write   # 推 gh-pages 分支
  pages: write      # 调 Pages API 自动启用

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: quarto-dev/quarto-actions/setup@v2
      - run: quarto render
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_book
          publish_branch: gh-pages
          force_orphan: true   # 每次部署一个孤立提交，分支只含编译产物 + .nojekyll
```

3. 首次启用可用 API 自动设置源（已配置时返回 409，可继续；失败时在 Settings → Pages 选择 `gh-pages` 分支）：

```bash
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/<owner>/<repo>/pages \
  -d '{"source":{"branch":"gh-pages","path":"/"}}'
```

- 优点：Pages 网页端能看到「实际 HTML」的 `gh-pages` 分支；源码 `main` 与产物分支彻底分离，`force_orphan` 保证产物分支无历史噪音。
- 注意：不再需要 `configure-pages` / `upload-pages-artifact` / `deploy-pages`（那是方式三的 Actions 部署件）；`id-token: write` 也不需要。

## 站点路径与 baseurl

- GitHub Pages 站点 URL 形如 `https://<user>.github.io/<repo>/`（项目站点）或 `https://<user>.github.io/`（用户/组织站点）。
- 项目站点下相对链接要保证正确：优先使用**相对路径**，避免写死绝对 URL。
- Book 的章节导航由 `book.chapters` 生成；站点型导航用 `_quarto.yml` 的 `website` 配置管理（navbar/sidebar），链接用 `href: xxx.qmd`，Quarto 渲染时自动修正。

## 发布前检查清单

- [ ] 本地 `quarto render` 通过，无错误
- [ ] 相对链接/图片路径正确（本地预览与线上一致）
- [ ] 需要单文件时已设 `embed-resources: true`
- [ ] 中文内容为 UTF-8，无乱码
- [ ] Book 入口页（`index.qmd`）存在，作为首页
- [ ] GitHub Pages 已启用且部署方式与选择匹配（Actions 或 branch）
- [ ] 示例均经 `.cursor/skills/cpp-content/scripts/verify_examples.py` 编译校验（见 cpp-content skill）
