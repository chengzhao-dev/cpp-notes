---
kb_id: "cpp-tooling-quarto-render-v2"
title: "Quarto 渲染行为与失效模式"
domain: "quarto-docs"
subdomain: "rendering"
tags: [quarto, render, yaml, callout, include, encoding, troubleshooting, grid_width, reading_width, gutter, viewport_target, sidebar_width, margin_width, sidebar_collapse, collapse_level, text_wrap, code_block_border, code_title, filename, toc_indent, typography, line_height, font_stack, webfont_subset, fixel_text, lxgw_wenkai_screen, lxgw_bright_code, monaspace_argon, code_followup_gap, reference_sites, homepage_hero, marketing_layout]
level_range: [0, 9]
dependencies: ["cpp-tooling-build-chain-v2"]
created: "2026-09-09"
updated: "2026-09-19"
chunk_strategy: "semantic_heading"
estimated_tokens: 2500
---

# Quarto 渲染行为与失效模式

> 本文件是 Quarto 配置生效边界与页面几何行为的唯一出处。写作侧怎么做见 `quarto-docs` 的 reference，`_quarto.yml` 的现行取值见 `references/quarto/rendering-and-output.md`。

## 配置与产物

Book 默认输出 `_book/`，发布产物路径必须与项目类型匹配。YAML 层级、缩进或作用域错误可能不报错而静默失效。修改后应渲染并检查生成页面。

## 提示框与包含文件

Quarto 只识别内置提示框类型。自定义提示框类可能退化为普通章节。包含真实代码文件时使用带语言标记的代码围栏，否则代码中的 Markdown 字符会被当作正文解析。

## 三栏宽度预算

Quarto 的 `body-width` 是上限声明，不是保证值。`sidebar-width + body-width + margin-width + 2 × gutter-width` 超过目标视口时，浏览器按比例压缩正文列，作者在配置里看到的仍是自己写的数字，所以改栅格前先做减法。本项目当前三栏声明合计为 1360px（`272 + 800 + 256 + 32`），目标视口取 1440px：1366 及以上的机器零压缩，1536 与 1920 有富余。正文上限保持 800px，`margin-width` 取 256px，给右侧三级目录折行余量。

### 左右栏为什么取 272 与 256

左右栏宽度来自同类教程文档的实测值，而不是从正文宽度倒推。VitePress 系（vuejs.org）左栏 272px、右栏 256px、正文 688px、布局上限 1440px；react.dev 左右各 320px、正文上限 336px，但三栏要 1536px 才成立。取 VitePress 一侧的数值，是因为它同时满足两个约束：侧栏章节条目的可用文字宽度从 240px 时的 135px 提到 272px 时的 167px，十个章节标题的折行数从 6 个降到 2 个；而 272 + 256 把合计留在 1360px，1366 及以上的视口仍能把正文列顶满 800px 上限（实测段落宽 768px），只有 1280px 视口压到约 678px。

剩余折行标题说明加宽侧栏已不是主要手段。最长的两个条目「编译并运行第一个 C++ 程序」与「Android 手机影像中的 C++ 交付背景」在 272px 侧栏内都要折行，侧栏要放到约 334px 才能全部单行，而 334 + 256 把三栏合计推到 1428px，目标视口升到 1536px，1366 与 1440 的机器都要为最长的一条中英混排标题让出正文宽度。按「目录折行与缩进」一节的结论，这种情况改缩短标题而不是继续加宽：工程应用章因此由「Android 手机影像中的 C++ 交付背景」改为「影像算法的交付形态」，两个长 H2 同步压短成「开发期的可执行文件」「上线交付的动态库」。

屏幕分辨率分布支持这个取法：1920×1080 约占 22%–24%，1536×864 约占 10%–11%，1366×768 约占 7%–9%。也就是主流机器落在 1536 与 1920，1366 是仍需覆盖的下限，1440 附近（含 1280×800、1440×900 的缩放态）作为目标视口能覆盖绝大多数桌面读者。

页面容器只有 `padding-left`，右侧没有补偿，正文实际可用宽度比 grid 算出的列宽又少十几到三十像素。因此判断正文够不够宽要看实测的段落宽度，不看 grid 声明值。`body-width` 变大后，普通段落仍可能因为主题 CSS 的 `max-width: 75ch` 被二次收窄。正文规则应使用 `max-width: 100%`，让段落跟随实际列宽。只有每行低于约 40 个汉字时，换行数才会明显上升，扫读会退化成逐行读。

窄屏下侧栏会换成覆盖正文的浮层，那套布局另有约束，见标识 `cpp-quarto-sidebar-overlay-v1` 的知识文件。

## 侧栏分组为什么默认折叠

Book 的 sidebar 选项写在 `book:` 键下，不是 `website:`；Book 与 Website 共用同一套 sidebar 组件，因此 `website:` 文档里的 `collapse-level` 等选项同样适用。顶层 part 以 depth=1 渲染，`collapse-level` 的默认值 2 让 part 与其下章节全部展开：章节变多后左侧一次铺开全书目录，读者失去位置感。取 1 后分组默认折叠，只有当前页所在的 part 因构建期写入的 `expanded` 自动展开，与 Vue、React 文档「分组可折叠、当前路径可见」的处理一致。

