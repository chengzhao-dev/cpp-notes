# 主题结构与组件规则（scss 变量 / css 组件）

本文件规定 `theme/scss/`（主题变量）与 `theme/css/`（组件规则）下各文件的职责、组件规则要点、以及**新增配色/callout/组件的流程**。渲染/缓存命令以 `AGENTS.md` 为准；令牌表见 `design-tokens.md`。

## 文件职责

| 文件 | 放什么 | 不放什么 |
|---|---|---|
| `theme/scss/theme-*.scss` | Bootstrap/主题变量（`$primary`、`$body-color`、`$callout-color-*` 等） | 组件规则 |
| `theme/css/tokens.css` | CSS 变量令牌（亮暗两块） | 组件选择器 |
| `theme/css/*.css` | 按域拆分的组件规则；加载顺序 = `_quarto.yml` 的 `css:` 列表 | Bootstrap 变量 |

## 关键结构约定

- **垂直节奏**：块间距由 `#quarto-document-content > *` 与 `section > *` 的上边距统一控制（正文↔代码块 1.375rem、标题上 3.375/2.5/2.0rem 等）。**不要**再对 `pre`/`p` 单独设 `margin-bottom`。
- **顶栏**：与页面同底色 + 底部 1px 发丝线；搜索/主题切换/面包屑用 `--navbar-*` 令牌。
- **章节横线（`---`）**：每个 `##`/`###` 前在 qmd 源写一条 `---`（上下空行）；`##`/`###` 无下边框。`---` 紧贴前段会触发 setext 陷阱（见 quarto-docs pitfalls）。
- **正文链接**：强调色（`--link-color` 橙）+ 细下划线。
- **表格**：无外框/斑马纹，表头底线 + 行 hairline。
- **callout**：左 3px 色条 + 浅底 + 小圆角（Mintlify 语法）；标题在上、内容在下。
- **代码块**：简洁圆角 pre，复制钮 hover/focus 显示；配色交给 `highlight-style: github-light/dark`。
- **侧栏 active**：浅底 + 橙色左轨（`--accent`）。

## 新增 callout 的流程

1. 在 `tokens.css` 加 `--callout-<name>-border` / `--callout-<name>-bg`（亮暗各一对）。
2. 在 `theme-*.scss` 加 `$callout-color-<name>`（与 border 色一致，供图标 data URI）。
3. 在 `callouts.css` 加 `.callout.callout-<name>` 规则。
4. 更新 `design-tokens.md`。

## 校验

用 `scripts/check_layout.py` 或单次字面匹配（勿宽扫 minified Bootstrap CSS）。清 SASS 缓存见 `AGENTS.md`。
