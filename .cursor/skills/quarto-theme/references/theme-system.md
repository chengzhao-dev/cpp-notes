# 主题系统（设计令牌与文件结构）

## 设计令牌（GitHub 风格）

本文件是本仓库明暗双主题的**令牌规范来源**。页面颜色参考 GitHub Light / GitHub Dark，代码高亮由 Quarto 的同名主题提供；实际生效位置在 `.cursor/skills/quarto-theme/assets/theme/css/tokens.css`，二者保持同步。

### 令牌对照表

| 语义 | CSS 变量 | 亮色 | 暗色 |
|---|---|---|---|
| 页面底色 | `--page-bg` | `#FFFFFF` | `#0D1117` |
| 正文最大宽度 | `--content-width` | `800px` | `800px` |
| 浮起面 | `--surface-raised` | `#F6F8FA` | `#161B22` |
| 正文 | `--body-color` | `#1F2328` | `#E6EDF3` |
| 次要文字 | `--text-secondary` | `#656D76` | `#8B949E` |
| 链接/强调 | `--link-color` / `--accent` | `#0969DA` | `#4493F8` |
| 正文链接 | `--text-link` | `= --link-color` | `= --link-color` |
| 代码底 | `--code-bg` | `#FFFFFF` | `#0D1117` |
| 代码文字 | `--code-fg` | `#1F2328` | `#E6EDF3` |
| 代码边框 | `--code-border` | `#D0D7DE` | `#30363D` |
| 代码内边距 | `--code-padding` | `0.75rem 1rem` | `0.75rem 1rem` |
| 代码圆角 | `--code-radius` | `6px` | `6px` |
| 表格/卡片边框 | `--table-border` / `--card-border` | `#D0D7DE` | `#30363D` |
| 主按钮底 | `--btn-primary-bg` | `#1F883D` | `#238636` |
| 眉标强调点 | `--dot-accent` | `#1F883D` | `#3FB950` |
| 顶栏底 | `--navbar-bg` | `#FFFFFF` | `#0D1117` |
| 顶栏文字 | `--navbar-fg` | `#1F2328` | `#E6EDF3` |
| 顶栏次要 | `--navbar-muted` | `#656D76` | `#8B949E` |

### callout 色（左条 + 浅底）

| callout | 亮色 border / bg | 暗色 border / bg |
|---|---|---|
| note | `#2563EB` / `#EFF6FF` | `#60A5FA` / `#172554` |
| tip | `#16A34A` / `#F0FDF4` | `#4ADE80` / `#14532D` |
| warning | `#D97706` / `#FFFBEB` | `#FBBF24` / `#451A03` |
| important | `#7C3AED` / `#F5F3FF` | `#A78BFA` / `#2E1065` |
| caution | `#DC2626` / `#FEF2F2` | `#F87171` / `#450A0A` |

SASS 层 `$callout-color-*`（`theme-*.scss`）与上表 border 色一致，驱动编译期 callout 图标 data URI。

### 组件约定

- **代码块**：简洁圆角 pre，弱底 + 细边，无顶栏/交通灯；复制钮右上角，hover/focus 显示。
- **Callout**：左 3px 色条 + 浅底 + `border-radius: 6px`；标题在上、内容在下。
- **侧栏 active**：浅底高亮 + GitHub 蓝色左轨（`--accent`）。
- **首页卡片**：平边框，轻 hover 变边框色，无抬升阴影；网格一行最多两列。
- **首页与组件**：采用 GitHub 文档式细边框、冷灰分隔线和轻背景；卡片 hover 只改变边框或背景，不改变尺寸。
- **顶栏品牌标**：与 `.cursor/skills/quarto-theme/assets/theme/assets/favicon.svg` 同源，标签页图标与导航品牌一致。
- **纯文本代码块**：使用与语言代码块相同的 `--code-bg`、`--code-fg`、`--code-border`、字体、内边距和圆角；`text` 内容不启用语言 token。

### 字体栈（三处同步）

自托管 OFL 字体（`.cursor/skills/quarto-theme/assets/theme/assets/fonts/` + `.cursor/skills/quarto-theme/assets/theme/css/fonts.css`），无第三方 CDN：

- Sans：`Inter` → `Noto Sans SC` → 系统/CJK 回退（`theme-*.scss`、`tokens.css --ui-font`）
- Mono：`JetBrains Mono` → `Noto Sans Mono CJK SC` / `Noto Sans SC` → ui-monospace 回退；代码主题使用 GitHub Light / GitHub Dark。代码块统一左对齐，终端输出保留原始空格。

### 正文字号

| 元素 | 值 |
|---|---|
| 正文 | 16px / lh 1.75 |
| H1（title） | 32px / w600 |
| H2 | 24px / w600 / mt 3rem mb 1rem |
| H3 | 20px / w600 |

