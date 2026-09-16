# 主题系统（设计令牌与文件结构）

## 设计令牌（GitHub 风格）

本文件说明令牌语义、组件映射与新增流程。实际生效值只写在
`.agents/skills/quarto-theme/assets/theme/css/tokens.css`，本文件不维护数值副本。

### 令牌索引

| 语义 | CSS 变量 | 使用边界 |
|---|---|---|
| 页面底色 / 浮起面 | `--page-bg` / `--surface-raised` | 页面与抬升表面 |
| 正文最大宽度 | `--content-width` | 正文容器上限，不是段落二次限宽 |
| 正文 / 次要文字 | `--body-color` / `--text-secondary` | 正文层级 |
| 链接 / 强调 | `--link-color` / `--accent` / `--text-link` | 链接和交互强调 |
| 代码外观 | `--code-*` / `--code-title-*` | 语言块、纯文本块与代码标题 |
| 表格 / 卡片边框 | `--table-border` / `--card-border` | 分隔与边框 |
| 按钮 / 眉标 | `--btn-primary-*` / `--dot-accent` | 首页与状态强调 |
| 顶栏 | `--navbar-*` | 导航、搜索与主题切换 |

### callout 色（左条 + 浅底）

每个内置 callout 都有一对 `--callout-<type>-border` / `-bg`，值只写在
`tokens.css`。SCSS 的 `$callout-color-*` 必须与对应 border 令牌同步，用于生成
编译期图标 data URI。

### 组件约定

- **代码块**：弱底 + 细边。有 `filename` 时使用标题条，无交通灯，复制钮右上角。
- **Callout**：左 3px 色条 + 浅底 + `border-radius: 6px`，标题在上、内容在下。正文与页面正文同为 16px，标题为 15px。可选内容靠容器区分，不靠缩小字号。
- **侧栏 active**：浅底高亮 + GitHub 蓝色左轨（`--accent`）。
- **首页卡片**：平边框，轻 hover 变边框色，无抬升阴影，网格一行最多两列。根首页 Hero 无框左对齐。
- **首页与组件**：采用 GitHub 文档式细边框、冷灰分隔线和轻背景，卡片 hover 只改变边框或背景，不改变尺寸。
- **顶栏品牌标**：与 `.agents/skills/quarto-theme/assets/theme/assets/favicon.svg` 同源，标签页图标与导航品牌一致。
- **纯文本代码块**：使用与语言代码块相同的 `--code-bg`、`--code-fg`、`--code-border`、字体、内边距和圆角，`text` 内容不启用语言 token。
- **`.code-caption`**：图或代码块的一句附属说明，`--text-secondary` 次要文字色、字号略小，紧贴所描述对象（`base.css` 已压缩其与代码块的间距），写作侧规则见 quarto-docs `authoring.md`。
- **可折叠答案**：`details.answer-disclosure` 使用原生 `summary` 展开，默认收起，边框和圆角与卡片一致。`summary` 直接承载固定摘要文本，明暗两态共用令牌。

### 页面列宽与正文宽度

- Quarto `grid.body-width` 是正文列的上限。sidebar、body、margin 与两条 gutter 的合计超过视口时，浏览器会压缩正文列。当前取值只在 `_quarto.yml` 维护。
- `--content-width` 只限制正文容器的最大宽度，不代表每个段落都必须再按字符数收窄。
- 普通段落、列表、代码块、表格和 callout 使用实际正文列宽。首页标题描述可以单独使用 `ch` 控制导语长度。
- 主题 CSS 不得用 `75ch` 等第二层限制覆盖正文列。窄屏由父容器缩放，内容保持 `max-width: 100%` 并避免横向溢出。

### 字体栈（三处同步）

自托管 OFL 字体（`assets/fonts/` + `css/fonts.css`），无第三方 CDN：

- Sans：`Fixel Text` → `LXGW WenKai Screen` → 系统中西文回退（`theme-*.scss`、`tokens.css --ui-font`）。
- Mono：`LXGW Bright Code` → `LXGW WenKai Screen` → ui-monospace 回退。代码主题使用 GitHub Light / GitHub Dark。

Fixel 使用 500/600/700。LXGW Screen v1.522 与 Bright Code v2.922 Regular 各打包为一个常用字符集 WOFF2，覆盖当前公开内容与一级常用汉字；未覆盖字符回退系统字体。Bright Code 的拉丁来自 Monaspace Argon，中文来自霞鹜文楷，缺字回退 WenKai Screen。网页子集由临时 fontTools 生成。变更需同步 SCSS、tokens、fonts、OFL、资产文件与 `check_layout.py`。单页最多请求 5 个字体文件，预算为 1.6 MB。字体资产由检查器核对 URL、数量、签名和孤儿文件，数值间距以 `tokens.css` 为准。

### 正文字号

