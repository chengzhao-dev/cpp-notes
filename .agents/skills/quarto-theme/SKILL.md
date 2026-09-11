---
name: quarto-theme
description: Quarto Book HTML 主题与设计系统。涉及 .agents/skills/quarto-theme/assets/theme/scss、.agents/skills/quarto-theme/assets/theme/css、includes、设计令牌、布局校验时使用。默认中文。
metadata:
  short-description: Quarto Book HTML 主题与设计令牌
---

# Skill: quarto-theme

明暗双主题采用 GitHub Light / GitHub Dark 色板，保留适合教程阅读的三栏布局。只负责样式与令牌，页面结构交给 `quarto-docs`。

## 适用场景

- 改 `scss/` 变量、`css/` 组件规则、`tokens.css` 令牌、`includes/` 与字体图标资源。
- 校验布局契约、新增配色或 callout、调整代码块外观。
- **不适用**：正文写法与 `.qmd` 结构（转 `quarto-docs`）；改任一主题文件会触发整本重渲染。

## 任务路由

| 任务 | 读取 |
| --- | --- |
| 改任何主题文件（含文件职责、组件规则、新增流程） | `references/theme-system.md` + **目标那一个** css 文件 |
| 改样式的代价与运行边界 | `.agents/skills/agent-ops/references/repository-structure.md` |

禁止通读整个 `.agents/skills/quarto-theme/assets/theme/css/`，禁止为「看一下」加载无关 css。

## P0 硬约束

1. 颜色、字号、间距的唯一出处是 `tokens.css`；组件 css 不写字面色值。
2. 改 `.agents/skills/quarto-theme/assets/theme/**` 或 `_quarto.yml` 前确认整本重渲染代价，改后跑 `run.py render`。
3. 令牌语义、复制按钮作用域、`@media print`、触屏兜底、Mermaid 输出 SVG 由 `check_dom_contracts.py` 断言，改前后各跑一次。
4. 不按字符内容、DOM 位置或命令名覆盖高亮颜色，语义色交给 Pandoc/Quarto token。

## 工作流程

1. 先定位承载该样式的 css 文件，再读它和 `theme-system.md`，不扩散到其他 css；令牌改在 `tokens.css`，组件规则只引用令牌。
2. 新增配色或 callout 按 `references/theme-system.md`「新增流程」四步走完并同步令牌表。
3. 运行 `python .agents/skills/agent-ops/scripts/run.py render`，用产物确认明暗两态。

## 完成判据

- [ ] `run.py check` 全通过，含 `layout`、`dom`、`callouts`、`typography`（有 `_book/` 时该四项必须实际执行，不得 MISS）。
- [ ] 明暗两态与触屏兜底均在渲染产物中确认，无新增色值硬编码。
- [ ] 新增令牌已写回 `references/theme-system.md`。
