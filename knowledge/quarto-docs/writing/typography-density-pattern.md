---
kb_id: "cpp-quarto-typography-density-v1"
title: "三栏宽度预算与正文排版密度的判定依据"
domain: "quarto-docs"
subdomain: "typography"
tags: [grid_width, gutter, code_block, border, text_wrap, density, paragraph_box_ratio, toc_wrap]
level_range: [0, 9]
dependencies: ["cpp-quarto-chapter-pattern-v1"]
created: "2026-09-10"
updated: "2026-09-12"
chunk_strategy: "semantic_heading"
estimated_tokens: 1500
---

# 三栏宽度预算与正文排版密度的判定依据

> 本文件记录「页面看着乱」这一类问题的可测量成因与阈值，是这块领域知识的唯一出处。
> 页面由哪些块组成、每块职责见标识 `cpp-quarto-chapter-pattern-v1` 的知识文件。
> 渲染取值见标识 `cpp-tooling-quarto-render-v2` 与 `cpp-tooling-quarto-html-v2` 的知识文件。
> 断言由 `.agents/skills/quarto-theme/scripts/check_typography.py` 在 1280 与 1100 两档视口执行。

## 三栏宽度预算

Quarto 的 `body-width` 是上限声明，不是保证值。grid 四项之和超过目标视口时，浏览器按比例压缩正文列，作者看到的却是自己写的数字，因此必须先做减法。

```text
sidebar + body + margin + 2 × gutter <= 目标视口
```

本项目取 1280 为主目标：`272 + 800 + 256 + 2 × 16 = 1360`，超出 80px，正文列落到 688px。这 80px 是有意的让步：`margin-width` 256px 是长中英混排标题在右侧目录不折行所需的最小宽度，缩侧栏会让左侧目录先出问题。

两侧还有一条不对称：页面容器有 `padding-left`，右侧没有补偿，正文实际可用宽度比 grid 算出的列宽又少 14–32px。所以判断「正文够不够宽」要用实测的段落 `clientWidth`，而不是 grid 声明值。阈值 640px（1280 档）与 540px（1100 档）对应每行约 40 个汉字，低于它换行数上升，扫读会退化成逐行读。

## 代码块外观只有一个控制点

`div.sourceCode` 与其中的 `pre.sourceCode` 若都声明边框、圆角和底色，页面就出现框中框：两层同色边框叠成一条灰线，圆角半径不同时还会露出内层方角。

规则是外观归外层容器，滚动归内层：

| 声明 | 归属 |
|---|---|
| `border`、`border-radius`、`background-color` | `div.sourceCode` |
| `padding`、`overflow` | `pre.sourceCode` |
| 字体、字号、行高 | 两者共用同一组 token |

没有 `div` 包裹的裸 `pre`（目录树、命令输出）自己承担边框，观感与语言代码块一致。这条分工必须由脚本断言，因为 Quarto 升级会改 DOM：包裹层一旦消失，`pre.sourceCode` 就同时命中两条规则。

## 换行语义会被同特异规则静默取消

`code-overflow: wrap` 由 Quarto 注入 `pre > code.sourceCode { white-space: pre-wrap }`，特异度 (0,1,1)。主题里任何一条同样形状的 `pre.sourceCode code { white-space: pre }` 与它同特异且加载更晚，于是横向滚动回来，作者却以为配置生效了。

结论是主题 CSS 不要重新声明 `white-space`，需要覆盖时取与 Quarto 一致的 `pre-wrap` 并补 `overflow-wrap: anywhere`，让超长命令行在窄栏里折行而不是撑出横向滚动条。这一条同样只有计算样式断言能守住。

## 段落与盒子比例

盒子指代码块、表格、提示框、引用块和图表容器。它们底色与边框一致、左右内缩相同，连续出现时读者分不清内容边界，只能靠滚动位置感知。

| 指标 | 阈值 | 含义 |
|---|---|---|
| 段 / 盒 | ≥ 2.4 | 每两个盒子之间至少有一段自己的话 |
| 单个 `##` 内盒子 | ≤ 2 | 一节的主线动作不超过两条 |
| 连续盒子 | ≤ 1 处 | 相邻盒子最多一处，其余被正文隔开 |

比值低于 2 时，页面从「读一段做一步」退化成「抄一屏」。修法是补承接正文，而不是删盒子：盒子承担可复制性，正文承担判断依据，两者不可互换。

## 命令、说明与输出的三分法

逐条示例命令带 `$ ` 提示符和行内注释时，一个 30 行的块里真正要敲的往往只有三行。提示符不能复制（粘进终端会报错），注释与命令同色同权重，读者必须自己做一次「哪几行有用」的筛选。

三类信息因此分归三个位置：命令进代码块，说明进正文段落，输出进紧随其后的 `text` 块。「哪一行是输出」由块边界表达，不再依赖 `# 预期输出` 这类注释约定，读者先决定要不要做，再看到怎么做。

位置的分配、提示符与注释写法、代码块语言选择等操作细则的唯一出处是 `.agents/skills/quarto-docs/references/quarto/terminal-validation.md`，本文件只保留成因。

## 目录折行与侧栏宽度

右侧目录条目折行是「锯齿」感的直接来源。三级条目的可用宽度等于 `margin-width` 减去竖线占位再减去每级缩进，缩进系数从整级降到半级，就能把三级文字宽度从 166px 抬回 226px。

第二条线索是标题本身。混合中英的长标题（如「接入 Windows Terminal 与 VS Code」）折行点不可控，缩短或拆分比调窄缩进更稳定。两条都不足以达标时，按计划把 `margin-width` 降回 224px 复测，而不是继续压 `--toc-indent`。

## 与自动化断言的分界

本文件只解释成因与阈值。数值断言全部在 `.agents/skills/quarto-theme/scripts/check_typography.py`，浏览器侧测量在同级 `measure_pages.mjs`。改标题、改缩进、改 grid 之后由 `run.py check` 判定，不靠人工目测长期维持。正文高度上限按当前两章实测值设置为 4300px 与 5100px，仅用于捕获后续异常增长。