章节分隔：Quarto 默认 h2 下边框；qmd 不写 `---` 分节线。

### 设计来源

- **布局**：Quarto Book 三栏（左导航 + 正文 + 右 TOC），页面色彩参考 GitHub 文档界面
- **阅读体例**：渐进式中文、小步展开，参考 [learncpp.com](https://www.learncpp.com/)
- **实现**：Bootstrap cosmo/darkly 基底 + `.cursor/skills/quarto-theme/assets/theme/css/` 域拆分覆盖

## 主题结构与组件规则（scss 变量 / css 组件）
官方字段依据 Quarto [HTML format reference](https://quarto.org/docs/reference/formats/html.html)；以下 CSS/SCSS 选择器、令牌和装配顺序是本项目契约，不是 Quarto 内置 API。

本文件规定 `.cursor/skills/quarto-theme/assets/theme/scss/`（主题变量）与 `.cursor/skills/quarto-theme/assets/theme/css/`（组件规则）下各文件的职责、组件规则要点、以及**新增配色/callout/组件的流程**。渲染/缓存命令以 `AGENTS.md` 为准；令牌表见本文件「设计令牌」。

### 文件职责

| 文件 | 放什么 | 不放什么 |
|---|---|---|
| `.cursor/skills/quarto-theme/assets/theme/scss/theme-*.scss` | Bootstrap/主题变量（`$primary`、`$body-color`、`$callout-color-*` 等） | 组件规则 |
| `.cursor/skills/quarto-theme/assets/theme/css/tokens.css` | CSS 变量令牌（亮暗两块） | 组件选择器 |
| `.cursor/skills/quarto-theme/assets/theme/css/*.css` | 按域拆分的组件规则；加载顺序 = `_quarto.yml` 的 `css:` 列表 | Bootstrap 变量 |

### 关键结构约定

- **垂直节奏**：块间距由 `#quarto-document-content > *` 与 `section > *` 的上边距统一控制（正文↔代码块 1.375rem、标题上 3.375/2.5/2.0rem 等）。**不要**再对 `pre`/`p` 单独设 `margin-bottom`。
- **顶栏**：与页面同底色 + 底部 1px 发丝线；搜索/主题切换/面包屑用 `--navbar-*` 令牌。
- **章节横线（`---`）**：每个 `##`/`###` 前在 qmd 源写一条 `---`（上下空行）；`##`/`###` 无下边框。`---` 紧贴前段会触发 setext 陷阱（见 quarto-docs pitfalls）。
- **正文链接**：强调色（`--link-color` 橙）+ 细下划线。
- **表格**：无外框/斑马纹，表头底线 + 行 hairline。
- **callout**：左 3px 色条 + 浅底 + 小圆角（Mintlify 语法）；标题在上、内容在下。
- **代码块**：简洁圆角 pre，复制钮 hover/focus 显示；配色交给 `highlight-style: github-light/dark`。
- **侧栏 active**：浅底 + 橙色左轨（`--accent`）。

### 新增 callout 的流程

1. 在 `tokens.css` 加 `--callout-<name>-border` / `--callout-<name>-bg`（亮暗各一对）。
2. 在 `theme-*.scss` 加 `$callout-color-<name>`（与 border 色一致，供图标 data URI）。
3. 在 `callouts.css` 加 `.callout.callout-<name>` 规则。
4. 把令牌写回本文件第一节令牌表。

### 校验

用 `scripts/check_layout.py` 或单次字面匹配（勿宽扫 minified Bootstrap CSS）。清 SASS 缓存见 `AGENTS.md`。

### 代码高亮契约

- 亮色 `github-light`、暗色 `github-dark`，配置唯一来源是 `_quarto.yml`。
- 语义颜色由 Pandoc/Quarto 的 token 提供，CSS 只负责背景、布局、字体和稳定的基础色。
- 括号、标点、`$`、版本号和普通输出必须保持连续的基础色，不按命令名或字符内容覆盖。
- `text` 代码块用于命令输出和纯文本演示，不启用语言高亮，但与 `cpp`、`cmake`、`bash`、`powershell` 共用字体、字号、行高和字重。
- 三类代码块（`text`、语言代码块、`include` 代码）共用内边距、边框和 `--code-*` 令牌；页面明暗使用 GitHub 中性灰、蓝色链接和绿色状态色。

### 产物契约断言

`.cursor/skills/agent-ops/scripts/check_dom_contracts.py` 断言以下项，改 DOM 相关样式前后各跑一次：

- 复制按钮 hover 作用域限定在 `.code-copy-outer-scaffold`（Quarto 1.10 起按钮与 `div.sourceCode` 是兄弟）。
- `@media print` 不得隐藏 scaffold 本身；`@media (hover: none)` 提供触屏兜底。
- favicon 注入与发布；Mermaid 输出 SVG 而不是源码块。
