# 主题结构与组件规则（scss 变量 / css 组件）

本文件规定 `theme/scss/`（主题变量）与 `theme/css/`（组件规则）下各文件的职责、组件规则要点、以及**新增配色/callout/组件的流程**。渲染/缓存命令以 `AGENTS.md` 为准。

## 文件职责（单一信息源）

| 文件 | 放什么 | 不放什么 |
|---|---|---|
| `theme/scss/theme-light.scss` | 仅 Bootstrap/主题变量（`$font-*`、`$primary`、`$body-color`、`$navbar-*`、`$line-height-base` 等） | 组件规则 |
| `theme/scss/theme-dark.scss` | 同上（暗色变量） | 组件规则 |
| `theme/css/tokens.css` | CSS 变量令牌（`--body-color` 等，亮暗两块），颜色走变量，`body.quarto-light`/`body.quarto-dark` 切换 | Bootstrap 变量（除非需覆盖组件默认） |
| `theme/css/base.css` 等组件 css | 组件规则按域拆分：`base` 排版 / `code` 代码块 / `content` 正文与表格 / `mermaid` 图表 / `nav` 导航 / `sidebar` 侧栏 / `callouts` 提示卡片 / `landing` 首页 / `misc` 页脚打印；加载顺序 = `_quarto.yml` 的 `css:` 列表 | Bootstrap 变量（除非需覆盖组件默认） |

## 关键结构约定

- **垂直节奏**：块间距由 `#quarto-document-content > *` 与 `section > *` 的上边距节奏统一控制
  （正文↔代码块 1.375rem、代码块↔代码块 1.5rem、说明段紧贴代码块 0.5rem、
  标题上 3.375/2.5/2.0rem、标题下紧贴首段 0.75rem）。
  **不要**再对 `pre`/`p` 单独设 `margin-bottom`。
- **顶栏（opencode 风，与页面同底色）**：亮暗两态顶栏均与页面同底
  （`--navbar-bg` `#fdfcfc`/`#131010` 暖灰），文字用 `--navbar-fg`（正文色），仅底部 1px 发丝线分隔；
  品牌图标走 `mask` + `currentColor`。
  搜索框/主题切换/面包屑/汉堡按钮一律用 `--navbar-*` / 正文令牌，不要写死颜色。
- **章节横线（`---`）**：每个 `##`/`###` 前在 qmd 源写一条 `---`（上下空行），渲染为 `<hr>` 细线，
  由「段落节奏」3.375rem 上距承托；`##`/`###` **不再**有下边框（旧 `border-bottom` 已移除）。
  `---` 紧贴前段会触发 setext 标题陷阱（见 quarto-docs pitfalls 第 11 条）。
- **正文链接（近黑常驻下划线）**：`#quarto-document-content a` 用 `--text-link`（= 正文色）＋常驻细下划线，hover 不变色；UI 强调（CTA/复制按钮/focus ring/卡片 hover 边）仍走 `--link-color` 蓝。标题锚点 `#` 用次要灰。
- **表格（opencode 风）**：无外框/圆角/斑马纹，表头底线 + 行 hairline（`--table-hairline`），表头 uppercase 600 / 0.8125rem / letter-spacing .5px，td 0.875rem、首尾列贴边。
- **callout（opencode aside 风）**：无边框、无左条、无圆角，仅彩色低饱和底；标题 0.8125rem / 700 / letter-spacing .5px（中文无影响），内容略小一档（0.9375rem）。
- **主按钮（绿底白字）令牌与使用规范**：`--btn-primary-bg`（Primer 绿）+ `--btn-primary-fg`（白）已定义。
  绿色底 + 白字**仅用于「页面唯一主操作」按钮**
  （对齐 gitcn.org / GitHub Primer：Merge pull request、Confirm merge、Copy Exercise、「前往 GitHub 实操练习」均为此类），
  一个页面最多一个；链接、导航、次要操作一律不用绿底。
  需要时按下表 Primer 完整状态实现：

  | 状态 | 亮色 | 暗色 |
  |---|---|---|
  | rest | 底 `#1f883d` / 白字 / 边框 `rgba(31,35,40,.15)` / 阴影 `0 1px 0 rgba(31,35,40,.1)` / 高 32px / 圆角 6px | 底 `#238636` |
  | hover | 底 `#1a7f37` | 底 `#29903b` |
  | active | 底 `hsla(137,66%,28%,1)` + inset 阴影 `inset 0 1px 0 rgba(0,45,17,.2)` | 同左 |
  | focus | 2px 蓝环 `var(--accent)`，outline-offset -2px | 同左 |
  | disabled | 底 `#94d3a2` + 80% 白字 | 底 `#238636` 降透明度 |

  当前首页 hero 不用独立绿按钮，CTA 统一为卡片内蓝链 `.landing-card a.cta`。
- **代码配色交给高亮**：`highlight-style: github-light`/`github-dark`，`code.css` 不再给代码块额外配色。

## 新增配色 / callout 的流程

1. 在 `theme/css/tokens.css` 的 `body{}`（亮）与 `body.quarto-dark{}`（暗）各加一对变量：`--callout-<name>-border` / `--callout-<name>-bg`。
2. 在 callout 规则区加 `.callout.callout-<name>`（无边框、无左条、仅彩色浅底，与现有 aside 风一致）与标题/图标着色规则。
3. 同步更新本 skill 的 `references/design-tokens.md` 令牌表。
4. 校验（见下）。

## 校验布局是否生效

**不要对压缩后的大 CSS（`site_libs/bootstrap/*.min.css`，单行约 500KB）做宽模式全串扫描或打印全部命中**。用单次字面匹配 + 限定输出：

```powershell
# 例：确认主按钮绿/卡片圆角/深顶栏已进入产物
Get-ChildItem _book -Recurse -Include *.css | Select-String -SimpleMatch '#1f883d' | Measure-Object
Get-ChildItem _book -Recurse -Include *.css | Select-String -SimpleMatch '#fdfcfc' | Measure-Object
```

或用本 skill 的 `scripts/check_layout.py` 一键校验关键令牌与选择器。

## 改主题后样式不生效（SASS 缓存）

仅删 `.quarto` 可能不够，Quarto 的 SASS 编译缓存还落在全局目录 `$env:LOCALAPPDATA\quarto` 与 `~/.cache/quarto`。彻底清缓存见 `AGENTS.md`。
