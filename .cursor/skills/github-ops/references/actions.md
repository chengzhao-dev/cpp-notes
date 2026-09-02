# GitHub Actions

本仓库工作流：`.github/workflows/pages.yml`（发布）、`render-check.yml`（PR 渲染）。

## pages.yml

- 触发：`push` 到 `main`，或 `workflow_dispatch`
- 步骤：checkout → setup Quarto → setup Python → `quarto render` → `scripts/build/defer-mermaid.py` → `peaceiris/actions-gh-pages` 推 `_book/` 到 `gh-pages`（`force_orphan`）→ 可选校正 Pages source
- 权限：`contents: write`（推分支）、`pages: write`（调 Pages API）
- Pages 设置：Deploy from a branch → `gh-pages` / `(root)`（见 `github-pages.md` 方式四）

## render-check.yml

- 触发：PR 到 `main`
- 步骤：render + defer-mermaid + `verify_examples.py`

## PR 增强（TASK-INFRA-005）

在 `render-check.yml` 追加：

```yaml
      - run: python3 .cursor/skills/cpp-content/scripts/verify_examples.py
```

可选 `--style` 需 WSL 内 clang 工具链，CI 默认仅编译校验。
