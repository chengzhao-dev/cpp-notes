# GitHub Actions 工作流

本仓库用 Actions 做两件事：**发布 GitHub Pages** 与 **CI 校验（编译示例）**。产物目录：Book 项目是 `_book/`（非 `_site/`）。

## 发布 Pages 的工作流（`.github/workflows/pages.yml`）

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
      - run: python3 scripts/defer-mermaid.py
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: _book
      - id: deployment
        uses: actions/deploy-pages@v4
```

渲染后执行 `python3 scripts/defer-mermaid.py`，给 mermaid 脚本加 `defer`、不阻塞首屏（见 AGENTS.md「mermaid 懒加载」）。

前提：仓库 Settings → Pages → Build and deployment 选 **GitHub Actions**。

## 排错

- 发布没更新：看 Actions 是否成功（失败看日志）；确认上传 `path: _book`（Book 项目）。
- 私有仓库有 Actions 分钟数限制，公开仓库无。
- 缓存/CDN 延迟：等几分钟或强刷新。