折叠只改变初始展开状态，不改变产物结构：侧栏浮层断言与溢出扫描都不依赖展开状态，主题 CSS 也不重声明 Bootstrap 的 collapse 类。判断依据取 Quarto 模板而不是猜测，`projects/website/templates/sidebaritem.ejs` 用 `collapse <= depth && !item.expanded` 计算折叠。`_quarto.yml` 属于整本渲染的触发范围，改完必须重新渲染并实测。

## 字体与正文测量

正文的拉丁字符使用 Fixel Text 的 500/600/700，界面中文使用 `LXGW WenKai Screen`，代码使用 `LXGW Bright Code`。三者均为 SIL OFL 1.1，适合自托管的个人和商业项目。中文与代码字体各使用一个常用字符集 WOFF2，覆盖当前公开内容和一级常用汉字。每个包只有一个请求，单页最多请求 5 个字体文件，体积预算为 1.6 MB。Bright Code 的拉丁部分来自 Monaspace Argon，中文部分来自霞鹜文楷。代码栈保留 `LXGW WenKai Screen` 作为缺字回退，避免扩展区字符或下载失败时掉到系统衬线字体。

参考站点承担不同任务：Quarto 教程在 1280px 下正文约 616px，采用 17px / 1.5。GitHub Markdown 约 823px，采用 16px / 1.5。gitcn 的主内容区约 1024px，但说明文字会缩到约 672px。根首页的文字密度和卡片布局服务于快速浏览，不能直接当作连续正文的基准。教程正文保留 16px / 1.65，并把上限收至 800px，兼顾中文字形、代码宽度与连续阅读。

## 列表内代码块后的结果间距

Quarto 将每个 `##` 的内容包在 `section` 中，主题的直属子元素间距能覆盖顶层代码块与后续段落，却覆盖不到有序列表内部的 `li > p`。因此代码块后紧跟验证句时会退回浏览器默认间距，视觉上显得贴在代码框底部。主题用 `--code-followup-gap` 统一为列表项内的代码块与后续验证段提供 1rem 上距。顶层代码块的 1.375rem 间距保持不变，避免同一规则把正文节奏整体压缩。

## 目录折行与缩进

右侧目录条目折行是页面「锯齿」感的直接来源。三级条目的可用宽度等于 `margin-width` 减去竖线占位再减去每级缩进，缩进系数从整级降到半级能换回约六十像素文字宽度。第二条线索是标题本身：中英混排的长标题折行点不可控，缩短或拆分标题比继续压缩进更稳定。两条都不足以达标时，加大 `margin-width` 复测，代价是三栏合计上升、目标视口被推高，因此最后才动它，而不是继续压 `--toc-indent`。

## 换行语义会被同特异规则静默取消

`code-overflow: wrap` 由 Quarto 注入 `pre > code.sourceCode { white-space: pre-wrap }`。主题里任何一条形状相同、特异度相同且加载更晚的 `pre.sourceCode code { white-space: pre }` 会把它取消，横向滚动回来，作者却以为配置生效了。结论是主题 CSS 不重新声明 `white-space`，需要覆盖时取与 Quarto 一致的 `pre-wrap` 并补 `overflow-wrap: anywhere`，让超长命令行在窄栏折行。这一条只有计算样式断言能守住。

## 代码块外观只有一个控制点

`div.sourceCode` 与其中的 `pre.sourceCode` 若都声明边框、圆角和底色，页面出现框中框：两层同色边框叠成一条灰线，圆角半径不同时还会露出内层方角。分工是外观（`border`、`border-radius`、`background-color`）归外层容器，`padding` 与 `overflow` 归内层，字体、字号、行高两者共用同一组令牌。没有 `div` 包裹的裸 `pre`（目录树、命令输出）自己承担边框，观感与语言代码块一致。这条分工由 `check_dom_contracts.py` 断言，因为 Quarto 升级会改 DOM：包裹层一旦消失，`pre.sourceCode` 就同时命中两条规则。

## 代码来源标题的职责

代码高亮只说明语法，说明不了这段内容应该在哪个终端运行，也说明不了它是不是仓库中的真实文件。Quarto 的 `filename` 属性在代码块上方生成独立标题条，用 `PowerShell（管理员）`、`Ubuntu Bash（工程根目录）` 标明运行环境，用 `main.cpp`、`CMakeLists.txt`、`build-and-run.sh` 标明真实文件，用 `输出` 区分执行结果。这样读者不必从正文反推代码来源，正文也能只说明当前动作和成功判据，不用反复写“下面是一段 Bash 代码”。

标题条与代码体必须共享外框并取消相接处的圆角，否则会出现双线或断角。复制按钮固定在右上角时，标题区要预留宽度，避免长文件名被遮挡。标题只是来源标签，不是操作步骤，因此不能替代正文中的执行位置、命令目的和安全边界。该结构由 `check_docs.py` 检查属性围栏，由 `check_dom_contracts.py` 检查渲染产物。

## 编码与路径

中文文件使用 UTF-8 无 BOM 与 LF。路径或文件名含非 ASCII 特殊字符时，Windows 工具链可能在编码或索引阶段失败。仓库路径名保持 ASCII。
