# Quarto 基础（Book 项目）

本文件是 Quarto Book 项目结构、YAML front matter、章节标题约定的**规范唯一出处**。其他文件（authoring.md、rendering-and-output.md）提到这些约定时一律引用本文件，不重复陈述。`format: html` 的取值只在 `knowledge/quarto-docs/output/html-output.md` 列一份，本文件不复制，避免两处随修订漂移。

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
| `description` | **只有根 `index.qmd` 会渲染成页面可见副标题**（产物里的 `<div class="description">`）。part 封面写该字段只产出 `<meta name="description">` 供搜索引擎使用，页面上不显示，因此分组引导句必须写成 `##` 下的正文段落；普通章节不写该字段 |
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

## Quarto Book 项目（本书所用格式）

本备忘录使用 **Quarto Book**（`project: type: book`），适合章节化技术文档。核心配置（**已对齐仓库 `_quarto.yml`**，不要与真实配置冲突）：

```yaml
project:
  type: book

book:
  title: "cpp-notes"
  chapters:
    - index.qmd
    - part: "准备开发环境与工具链"
      chapters:
        - content/getting-started/setup-wsl2.qmd

format:
  html:
    theme:
      light: [cosmo, .cursor/skills/quarto-theme/assets/theme/scss/theme-light.scss]
      dark: [darkly, .cursor/skills/quarto-theme/assets/theme/scss/theme-dark.scss]
    # format: html 的其余取值（grid/css/toc/code-*/lang）以 _quarto.yml 与
    # references/quarto/rendering-and-output.md 的现行取值表为准，本文件不复制
```

- `book:` 下的 `title`、`author`、`date` 为书目信息；`chapters` 定义章节顺序。
- **`index.qmd` 必须存在**，作为 Book 首页/入口。
- 章节可放子目录（如 `content/getting-started/setup-wsl2.qmd`），在 `chapters` 写相对路径。
- **`part:` 分组**：可用标题字符串（`part: "标题"`）或指向索引页（如 `part: content/getting-started/index.qmd`，本书在用），产生分卷/分部标题。索引页的 `.hero-eyebrow` 是可选视觉组件，只在正文真的写了该 div 时生效，与 `part:` 的写法无关，不构成索引页的硬性要求。
- 章节间交叉引用用 `@sec-...`、`@tbl-...`、`@fig-...`。
- 渲染：`quarto render`，Book **默认输出到 `_book/`**（区别于 website 的 `_site/`）。

## 章节标题约定（规范，唯一出处）

章节标题**二选一**：用 YAML `title:` **或**顶层 `# H1`，二者皆有时同文本必然重复渲染（YAML 标题进标题栏 `<header>`，`# H1` 另成一级章节），并造成**章节编号/结构错乱**。

推荐写法——用 `title:`，**不要**再写同文本 `# H1`；小节从 `##`（H2）开始：

```markdown
---
title: "章节标题"
---

开篇可见引导语写正文普通段落（动机 + 读者读完能做什么，1–3 句），普通章节不要写 `description:`；只有 index.qmd（封面页）的 description 会显示为标题下的引导段落。

## 第一个小节
正文。
```

- 侧边栏 / TOC / 面包屑 / 章节号均取自 `title:`。
- 首页 `index.qmd` 同理：去掉重复 `# H1`；其 `description:` **会**显示为可见引导段。
- 普通章节若需可见开篇说明，**在正文顶部写普通段落**（`description:` 在此只进 `<meta>`）。
- 页面内不得再出现顶层 `# H1`（它会被当作又一个编号章节，重复且错位）。
- **标题层级归并（H2 伞 + H3 子）**：多个内容高度相关、同属一个大阶段的同级 `##` 小节，
  应归并为一个 `##` 伞标题，各块降为 `###` 子标题，避免平铺过多同级 H2 造成结构破碎。
  示例：章首用一段正文引言交代动机和读者收益，路线图紧跟其后；
  其后 `## 准备与安装` 下挂 `### 先决条件`、`### 安装 WSL2`（内含基本验证与常见问题 callout）、`### 启动与关闭`。
  归并前先 grep 确认无 `@sec-` / `#anchor` 交叉引用这些标题，以免断链。

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
- 发布 GitHub Pages：见 `github-ops` skill
- 渲染/路径/编码坑：本目录 `rendering-and-output.md`（编号索引）
- 本仓库渲染/预览/缓存等操作细节：**以 `AGENTS.md` 与 `.cursor/skills/quarto-theme/assets/theme/css/` 组件 css 为准**（见 SKILL.md 分工说明），本文件不重复承载。
