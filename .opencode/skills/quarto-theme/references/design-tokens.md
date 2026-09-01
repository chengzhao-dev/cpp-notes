# 设计令牌（opencode 暖灰，结构沿用 Primer 值域）

本文件是本仓库明暗双主题的**令牌唯一出处**。设计基准：opencode 暖灰（色温对齐 opencode.ai/docs，结构沿用 GitHub Primer 值域）：亮色为暖纸白 hsl(0,20%,99%)、暗色为暖黑 hsl(0,9%,7%)。实际生效位置在仓库的 `theme/css/tokens.css`（`body` 与 `body.quarto-dark` 的 CSS 变量块）；本文件是它的规范来源，二者保持同步。

## 令牌对照表

| 语义 | CSS 变量 | 亮色（opencode 暖灰） | 暗色（opencode 暖黑） |
|---|---|---|---|
| 页面底色 | `--page-bg` | `#fdfcfc` | `#131010` |
| 正文 | `--body-color` | `#201d1d` | `#e8e6e3` |
| 次要文字 | `--text-secondary` | `#5c5858` | `#a7a29a` |
| 链接/强调（UI） | `--link-color` / `--accent` | `#0969da` | `#4da3ff` |
| 正文链接（近黑） | `--text-link` | `#201d1d`（= 正文色） | `#e8e6e3`（= 正文色） |
| 链接下划线（UI） | `--link-underline` | `rgba(9,105,218,.4)` | `rgba(77,163,255,.5)` |
| 正文链接下划线 | `--text-underline` | `rgba(32,29,29,.4)` | `rgba(232,230,227,.45)` |
| 代码底 | `--code-bg` | `#f8f7f7` | `#1b1818` |
| 代码边框 | `--code-border` | `#d9d8d8` | `#3c3a3a` |
| 表格/卡片边框 | `--table-border` / `--card-border` | `#d9d8d8` | `#3c3a3a` |
| 表格行底线（更淡） | `--table-hairline` | `#eceaea` | `#242121` |
| 主按钮底 | `--btn-primary-bg` | `#1f883d` | `#238636` |
| 主按钮 hover | `--btn-primary-hover-bg` | `#1c8139` | `#29903b` |
| 主按钮文字 | `--btn-primary-fg` | `#ffffff` | `#ffffff` |
| 强调绿点 | `--dot-green` | `#2da44e` | `#3fb950` |
| 顶栏底（同页面底色） | `--navbar-bg` | `#fdfcfc` | `#131010` |
| 顶栏文字 | `--navbar-fg` | `#201d1d` | `#e8e6e3` |
| 顶栏次要文字 | `--navbar-muted` | `#5c5858` | `#a7a29a` |
| 顶栏边框（发丝线） | `--navbar-border` | `#d9d8d8` | `#3c3a3a` |
| 次级导航底（毛玻璃） | `--navbar-secondary-bg` | `rgba(253,252,252,.72)` | `rgba(19,16,16,.72)` |
| 顶栏搜索框底 | `--navbar-input-bg` | `#f8f7f7` | `#1b1818` |

## 主按钮（绿底白字）使用规范

绿色底 + 白字**仅用于「页面唯一主操作」按钮**（对齐 gitcn.org / GitHub Primer：Merge pull request、Confirm merge、Copy Exercise、「前往 GitHub 实操练习」均为此类），一个页面最多一个；链接、导航、次要操作一律不用绿底。完整状态（亮色）：

| 状态 | 值 |
|---|---|
| rest | 底 `#1f883d` / 白字 / 边框 `rgba(31,35,40,.15)` / 阴影 `0 1px 0 rgba(31,35,40,.1)` / 高 32px / 圆角 6px |
| hover | 底 `#1a7f37` |
| active | 底 `hsla(137,66%,28%,1)` + inset 阴影 `inset 0 1px 0 rgba(0,45,17,.2)` |
| focus | 2px 蓝环 `#0969da`（`--accent`），outline-offset -2px |
| disabled | 底 `#94d3a2` + 80% 白字 |

暗色：rest `#238636`、hover `#29903b`，其余状态同亮色。当前首页 hero 不用独立绿按钮，CTA 统一为卡片内蓝链 `.landing-card a.cta`。

## callout 色（Primer 语义色）

| callout | 亮色 border | 暗色 border |
|---|---|---|
| note | `#0969da` | `#58a6ff` |
| tip | `#1a7f37` | `#3fb950` |
| warning | `#9a6700` | `#d29922` |
| important | `#8250df` | `#a371f7` |
| caution | `#d1242f` | `#f85149` |
| best-practice（最佳实践，绿） | `#1a7f37` | `#3fb950` |
| key-insight（关键洞察，金） | `#b08800` | `#e3b341` |

## drop-in 片段（`theme/css/tokens.css` 顶部变量块）

亮色：

```css
body {
  --body-color: #201d1d;
  --code-bg: #f8f7f7;
  --code-border: #d9d8d8;
  --link-color: #0969da;                 /* UI 强调色（CTA / 复制按钮 / focus ring）保留蓝 */
  --text-link: var(--body-color);       /* 正文链接近黑（opencode 风） */
  --text-underline: rgba(32,29,29,.4);  /* 正文链接常驻下划线 */
  --text-secondary: #5c5858;
  --table-hairline: #eceaea;            /* 表格行底线（比表头线更淡） */
  --btn-primary-bg: #1f883d;
  --btn-primary-hover-bg: #1c8139;
  --btn-primary-fg: #ffffff;
  --dot-green: #2da44e;
  --navbar-bg: #fdfcfc;
  --navbar-fg: #201d1d;
  --navbar-muted: #5c5858;
  --navbar-border: #d9d8d8;
}
```

暗色：

```css
body.quarto-dark {
  --body-color: #e8e6e3;
  --code-bg: #1b1818;
  --code-border: #3c3a3a;
  --link-color: #4da3ff;
  --text-link: var(--body-color);
  --text-underline: rgba(232,230,227,.45);
  --text-secondary: #a7a29a;
  --table-hairline: #242121;
  --btn-primary-bg: #238636;
  --btn-primary-hover-bg: #29903b;
  --btn-primary-fg: #ffffff;
  --dot-green: #3fb950;
  --navbar-bg: #131010;
  --navbar-fg: #e8e6e3;
  --navbar-muted: #a7a29a;
  --navbar-border: #3c3a3a;
}
```

## 设计来源

- 亮色：opencode 暖纸白（`hsl(0,20%,99%)` ≈ `#fdfcfc`），结构值域沿用 GitHub Primer v2（`--fgColor-default` 等），参考 gitcn.org。
- 暗色：opencode 暖黑（`hsl(0,9%,7%)` ≈ `#131010`），结构值域对应 Dark Reader 默认调色板（`#e8e6e3` 文字、`#4da3ff` 链接），**非** Primer 原生暗色（`#0d1117`/`#f0f6fc`）。
