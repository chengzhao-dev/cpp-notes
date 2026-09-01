---
name: quarto-theme
description: 维护 Quarto Book 的 HTML 主题与设计系统。当用户涉及 theme/scss/theme-light.scss、theme-dark.scss、theme/css 组件 css（tokens/base/code/content/mermaid/nav/sidebar/callouts/landing/misc）、设计令牌（opencode 暖灰，结构沿用 Primer 值域）、明暗主题配色、导航栏/卡片/callout/代码块/页脚样式、新增配色或 callout、校验布局是否生效时使用。默认用中文回复。
---

# Skill: quarto-theme

# Quarto Book HTML 主题与设计系统

## 角色定位

你是主题/设计系统维护者，负责本仓库 Quarto Book 的**明暗双主题**外观。
设计基准：opencode 暖灰（色温对齐 opencode.ai/docs，结构沿用 GitHub Primer 值域）。
样式实现细节与渲染/缓存命令以 `AGENTS.md` 与 `theme/css/` 组件 css 为准；
本 skill 承载**令牌表 + 主题结构 + 组件规则 + 校验方法**（可移植，随仓库发布）。

## 触发条件

- 修改 `theme/scss/`（`theme-light.scss` / `theme-dark.scss`）、`theme/css/`（按域拆分的组件 `*.css`）或 `theme/includes/`
- 新增/调整配色、callout、卡片、导航栏、代码块、页脚等组件样式
- 校验布局/令牌是否生效（SASS 缓存、`grid.*` 不生效等）
- 需要查询设计令牌（Primer light / Dark Reader dark 的精确值）

## 参考文件

- 设计令牌表（Primer light + Dark Reader dark，映射到 CSS 变量，含 drop-in 片段）：`references/design-tokens.md`
- SCSS/CSS 文件职责 + 组件规则 + 新增配色/callout 流程 + 校验方法：`references/theme-structure.md`
- 校验布局生效：`scripts/check_layout.py`

## 结构（单一信息源）

| 文件 | 职责 |
|---|---|
| `theme/scss/theme-light.scss` | 仅 Bootstrap/主题变量（字体、主色、底色），**不含组件规则** |
| `theme/scss/theme-dark.scss` | 同上（暗色变量） |
| `theme/css/*.css` | 组件规则按域拆分：`tokens` 设计令牌 / `base` 基础排版 / `code` 代码块 / `content` 正文与表格 / `mermaid` 图表 / `nav` 导航与面包屑 / `sidebar` 侧栏与 TOC / `callouts` 提示卡片 / `landing` 首页 / `misc` 页脚与打印；加载顺序 = `_quarto.yml` 的 `css:` 列表，颜色走 `tokens.css` 变量，`body.quarto-light`/`body.quarto-dark` 切换 |

改样式先找对应域的 `theme/css/*.css`。渲染/缓存注意事项见 `AGENTS.md`。

## 快速要点

- 明暗两套 SASS 各编译一次，改 `theme/scss/` 会触发整本重渲染。
- 校验布局用**单次字面匹配**（如 `scripts/check_layout.py` 的子串匹配），
  不要对压缩后大 CSS 做宽模式全串扫描。
- 清理缓存命令与 Windows 卡死处理见 `AGENTS.md`，本 skill 不重复承载。
- 设计令牌值见 `references/design-tokens.md`；新增配色照 `references/theme-structure.md` 的流程走。
