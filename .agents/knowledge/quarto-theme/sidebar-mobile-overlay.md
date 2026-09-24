---
kb_id: "cpp-quarto-sidebar-overlay-v1"
title: "窄屏左侧栏浮层的可读性"
domain: "quarto-theme"
subdomain: "layout"
tags: [sidebar, mobile, overlay, transparency, scrim, backdrop_filter, breakpoint, z_index, android, readability]
level_range: [0, 9]
dependencies: ["cpp-tooling-quarto-render-v2", "quarto-theme-brand-bar-v1"]
created: "2026-09-19"
updated: "2026-09-19"
chunk_strategy: "semantic_heading"
estimated_tokens: 600
---

# 窄屏左侧栏浮层的可读性

## 为什么窄屏侧栏会「透字」

桌面端左侧栏是常驻栏，与正文同处一个网格列，背景透明时露出的是页面底色，观感上等于与页面融为一体。≤991.98px 时布局换行为单列，Quarto 通过 `.collapse-horizontal` 把 `#quarto-sidebar` 变成覆盖正文的浮层，同一断点下 `#quarto-sidebar-glass` 从 `display: none` 变为覆盖整个视口的灰遮罩（`#66666666`，约 40%）。侧栏的 `z-index` 高于遮罩，所以浮层之下是「遮罩 + 被压暗的正文」。

浮层沿用透明底色时，读者看到的是三层叠加：正文笔画透过侧栏文字，遮罩再把两者一起压暗。这就是移动端浏览器上「字体背景太模糊、同时能看见下面正文」的成因，也解释了为什么同一份内容在桌面端没有这个问题——桌面端透明底露出的是干净的页面底色。Android 上侧栏展开后占满下方界面，透字面积最大，因此观感最差。

### 同一个底色值为什么能覆盖两种状态

桌面端透明底露出的本来就是页面底色，所以浮层改用页面底色令牌后，桌面观感不变、窄屏不再透字，一个值覆盖两种状态，也不必为浮层新增令牌。真正需要按断点限定的是分隔线而不是底色：桌面端侧栏右侧不加竖线，只有浮层压在正文上时才需要一条发丝线把它与身后的遮罩分开。

次级导航那种「半透明 + `backdrop-filter: blur()`」不适合浮层：模糊本身就是本次要消除的观感，而浮层需要的是能被断言的不透明值。仅靠调高遮罩不透明度也不行，正文仍会从侧栏内部透出。

## 验收为什么断言计算样式而不是截图

断点由视口宽度触发，与元素是否可见无关。因此侧栏处于收起状态（`.collapse` 无 `.show`）时，`getComputedStyle` 仍返回浮层分支的底色，alpha 可以离线断言。截图做不到这一点：它受字体加载、展开动画时序和遮罩叠加影响，同一个缺陷在不同机器上表现强弱不一，而断言只在「侧栏又回到透底状态」时才失败。

断言放在视口 ≤991.98px 的分支，与 Quarto 自身切换浮层的断点一致；用更大的断点会把桌面端的透明底误判为失败。
