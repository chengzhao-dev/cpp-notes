# 发布到 GitHub Pages（操作清单）

本文件只放「怎么做」。为什么这样选、失效模式与取舍依据在知识库，一条命令取用：

```powershell
& .agents/skills/agent-ops/scripts/run.ps1 kb-search "GitHub Pages 部署方式与产物分支" --domain github-ops
```

> Book 输出目录是 `_book/`（website 为 `_site/`），上传 `path` 与 `publish_dir` 都跟着用 `_book`。

## 本仓库现行模式

Actions 渲染 + 推 `gh-pages` 产物分支，配置在 `.github/workflows/pages.yml`：

1. Pages 设置选 **Deploy from a branch** → 分支 `gh-pages`、目录 `/ (root)`。
2. `quarto render` → `python3 .agents/skills/python-tools/scripts/render/defer_mermaid.py`（本地 render 不自动跑，CI 必须执行）。
3. `peaceiris/actions-gh-pages@v4` 上传 `./_book` 到 `gh-pages`，`force_orphan: true`。
4. 幂等纠正 Pages 源：先 POST 再 PUT，返回 409 属正常，非 2xx/409 时提示去 Settings → Pages 手工选择。
5. `permissions` 只需 `contents: write` 与 `pages: write`。不用 `configure-pages`/`upload-pages-artifact`/`deploy-pages`，也不需要 `id-token: write`。

## 备选模式（新项目或无 Actions 时）

| 模式 | 关键步骤 | 适用 |
|---|---|---|
| `quarto publish gh-pages` | 交互式选仓库后自动渲染并推 `gh-pages` | 单文档、小站点、快速发布 |
| 渲染到 `docs/` + 分支部署 | `_quarto.yml` 设 `project.output-dir: docs`，提交后选 `main` + `/docs` | 想在源码仓库直接看到产物 |
| Actions 平台部署件 | Settings → Pages 选 **GitHub Actions**，走 `configure-pages` → `upload-pages-artifact` → `deploy-pages` | 与 CI 检查合并、团队协作 |

## 发布前检查清单

- [ ] 本地 `quarto render` 通过，无错误
- [ ] 相对链接与图片路径在带仓库名前缀的项目站点下仍正确
- [ ] 需要单文件时已设 `embed-resources: true`
- [ ] 中文内容为 UTF-8 无 BOM，无乱码
- [ ] Book 入口页 `index.qmd` 存在，作为首页
- [ ] 部署源（分支 + 目录或工作流）与所选模式匹配
- [ ] 示例经 `.agents/skills/cpp-content/scripts/verify_examples.py` 编译校验

## 页面未更新时的处置

1. 先看工作流是否成功，再核对部署源的分支与目录，最后才考虑缓存与分发延迟。
2. 任务成功但页面未变时不要重复触发部署。原因未确认前重复部署只会加深半更新风险。
3. 本地正常、线上 404 优先查文件名大小写。
