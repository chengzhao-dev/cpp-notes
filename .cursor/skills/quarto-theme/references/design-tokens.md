# 设计令牌（GitHub 风格）

本文件是本仓库明暗双主题的**令牌规范来源**。页面颜色参考 GitHub Light / GitHub Dark，代码高亮由 Quarto 的同名主题提供；实际生效位置在 `theme/css/tokens.css`，二者保持同步。

## 令牌对照表

| 语义 | CSS 变量 | 亮色 | 暗色 |
|---|---|---|---|
| 页面底色 | `--page-bg` | `#FFFFFF` | `#0D1117` |
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

## callout 色（左条 + 浅底）

| callout | 亮色 border / bg | 暗色 border / bg |
|---|---|---|
| note | `#2563EB` / `#EFF6FF` | `#60A5FA` / `#172554` |
| tip | `#16A34A` / `#F0FDF4` | `#4ADE80` / `#14532D` |
| warning | `#D97706` / `#FFFBEB` | `#FBBF24` / `#451A03` |
| important | `#7C3AED` / `#F5F3FF` | `#A78BFA` / `#2E1065` |
| caution | `#DC2626` / `#FEF2F2` | `#F87171` / `#450A0A` |

SASS 层 `$callout-color-*`（`theme-*.scss`）与上表 border 色一致，驱动编译期 callout 图标 data URI。

## 组件约定

- **代码块**：简洁圆角 pre，弱底 + 细边，无顶栏/交通灯；复制钮右上角，hover/focus 显示。
- **Callout**：左 3px 色条 + 浅底 + `border-radius: 6px`；标题在上、内容在下。
- **侧栏 active**：浅底高亮 + GitHub 蓝色左轨（`--accent`）。
- **首页卡片**：平边框，轻 hover 变边框色，无抬升阴影；网格一行最多两列。
- **首页与组件**：采用 GitHub 文档式细边框、冷灰分隔线和轻背景；卡片 hover 只改变边框或背景，不改变尺寸。
- **顶栏品牌标**：与 `theme/assets/favicon.svg` 同源，标签页图标与导航品牌一致。
- **纯文本代码块**：使用与语言代码块相同的 `--code-bg`、`--code-fg`、`--code-border`、字体、内边距和圆角；`text` 内容不启用语言 token。

## 字体栈（三处同步）

自托管 OFL 字体（`theme/assets/fonts/` + `theme/css/fonts.css`），无第三方 CDN：

- Sans：`Inter` → `Noto Sans SC` → 系统/CJK 回退（`theme-*.scss`、`tokens.css --ui-font`）
- Mono：`JetBrains Mono` → `Noto Sans Mono CJK SC` / `Noto Sans SC` → ui-monospace 回退；代码主题使用 GitHub Light / GitHub Dark。代码块统一左对齐，终端输出保留原始空格。

## 正文字号

| 元素 | 值 |
|---|---|
| 正文 | 15px / lh 1.625 |
| H1（title） | 33.75px / w400 |
| H2 | 20.625px / w400 / mt 3rem mb 1rem |
| H3 | 18px / w400 |

章节分隔：Quarto 默认 h2 下边框；qmd 不写 `---` 分节线。

## 设计来源

- **布局**：Quarto Book 三栏（左导航 + 正文 + 右 TOC），页面色彩参考 GitHub 文档界面
- **阅读体例**：渐进式中文、小步展开，参考 [learncpp.com](https://www.learncpp.com/)
- **实现**：Bootstrap cosmo/darkly 基底 + `theme/css/` 域拆分覆盖
