# 设计令牌（冷灰 docs 风）

本文件是本仓库明暗双主题的**令牌规范来源**。设计基准：冷灰 docs（对齐 Cursor 文档站冷中性 + Mintlify 式组件）；亮色冷白 `#FFFFFF`、暗色近黑 `#0A0A0A`；强调色 Cursor 橙。实际生效位置在 `theme/css/tokens.css`；二者保持同步。

## 令牌对照表

| 语义 | CSS 变量 | 亮色 | 暗色 |
|---|---|---|---|
| 页面底色 | `--page-bg` | `#FFFFFF` | `#0A0A0A` |
| 浮起面 | `--surface-raised` | `#F7F7F8` | `#141414` |
| 正文 | `--body-color` | `#171717` | `#EDEDED` |
| 次要文字 | `--text-secondary` | `#737373` | `#A3A3A3` |
| 链接/强调 | `--link-color` / `--accent` | `#F54E00` | `#FF6A1A` |
| 正文链接 | `--text-link` | `= --link-color` | `= --link-color` |
| 代码底 | `--code-bg` | `#F7F7F8` | `#141414` |
| 代码边框 | `--code-border` | `#E5E5E5` | `#262626` |
| 表格/卡片边框 | `--table-border` / `--card-border` | `#E5E5E5` | `#262626` |
| 主按钮底 | `--btn-primary-bg` | `#F54E00` | `#FF6A1A` |
| 眉标强调点 | `--dot-accent` | `#F54E00` | `#FF6A1A` |
| 顶栏底 | `--navbar-bg` | `#FFFFFF` | `#0A0A0A` |
| 顶栏文字 | `--navbar-fg` | `#171717` | `#EDEDED` |
| 顶栏次要 | `--navbar-muted` | `#737373` | `#A3A3A3` |

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
- **侧栏 active**：浅底高亮 + 橙色左轨（`--accent`）。
- **首页卡片**：平边框，轻 hover 变边框色，无抬升阴影。

## 字体栈（三处同步）

自托管 OFL 字体（`theme/assets/fonts/` + `theme/css/fonts.css`），无第三方 CDN：

- Sans：`Inter` → `Noto Sans SC` → 系统/CJK 回退（`theme-*.scss`、`tokens.css --ui-font`）
- Mono：`JetBrains Mono` → ui-monospace 回退

## 正文字号（对齐 Cursor docs）

| 元素 | 值 |
|---|---|
| 正文 | 15px / lh 1.625 |
| H1（title） | 33.75px / w400 |
| H2 | 20.625px / w400 / mt 3rem mb 1rem |
| H3 | 18px / w400 |

章节分隔：Quarto 默认 h2 下边框；qmd 不写 `---` 分节线。

## 设计来源

- **布局**：Quarto Book 三栏（左导航 + 正文 + 右 TOC），视觉参考 [cursor.com/cn/docs](https://cursor.com/cn/docs)
- **阅读体例**：渐进式中文、小步展开，参考 [learncpp.com](https://www.learncpp.com/)
- **实现**：Bootstrap cosmo/darkly 基底 + `theme/css/` 域拆分覆盖
