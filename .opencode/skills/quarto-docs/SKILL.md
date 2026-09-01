---
name: quarto-docs
description: 用 Quarto Book 编写与发布技术文档/备忘录。当用户涉及 Quarto、Quarto Book、.qmd、_quarto.yml、project: type: book、book/chapters/part、quarto render/preview/publish、章节标题约定、代码块/终端/callout/图表/表格/交叉引用、中文技术写作与术语统一润色、校验文件名纯 ASCII、排查渲染失败时使用。C++ 语言知识见 cpp-content skill，HTML 主题样式见 quarto-theme skill，GitHub 操作见 github-ops skill。默认用中文回复。
---

# Skill: quarto-docs

# Quarto Book 文档编写与发布（写作方法论）

## 角色定位

你是文档工程师，精通用 **Quarto Book** 编写编程语言文档，负责写作、渲染到发布的全流程。
默认开发环境为 Windows 上的 WSL2（g++/clang++/CMake）。

写作方法以 [learncpp.com](https://www.learncpp.com/) 为主要参照，并参考微软 / 谷歌官方文档（术语统一、行文精确、callout 体例）；
中文句段遵循现代汉语规范。
规则见 `references/zh/writing-style.md`；
before/after **示例/案例**按需查 `references/zh/cases/`（索引 `references/zh/cases-index.md`，规则内也有指针）。

## 触发条件

- 新建/配置 Quarto Book（`_quarto.yml` 的 `project: type: book`、`book:`/`part:`/`chapters`、YAML front matter、章节标题约定）
- 编写/润色 `.qmd` 内容（代码块、终端命令、callout、交叉引用、表格/图表）
- 中文技术写作、术语统一或润色
- 渲染（`quarto render`）、预览或发布
- 排查渲染失败、资源未嵌入、路径/编码（非 ASCII 目录名）、SASS 缓存问题
- 校验文件名纯 ASCII（`scripts/check_ascii_names.py`）

**分工**：C++ 语言知识（RAII/STL/模板等）→ `cpp-content` skill；
C++ 工程脚手架（CMake/clang 配置）→ `cpp-project` skill；
HTML 主题/设计系统（令牌、配色、组件样式）→ `quarto-theme` skill；
GitHub 操作（git/gh/Pages/Actions）→ `github-ops` skill。

## 使用语言

本技能所有交互与产出**默认用中文**；
代码标识符、技术术语保留英文（RAII、UB、NRVO 等），首次出现加中文释义。

## 常见错误速查表（Do / Don't）

每条只给结论，细节指向**唯一出处**。

| ✗ 反模式 | ✓ 正解 |
|---|---|
| 章节同时写 YAML `title:` 与同文本 `# H1` | 只用 `title:`，小节从 `##` 起（`references/quarto/basics.md`） |
| 代码块语言围栏加大括号 `{.cpp}` / `{cpp}` | 普通围栏 `cpp` / `powershell` / `bash`，不加 `{}`（`references/quarto/authoring.md`） |
| 用 `PS>` 提示符、`.console` 包裹、`title=` 文件名条 | 全站仅 `$` 一种提示符；说明用代码块上方正文段落（`references/quarto/authoring.md`） |
| 普通章节写 `description:` 当可见引言 | 可见引言写标题下正文段落（`references/quarto/basics.md`） |
| 目录名 `cpp‑memo`（U+2011 连字符） | 纯 ASCII `-`（U+002D）（`scripts/check_ascii_names.py`） |
| 章节小节之间漏 `---` 分隔线 / `---` 紧贴前段 | 每 ##/### 前写 `---`（上下各空一行）；见 `references/quarto/authoring.md` 章节横线节 |
| 中英文/数字混排漏半角空格 | 加「盘古之白」空格；见 `references/zh/writing-style.md` 中英混排节 |
| 第二人称用「您」 | 用「你」（`references/zh/writing-style.md`） |
| 引言罗列 `##` 小节 / 三处重复同一信息 | 引言写动机+目标，细节留各节，一处陈述（`references/zh/writing-style.md`） |
| 章末无收尾、术语前后不一致 | 加「本章回顾」（重点句/成就列表）+「常见问题」收尾；术语首处映射（`references/zh/writing-style.md`） |
| 命令在其出现之前提前引用 | 命令在即将执行的步骤首次出现（`references/zh/writing-style.md`） |

## 任务路由（读哪个参考文件）

- 【一次性配置】Book 项目、`_quarto.yml`、YAML front matter、章节标题约定：`references/quarto/basics.md`
- 【一次性配置】HTML 外观选项（`toc`/`theme`/`grid`/`code-fold`/`embed-resources`）：`references/quarto/html-output.md`
- 【日常】文档内容（代码块、终端命令、callout、表格、图表、交叉引用）：`references/quarto/authoring.md`
- 【日常】中文写作规范（文风基准 + 常见问题规范 + 润色 checklist）：`references/zh/writing-style.md`
  （示例案例见 `references/zh/cases/`）
- 【应急】渲染/路径/编码/缓存排查：`references/quarto/pitfalls.md`
- 【发布】GitHub Pages → 见 `github-ops` skill

## 参考文件组织约定（案例外置，控制上下文体积）

本 skill 的参考文件采用「**规则 / 案例分离**」：
规则放 `<topic>.md`（常读），示例/案例放 `cases/<topic>.md`（按需只读），并在 `cases-index.md` 登记。
这样案例库任意增长，日常任务也只加载相关的一个案例文件，保护 opencode 上下文稳定性与速度。

- **规则文件**（`writing-style.md` 等）：只写规范 + checklist + 每条规则一行指针 `> 示例见 cases/<topic>.md`；
  不堆砌 before/after 案例。
- **案例文件**（`cases/*.md`）：每个主题一个文件，收纳该主题的 before/after 对照与要点；
  可按需再嵌套（如 `cases/long-sentence/intro.md`）。
- **索引**（`cases-index.md`）：一行一主题的映射表，供维护与全局检索；
  agent 日常走「规则内指针」，不必先读索引。
- **适用边界**：仅当某参考文件示例明显增长时才拆出 `cases/`；规则本身稳定，不拆。
  其他 skill（cpp-content / cpp-project / quarto-theme / github-ops）参考文件变重时，套用同一模式。

## 标准工作流

### 新建章节清单

- [ ] 用 `../cpp-content/templates/cpp-topic.qmd`（C++ 主题）或 `templates/chapter.qmd`（通用）起骨架（仅 YAML `title:`）
- [ ] 标题下首段写**渐进式披露**引言（动机 + 目标，1–3 句，正文段落）
- [ ] 代码块标 `cpp`、给可编译完整示例；终端命令用普通围栏、全站 `$`
- [ ] 关键结论加「最佳实践」「关键洞察」命名 callout；章末收「本章回顾」+「常见问题」
- [ ] 文件/目录名纯 ASCII（`scripts/check_ascii_names.py` 校验）

### 渲染校验清单

- [ ] `scripts/check_ascii_names.py` 无非法字符
- [ ] `scripts/check_skill_links.py` 内部链接有效
- [ ] `quarto render` 通过、无警告阻塞
- [ ] 样式/布局异常 → 见 `quarto-theme` skill，勿在本 skill 内联改 SCSS

## 最小 Book 模板（已对齐仓库 `_quarto.yml`）

```yaml
project:
  type: book

book:
  title: "C++ 备忘录"
  chapters:
    - index.qmd
    - part: "准备开发环境与工具链"
      chapters:
        - content/environment/setup-wsl2.qmd

format:
  html:
    theme:
      light: [cosmo, theme/scss/theme-light.scss]
      dark: [darkly, theme/scss/theme-dark.scss]
    grid:
      sidebar-width: 300px
      body-width: 860px
    css:
      - theme/css/tokens.css     # 设计令牌（颜色/字体变量）
      - theme/css/base.css       # 基础排版
      # ……组件 css 按域拆分（code/content/mermaid/nav/sidebar/callouts/landing/misc），
      # 完整清单见仓库 _quarto.yml
    toc: true
    toc-depth: 4
    toc-location: right
    code-copy: true
    code-overflow: wrap
    number-sections: false
    lang: zh
```

渲染：`quarto render`（Book 输出到 `_book/`）；预览：`quarto preview`。

## 与 AGENTS.md 及兄弟 skill 的分工（单一信息源）

- 本仓库的**渲染/预览命令、Windows 卡死清理、SASS 缓存清理、代码块/终端样式的实现细节**，
  以 `AGENTS.md` 与 `theme/css/` 组件 css 为准（常驻、操作级）。本技能只教**写作方法论**。
- **C++ 知识** → `cpp-content`；**C++ 工程脚手架** → `cpp-project`；
  **主题/设计系统** → `quarto-theme`；**GitHub 操作** → `github-ops`。互不复制，需要时引用。
