# GitHub Actions

本仓库工作流：`.github/workflows/pages.yml`（发布）、`render-check.yml`（PR 渲染）。

## pages.yml

- 触发：`push` 到 `main`
- 步骤：checkout → setup Quarto → setup Python → `quarto render` → `defer-mermaid.py` → upload `_book` → deploy Pages

## render-check.yml

- 触发：PR 到 `main`
- 步骤：render + defer-mermaid + `verify_examples.py`

## PR 增强（TASK-INFRA-005）

在 `render-check.yml` 追加：

```yaml
      - run: python3 .cursor/skills/cpp-content/scripts/verify_examples.py
```

可选 `--style` 需 WSL 内 clang 工具链，CI 默认仅编译校验。
