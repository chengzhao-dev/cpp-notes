---
name: designing-theme
description: Quarto Book HTML 主题与设计系统。涉及 .agents/skills/designing-theme/assets/theme/palettes、.agents/skills/designing-theme/assets/theme/css、includes、设计令牌、布局校验时使用。默认中文。
metadata:
  short-description: Quarto Book HTML 主题与设计令牌
---

# Skill: designing-theme

明暗双主题采用可切换 palette pack；生产默认是 GitHub Light / GitHub Dark。只负责样式与令牌，页面结构交给 `writing-quarto`。

## 适用场景

- 改 `palettes/<name>/` 色板、`css/` 组件规则、共享 `tokens.css`、`includes/` 与字体图标资源。
- 校验布局契约、新增配色或 callout、调整代码块外观。
- **不适用**：正文写法与 `.qmd` 结构（转 `writing-quarto`），改任一主题文件会触发整本重渲染。

## 任务路由

| 任务 | 读取 |
| --- | --- |
| 改任何主题文件（含文件职责、组件规则、阅读密度与首页 Hero） | `references/theme-system.md` + **目标那一个** css 文件 |
| 改配色 / 切换色板 | `references/theme-system.md` + 目标 `palettes/<name>/`（tokens、scss、meta）；不改组件 CSS |
| 改样式的代价与运行边界 | `.agents/skills/governing-agents/references/repository-structure.md` |

禁止通读整个 `.agents/skills/designing-theme/assets/theme/css/`，禁止为「看一下」加载无关 css。
## P0 硬约束

1. 页面语义颜色来自活跃 `palettes/<name>/tokens.css`；结构尺度来自共享 `css/tokens.css`。组件 css 不写十六进制或 `rgb()` 色值，一次性几何值可以保留在组件内。
2. 改 `.agents/skills/designing-theme/assets/theme/**` 或 `_quarto.yml` 前确认整本重渲染代价，改后跑 `run.py render`。
3. 代码标题、令牌语义、复制按钮作用域、`@media print`、触屏兜底与 Mermaid SVG 由 `check_dom_contracts.py` 断言，改前后各跑一次。
4. 不按字符内容、DOM 位置或命令名覆盖高亮颜色，语义色交给 Pandoc/Quarto token。
5. 正文使用自托管 `Fixel Text`、`LXGW WenKai Screen`，代码使用 `LXGW Bright Code`，中文回退仍为 `LXGW WenKai Screen`。改字体前必须同步 3 个 Fixel 字重、2 个 common 汉字包、`fonts.css`、SCSS 字体栈、CSS 令牌、OFL 说明和覆盖检查。
6. ≤991.98px 时左侧栏变成覆盖正文的浮层，必须有实色底；浮层透底会让正文文字叠在侧栏上，由 `check_layout.py` 断言。

## 工作流程

1. 先定位承载该样式的 css 或 palette 文件，再读它和 `theme-system.md`，不扩散到其他 css。颜色改在活跃 pack，结构尺度改在共享 `tokens.css`，组件规则只引用令牌。
2. 新增配色或 callout 按 `references/theme-system.md`「新增流程」四步走完并同步令牌表。
3. 运行 `& .agents/skills/governing-agents/scripts/run.ps1 render --require-browser`，用产物确认明暗两态、移动端与触屏兜底。

## 完成判据

- [ ] 发布验收用 `render --require-browser`，`layout`/`dom`/`callouts` 必须通过；`layout` 覆盖 `1280/768/390` 明暗两态、触屏复制与窄屏浮层不透明，不可用时明确 SKIP。
- [ ] 新增令牌已写回 `references/theme-system.md`。
