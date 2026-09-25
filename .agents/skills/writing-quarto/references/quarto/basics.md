# Quarto 基础（Book 项目）

本文件是 Quarto Book 项目结构、YAML front matter、章节标题约定的**规范唯一出处**。其他文件（authoring.md、rendering-and-output.md）提到这些约定时一律引用本文件，不重复陈述。`format: html` 的选项语义与失效边界归 `.agents/knowledge/quarto-writing/output/html-output.md`，本项目现行取值归 `rendering-and-output.md`，本文件不复制。

> 速查：`.qmd` = YAML front matter + Markdown 正文 · `title:` 与 `# H1` 二选一 · `index.qmd` 必须存在 · Book 输出 `_book/` · `part:` 分组章节

## 目录

- [.qmd 文档结构](#qmd-文档结构)
- [章节 front matter 字段](#章节-front-matter-字段)
- [章节标题](#章节标题)
- [Quarto Book 项目配置与格式](#quarto-book-项目配置与格式)
- [章节标题约定（唯一信息源）](#章节标题约定唯一信息源)
- [第一个小节](#第一个小节)
- [目录结构](#目录结构)
- [其他](#其他)

## .qmd 文档结构

一个 `.qmd` 文件由两部分组成：

```yaml
---
title: "文档标题"
author: "作者"
date: today
format: html
---

正文内容。
```

- **YAML front matter**：文档元数据与配置，位于文件顶部 `---` 之间。
- **Markdown 正文**：标准 Markdown + Quarto 扩展（divs、spans、callout、交叉引用等）。

## 常用 front matter 字段

| 字段 | 作用 |
|---|---|
| `title` / `subtitle` | 标题 / 副标题 |
| `description` | **只有根 `index.qmd` 会渲染成页面可见副标题**（产物里的 `<div class="description">`）。part 封面写该字段只产出 `<meta name="description">` 供搜索引擎使用，页面上不显示，因此分组引导句必须写成 `##` 下的正文段落。普通章节不写该字段 |
| `author` / `date` | 作者 / 日期（`today` 自动取当天） |
| `format` | 输出格式（`html`/`pdf`/`revealjs`），可写对象形式配置子选项 |
| `lang` | 语言，如 `zh`（影响部分 HTML 行为与 PDF） |
| `bibliography` / `csl` | 参考文献库 / 引用样式 |
| `toc` | 目录（常放在 `format: html` 下，见 `rendering-and-output.md`） |

## 常用命令

```bash
quarto render 文档.qmd            # 渲染单个文档
quarto render 文档.qmd --to html  # 指定输出格式
quarto preview 文档.qmd           # 本地预览（实时刷新）
quarto render                     # 渲染当前项目全部内容
quarto publish gh-pages           # 渲染并发布到 GitHub Pages
```

## Quarto Book 项目（本项目所用格式）

本项目使用 **Quarto Book**（`project: type: book`），适合章节化技术文档。核心配置（**已对齐仓库 `_quarto.yml`**，不要与真实配置冲突）：

```yaml
project:
  type: book

book:
  title: "C++ 学习轨迹笔记"
  chapters:
    - index.qmd
    - part: "准备开发环境与工具链"
      chapters:
        - content/getting-started/setup-wsl2.qmd

format:
  html:
    theme:
      light: [cosmo, .agents/skills/designing-theme/assets/theme/palettes/github/theme-light.scss]
      dark: [darkly, .agents/skills/designing-theme/assets/theme/palettes/github/theme-dark.scss]
    # format: html 的其余取值（grid/css/toc/code-*/lang）以 _quarto.yml 与
    # references/quarto/rendering-and-output.md 的现行取值表为准，本文件不复制
```

- `book:` 下的 `title`、`author`、`date` 为书目信息，`chapters` 定义章节顺序。
- **`index.qmd` 必须存在**，作为 Book 首页/入口。
- 章节可放子目录（如 `content/getting-started/setup-wsl2.qmd`），在 `chapters` 写相对路径。
- **`part:` 分组**：可用标题字符串（`part: "标题"`）或指向索引页（如 `part: content/getting-started/index.qmd`，本项目在用），产生分卷/分部标题。索引页的 `.hero-eyebrow` 是可选视觉组件，只在正文真的写了该 div 时生效，与 `part:` 的写法无关，不构成索引页的硬性要求。
- 章节间交叉引用用 `@sec-...`、`@tbl-...`、`@fig-...`。
- 渲染：`quarto render`，Book **默认输出到 `_book/`**（区别于 website 的 `_site/`）。

### 根首页与部分首页的链接边界

根首页和部分首页分别完成一次选择，不能越过对方直接承担章节导航。

- 根 `index.qmd` 只展示 `content/<part>/` 这一层的内容部分，每张卡说明该部分解决什么问题，并链接到对应的 `content/<part>/index.qmd`。
- `content/<part>/index.qmd` 只展示本部分已经发布的正文页面，不含自己。它负责说明阅读顺序，不复制正文中的命令、参数或操作步骤。
- 新增部分时先写部分首页，再在根首页增加部分卡。根首页不得直接链接部分内的正文页面，否则部分首页会被绕过，两层导航也会重复。

## 章节标题约定（规范，唯一出处）

章节标题**二选一**：用 YAML `title:` **或**顶层 `# H1`，二者皆有时同文本必然重复渲染（YAML 标题进标题栏 `<header>`，`# H1` 另成一级章节），并造成**章节编号/结构错乱**。

推荐写法——用 `title:`，**不要**再写同文本 `# H1`，小节从 `##`（H2）开始：

```markdown
---
title: "章节标题"
---

开篇可见引导语写正文普通段落（动机 + 读者读完能做什么，1–3 句），普通章节不要写 `description:`；只有 index.qmd（封面页）的 description 会显示为标题下的引导段落。

## 第一个小节
正文。
```

- 侧边栏 / TOC / 面包屑 / 章节号均取自 `title:`。
- 首页 `index.qmd` 同理：去掉重复 `# H1`，其 `description:` **会**显示为可见引导段。
- 普通章节若需可见开篇说明，**在正文顶部写普通段落**（`description:` 在此只进 `<meta>`）。
- 页面内不得再出现顶层 `# H1`（它会被当作又一个编号章节，重复且错位）。
- **标题层级（H2/H3）**：`##` 表示阅读阶段、范围或一个可验收任务，`###` 表示该阶段中可独立完成或观察的子任务。正文最多到 `###`，禁止 `####` 及更深标题。
- `###` 只用于源码阅读、验证、可选分支、排错症状等拥有独立动作或观察结果的内容。只有一两句话的解释并入相邻段落，不为目录对称强行拆分。
- 同一阶段包含多个可独立验收的任务时，用 `##` 统摄，把各任务写成 `###`。简单的单任务章节可以只有 `##`，这比补一个空壳 `###` 更清楚。
- 根首页、部分首页的卡片标题可以保留 `###`，那是导航组件的视觉层级，不改变正文最多三级的约束。
- 归并或改名标题前先检索 `@sec-` 与 `#anchor`，避免破坏交叉引用。

## 输出结构

单个文档 `report.qmd` 渲染后：

```
report.qmd
report.html          # 输出 HTML
report_files/        # 依赖资源（图片、CSS、JS）
```

如希望单一自包含 HTML（无外部依赖），用 `embed-resources: true`，见 `rendering-and-output.md`。

## 延伸

- 正文结构、代码块/终端约定与文档元素：`authoring.md`
- 外观配置（toc/theme/grid/code-fold）：`rendering-and-output.md`
- 发布 GitHub Pages：见 `shipping-github` skill
- 渲染/路径/编码坑：本目录 `rendering-and-output.md`（编号索引）
- 本仓库渲染/预览/缓存等操作细节：**以 `AGENTS.md` 与 `.agents/skills/designing-theme/assets/theme/css/` 组件 css 为准**（见 SKILL.md 分工说明），本文件不重复承载。
