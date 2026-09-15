---
name: quarto-theme
description: Quarto Book HTML 主题与设计系统。涉及 .agents/skills/quarto-theme/assets/theme/scss、.agents/skills/quarto-theme/assets/theme/css、includes、设计令牌、布局校验时使用。默认中文。
metadata:
  short-description: Quarto Book HTML 主题与设计令牌
---

# Skill: quarto-theme

明暗双主题采用 GitHub Light / GitHub Dark 色板，保留适合教程阅读的三栏布局。只负责样式与令牌，页面结构交给 `quarto-docs`。

正文列宽由 `_quarto.yml` 的 Quarto grid 与 `tokens.css` 的 `--content-width` 共同决定。普通段落和列表应占满实际正文列，不能在组件 CSS 中再次用 `ch` 限宽；只有首页标题描述等明确的短导语才保留独立的阅读宽度。
## 适用场景

- 改 `scss/` 变量、`css/` 组件规则、`tokens.css` 令牌、`includes/` 与字体图标资源。
- 校验布局契约、新增配色或 callout、调整代码块外观。
- **不适用**：正文写法与 `.qmd` 结构（转 `quarto-docs`），改任一主题文件会触发整本重渲染。

## 任务路由

| 任务 | 读取 |
| --- | --- |
| 改任何主题文件（含文件职责、组件规则、阅读密度与首页 Hero） | `references/theme-system.md` + **目标那一个** css 文件 |
| 改样式的代价与运行边界 | `.agents/skills/agent-ops/references/repository-structure.md` |

禁止通读整个 `.agents/skills/quarto-theme/assets/theme/css/`，禁止为「看一下」加载无关 css。
## P0 硬约束

1. 页面语义颜色和跨组件共享尺度只从 `tokens.css` 引用；组件 css 不写十六进制或 `rgb()` 色值，一次性几何值可以保留在组件内。
2. 改 `.agents/skills/quarto-theme/assets/theme/**` 或 `_quarto.yml` 前确认整本重渲染代价，改后跑 `run.py render`。
3. 代码标题、令牌语义、复制按钮作用域、`@media print`、触屏兜底与 Mermaid SVG 由 `check_dom_contracts.py` 断言，改前后各跑一次。
4. 不按字符内容、DOM 位置或命令名覆盖高亮颜色，语义色交给 Pandoc/Quarto token。
5. 正文使用自托管 `Fixel Text`、`LXGW WenKai Screen`，代码使用 `LXGW Bright Code`，中文回退仍为 `LXGW WenKai Screen`。改字体前必须同步 16 个 WenKai 与 16 个 Bright Code 分包、`fonts.css`、SCSS 字体栈、CSS 令牌、OFL 说明和覆盖检查。

## 工作流程

1. 先定位承载该样式的 css 文件，再读它和 `theme-system.md`，不扩散到其他 css。令牌改在 `tokens.css`，组件规则只引用令牌。
2. 新增配色或 callout 按 `references/theme-system.md`「新增流程」四步走完并同步令牌表。
3. 运行 `& .agents/skills/agent-ops/scripts/run.ps1 render --require-browser`，用产物确认明暗两态、移动端与触屏兜底。

## 完成判据

- [ ] 发布验收用 `render --require-browser`，`layout`、`dom`、`callouts` 必须实际执行且通过。
- [ ] `layout` 覆盖 `1280/1100/768/390` 的明暗两态，并确认触屏复制按钮可见；不可用时明确显示 SKIP，不宣称已验证。
- [ ] 新增令牌已写回 `references/theme-system.md`。
