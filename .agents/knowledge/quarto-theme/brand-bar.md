---
kb_id: "quarto-theme-brand-bar-v1"
title: "顶部品牌区的视觉一致性"
domain: "quarto-theme"
subdomain: "navigation"
tags: [navbar, brand, svg, baseline, responsive, dark_mode, contrast]
level_range: [0, 9]
dependencies: []
created: "2026-09-16"
updated: "2026-09-16"
chunk_strategy: "semantic_heading"
estimated_tokens: 360
---

# 顶部品牌区的视觉一致性

## 对齐与比例

顶栏图文按“墨迹”而不是按元素盒对齐。标题用 1.125rem 加粗，汉字字面高度实测 17px；图标元素取 1.5rem，经 `mask` 后墨迹为 18px，约为字面高度的 1.06 倍，视觉重量与标题相当。行高会把 CJK 字形的墨迹中心抬到行框中心之上约 0.17rem，flex 居中只对齐元素盒，图标看上去就比标题低，因此需要额外的下外边距把图标抬回同一视觉基线，让墨迹底边落在标题基线上。

图标用 `--navbar-fg` 上色，与 `--navbar-bg` 的对比度在明暗两态分别为 15.8:1 和 16.0:1，远高于正文 4.5:1 的门槛。若改成直接引用彩色徽标图片，SVG 图片内部的 `prefers-color-scheme` 由运行环境决定，系统偏好与站点主题不一致时会出现徽标与顶栏同底色的反转，因此单色遮罩更稳。浅色令牌同时声明 `color-scheme: light`，避免系统深色偏好渗入原生控件与内嵌资源。

## 窄屏退化

视口变窄时先压缩搜索框，再省略标题，最后缩小图标；主题切换、搜索和侧栏按钮必须保持独立点击区域，不能互相覆盖。桌面、平板、手机和小屏手机都应检查品牌栏高度与焦点轮廓。