| 元素 | 值 |
|---|---|
| 正文 | 16px / lh 1.65 |
| H1（title） | 32px / w600 |
| H2 | 24px / w600 / mt 2.75rem mb 0.9rem |
| H3 | 20px / w600 / mt 2rem |
| 代码块 | 15px / lh 1.65 |
| 行内代码 | 0.875em |
| Callout 正文 | 16px / lh 1.65 |
| Callout 标题 | 15px / w600 |

章节分隔：Quarto 默认 h2 下边框，qmd 不写 `---` 分节线。

### 设计来源

布局采用 Quarto Book 三栏，页面色彩和组件规则参考 GitHub 文档，阅读体例参考渐进式教程。实现为 Bootstrap cosmo/darkly 与主题 CSS 覆盖。

## 主题结构与组件规则（scss 变量 / css 组件）
官方字段依据 Quarto [HTML format reference](https://quarto.org/docs/reference/formats/html.html)；以下 CSS/SCSS 选择器、令牌和装配顺序是本项目契约，不是 Quarto 内置 API。

本文件规定 `.agents/skills/quarto-theme/assets/theme/scss/`（主题变量）与 `.agents/skills/quarto-theme/assets/theme/css/`（组件规则）下各文件的职责、组件规则要点、以及**新增配色/callout/组件的流程**。渲染/缓存命令以 `AGENTS.md` 为准。令牌表见本文件「设计令牌」。

### 文件职责

| 文件 | 放什么 | 不放什么 |
|---|---|---|
| `.agents/skills/quarto-theme/assets/theme/scss/theme-*.scss` | Bootstrap/主题变量（`$primary`、`$body-color`、`$callout-color-*` 等） | 组件规则 |
| `.agents/skills/quarto-theme/assets/theme/css/tokens.css` | CSS 变量令牌（亮暗两块） | 组件选择器 |
| `.agents/skills/quarto-theme/assets/theme/css/*.css` | 按域拆分的组件规则。加载顺序 = `_quarto.yml` 的 `css:` 列表 | Bootstrap 变量 |

### 关键结构约定

- **垂直节奏**：块间距由正文容器与 section 的 `* + *` 上边距控制（标题上距 2.75/2/2rem），不要再对 `pre`/`p` 单独设 `margin-bottom`。
- **顶栏**：与页面同底色 + 底部 1px 发丝线，搜索/主题切换/面包屑用 `--navbar-*` 令牌。
- **正文链接**：使用 `--link-color` 强调色与细下划线。
- **表格**：无外框/斑马纹，表头底线 + 行 hairline。
- **callout**：左 3px 色条 + 浅底 + 小圆角（Mintlify 语法），标题在上、内容在下。
- **侧栏 active**：浅底 + GitHub 蓝左轨（`--accent`）。

### 新增 callout 的流程

1. 在 `tokens.css` 加 `--callout-<name>-border` / `--callout-<name>-bg`（亮暗各一对）。
2. 在 `theme-*.scss` 加 `$callout-color-<name>`（与 border 色一致，供图标 data URI）。
3. 在 `callouts.css` 加 `.callout.callout-<name>` 规则。
4. 如有新增语义，补入本文件第一节令牌索引。

### 校验

用 `scripts/check_layout.py` 校验令牌、资产和可用的浏览器几何。发布验收覆盖
`1280/768/390` 的明暗两态和触屏复制按钮。需要刷新编译缓存时执行一次完整渲染。

### 代码高亮契约

- 亮色 `github-light`、暗色 `github-dark`，配置唯一来源是 `_quarto.yml`。
- 语义颜色由 Pandoc/Quarto 的 token 提供，CSS 只负责背景、布局、字体和稳定的基础色。
- 括号、标点、`$`、版本号和普通输出必须保持连续的基础色，不按命令名或字符内容覆盖。
- `text` 代码块用于命令输出和纯文本演示，不启用语言高亮，但与 `cpp`、`cmake`、`bash`、`powershell` 共用字体、字号、行高和字重。
- 三类代码块（`text`、语言代码块、`include` 代码）共用 `--code-*` 与 `--code-title-*` 令牌。有标题时由 `.code-with-filename` 统一顶部圆角和分隔线。

### 产物契约断言

`.agents/skills/agent-ops/scripts/check_dom_contracts.py` 断言以下项，改 DOM 相关样式前后各跑一次：

- GitHub 明暗高亮主题与代码 token 不得被组件选择器覆盖。
- 语言代码块与纯文本代码块共享背景、边框、字体和圆角。代码块本身不出现框中框。
- 复制按钮 hover 作用域限定在 `.code-copy-outer-scaffold`（Quarto 1.10 起按钮与 `div.sourceCode` 是兄弟）。
- `@media print` 不得隐藏 scaffold 本身。`@media (hover: none)` 提供触屏兜底。
- 有 `filename` 的代码块生成来源标题，复制按钮不遮挡标题。
- favicon 注入与发布。Mermaid 输出 SVG 而不是源码块。
