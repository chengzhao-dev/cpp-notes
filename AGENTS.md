# AGENTS.md

本仓库是 Quarto Book 项目（C++ 备忘录）。

- 写作规范 → `.opencode/skills/quarto-docs/`
- C++ 知识 / 代码风格 → `cpp-content`
- C++ 项目脚手架 → `cpp-project`
- 主题样式 → `quarto-theme`
- GitHub 操作 → `github-ops`

## 常用命令

```bash
quarto render             # 渲染整本 Book → _book/（产物可直接打开，零服务器延迟，最省事）
quarto preview            # 本地实时预览（Windows 上可能卡死/首屏转圈，见下）
quarto publish gh-pages   # 渲染并发布到 GitHub Pages
```

## 运行 Python 脚本（解释器解析协议）

- 仓库的 agent 工具脚本已全部为 Python（`.py`），**仅用标准库**，要求 Python ≥ 3.9。
- 调用任何脚本前，按以下优先级解析解释器；结果持久化，**一次指定后无需重复指定**：

  1. `scripts/python.json` 的 `python` 字段（指定，最高优先）
  2. 环境变量 `CPP_MEMO_PYTHON`
  3. 验证式自动搜索：逐候选实际执行 `<py> --version`，非零退出码即跳过（可排除 Windows 商店占位 stub）；
     顺序：PATH 上的 `python` / `python3` → 常见安装目录（miniforge3、anaconda3、
     `%LOCALAPPDATA%\Programs\Python\Python3*`、`C:\Python3*`）

- 自动搜索**命中后把该路径写入 `scripts/python.json`**（本机文件，已 gitignore）——此后不再搜索。
- **报错时机（懒探测）**：只有当任务首次需要运行某个 `.py` 脚本时才解析解释器；
  全部候选失败时立即报错，错误信息需包含：
  - 已尝试的候选清单；
  - 两条修复路径——把可用解释器写入 `scripts/python.json`（一行 JSON：`{"python": "D:/path/python.exe"}`），
    或安装 Python ≥ 3.9。
- 换用新解释器：手动改 `scripts/python.json`（或删除后走一遍搜索）。

## 渲染与预览注意事项

- **改 `theme/scss/`（`*.scss` 主题变量）、`theme/css/`（`*.css` 组件规则）或 `theme/includes/fonts.html`
  会触发整本重渲染**（明暗两套 SASS 各编译一次），非增量，改动后请留意耗时。
  这正是 `quarto preview` 启动后空白/转圈数秒的主因——它每次启动都整本重渲染并重编译两套 SASS。
- **日常查看优先用 `quarto render` 后直接打开 `_book/index.html`**：
  静态产物秒开，无预览服务器的整本重渲染/SASS 重编译开销；
  只有需要实时热更新时才开 `quarto preview`。
- **不要每次 preview 都清缓存**：保留 `.quarto/` 与全局 SASS 编译缓存时，preview 启动很快
  （仅首次/改了主题才重编译）。下面「彻底清缓存」的命令**只在改完主题/`_quarto.yml` 后样式仍不生效时才用**，
  不要当作常规步骤。
- `_book/`、`.quarto/` 是生成产物，已被 `.gitignore` 和 `opencode.json` 的 watcher 排除，不要手动编辑。
- **mermaid 懒加载**：`scripts/defer-mermaid.py` 会给输出 HTML 里 `mermaid.min.js` / `mermaid-init.js` 的
  `<script>` 加 `defer`，使其不阻塞首屏；不要手工把输出 HTML 里的这两个脚本改回同步加载。
  本地 `quarto render` 不自动执行该脚本；发布时由 GitHub Actions 在渲染后自动执行
  （见 `.github/workflows/pages.yml`）。如需本地查看该效果，按「运行 Python 脚本」解析解释器后手动运行
  `python scripts/defer-mermaid.py`。
- **`quarto preview` 在 Windows 上偶发卡死**（Deno 监视器/SASS）。卡死时的清理方式：

```powershell
Get-Process quarto,deno -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item -LiteralPath .quarto -Recurse -Force
quarto preview   # 重新启动
```

- **改 `_quarto.yml` 里的主题类选项（`theme` / `grid` / `highlight-style` 等）后样式可能不生效**：
  Quarto 的 SASS 编译缓存不仅在 `.quarto/`，还会落在全局目录 `$env:LOCALAPPDATA\quarto` 与 `~/.cache/quarto`；
  仅删 `.quarto` 仍会复用旧编译产物（侧栏/正文/页边距宽度等 `grid.*` 改动尤其容易踩坑）。
  彻底清缓存再重渲染的做法：

```powershell
Get-Process quarto,deno -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item -LiteralPath .quarto -Recurse -Force
Remove-Item -LiteralPath $env:LOCALAPPDATA\quarto -Recurse -Force
Remove-Item -LiteralPath $env:USERPROFILE\.cache\quarto -Recurse -Force
quarto render --to html
```

- **校验布局是否生效时，不要对压缩后的大 CSS（`site_libs/bootstrap/*.min.css`，单行约 500KB）
  做宽模式全串扫描或打印全部 `grid-template-columns` 命中项**——会输出海量内容并卡死。
  用单次字面匹配 + 限定输出，毫秒级返回。确认 `grid.sidebar-width` 是否生效：
  页面 `body` 为 `nav-sidebar floating` 时走**浮动栅格**，侧栏不是单轨道，而是
  **分段轨道 seg1/seg2/seg3 = 0.1w/0.2w、0.2w/0.6w、0.1w/0.2w**（`_bootstrap-mixins.scss` 的
  `page-columns-float-wide`）；单轨 `minmax(0px, 174px)` 属 **docked 变体**，浮动页不适用，不要当验收判据。

```powershell
# sidebar-width: 300px → 分段轨道应为 minmax(30px, 60px) 与 minmax(60px, 180px)（明暗两套各 1 处）
Get-ChildItem _book\site_libs\bootstrap -Filter *.min.css | Select-String -SimpleMatch 'minmax(30px, 60px)' | Measure-Object
Get-ChildItem _book\site_libs\bootstrap -Filter *.min.css | Select-String -SimpleMatch 'minmax(60px, 180px)' | Measure-Object
```

## 样式结构（明暗双主题）

- `theme/scss/theme-light.scss` / `theme-dark.scss`：仅 Bootstrap/主题变量（字体、主色、底色等），**不含组件规则**。
- **字体**：三层栈——Web 首选 **Inter**（拉丁）/ **Noto Sans SC 思源黑体**（中文）/ **IBM Plex Mono**
  （代码，opencode 同款），经 `theme/includes/fonts.html` 以 loli.net（Google Fonts 国内镜像）加载
  （css2、unicode-range 切片按需加载、`display=swap`、preconnect）；系统字体栈完整保留为回退，
  CDN 不可达时无感降级。
  字体栈三处需同步：两个 `theme-*.scss` 的 `$font-family-*`、`tokens.css` 的 `--ui-font` / `--mono-font`、
  `fonts.html` 的加载清单。
- `theme/css/*.css`：组件规则按域拆分，加载顺序 = `_quarto.yml` 的 `css:` 列表
  （保持原 common.css 的级联顺序，勿乱序）；颜色走 `tokens.css` 变量，
  由 `body.quarto-light` / `body.quarto-dark` 切换。**改样式先找对应域文件**：

  | 域 | 文件 | 职责 |
  |---|---|---|
  | `tokens` | `tokens.css` | 设计令牌 |
  | `base` | `base.css` | 基础排版 |
  | `code` | `code.css` | 代码块 |
  | `content` | `content.css` | 正文与表格 |
  | `mermaid` | `mermaid.css` | 图表 |
  | `nav` | `nav.css` | 导航与面包屑 |
  | `sidebar` | `sidebar.css` | 侧栏与 TOC |
  | `callouts` | `callouts.css` | 提示卡片 |
  | `landing` | `landing.css` | 首页 |
  | `misc` | `misc.css` | 页脚与打印 |

- **设计基准：opencode 暖灰**（色温对齐 opencode.ai/docs，结构沿用 GitHub Primer 值域）：
  - 标题字重 600；正文链接近黑 + 常驻下划线。
  - 表格与 callout 无框；callout 为 opencode aside 风：彩色浅底、标题左/内容右 flex、<768px 上下堆叠。
    语义色双轨——图标取色在 `theme-*.scss` 的 `$callout-color-*`，标题字色/底色在 `tokens.css` 的 `--callout-*`；
    中文标题由 `_quarto.yml` 顶层 `language:` 覆盖：note 注意 / tip 提示 / important 重要 / warning 警告 / caution 危险。
  - 代码块为 opencode EC 卡片：`div.sourceCode` 外框+圆角+弱底、头行为 2.25rem 空占位条+发丝线、
    `pre` 透明无边框，内边距 `0.75rem 1rem`，2rem 方形常显复制按钮。
  - 引用块（`>`）为 2px 左条 + 次要灰 + 0.9375rem（略小于正文，次要提示定位，见 `content.css`）。
  - 章节以 `---` 分隔。
- **垂直节奏**：块间距由 `#quarto-document-content > *` 与 `#quarto-document-content section > *` 的上边距节奏统一控制
  （Quarto 将 h2 章节包在 `<section class="level2">` 内，两者都要写）。
  正文↔代码块 1.375rem（上下对称）、代码块↔代码块 1.5rem、代码块前的说明段紧贴代码块 0.5rem、
  标题上方 3.375/2.5/2.0rem（下方紧贴首段 0.75rem）；正文行高 1.6875；列表 `li+li` 0.625rem。
  **不要**再对 `pre`/`p` 单独设 `margin-bottom`，否则会与外边距折叠打架。
- **章节横线（`---`）**：每个 `##` / `###` 标题前在 qmd 源里写一条 `---` 水平线（opencode 风，上下各空一行）——
  本仓库的章节分隔由这条线承担，`##`/`###` **不再**有下边框；
  Quarto 默认注入的 `h2,.h2{border-bottom:1px solid #dee2e6;padding-bottom:.5rem}` 已在 `base.css` 显式覆盖取消，
  改主题时勿删该规则。
  横线由「段落节奏」的 3.375rem 上距承托，与标题上边距同刻度；
  `---` 必须与前一段之间空一行，否则前一段会被 Pandoc 解析为 setext 二级标题（见 quarto-docs 的 pitfalls）。
  首页 `index.qmd` 与 part 索引页（含 `.hero-eyebrow`）不写 `---`。

## 代码块约定

- **两种块**：代码文件块（C++ 源码，用 `cpp` 语言围栏）、终端/命令块（用 `powershell` / `bash` 语言围栏）。
  命令与其输出写在同一个终端块内，不再区分"预期输出块"。
- **一律用普通语言围栏（不要加大括号 `{…}`）**：`cpp` / `powershell` / `bash` 等都不是 Quarto 执行引擎，
  一旦写成 ```` {powershell} ```` / ```` {.cpp} ```` 会被当成可执行 cell 而渲染异常
  （变成 inline code 或尝试拉起 python 内核）。
  文件名/说明统一用代码块上方的正文段落写一句中文说明，不要用 `title=`。
- **例外：图表围栏必须加大括号**。`mermaid` 与 `dot` 是 Quarto 内置的图表引擎，必须用可执行 cell 写法
  ```` {mermaid} ```` / ```` {dot} ````（带花括号），否则 Quarto 只会把它当普通代码块渲染成原文
  （不会加载 mermaid.js / 生成图像）。不要在 `mermaid`/`dot` 块上写 `title=`。
  - **每个 mermaid 块首行必须加 `%%{init}%%` 指令**（测量字体 = 渲染字体，否则 mermaid 按默认 trebuchet 测量、
    页面按 Inter/思源渲染，节点文字会折行并压到框底），同时把一行阈值放宽到 `wrappingWidth: 320`
    （≈18 个汉字，短句单行、超长才换行）。
  - **fontFamily 值里不能带单引号**——mermaid 指令解析器遇到 `'` 会丢弃整条指令（已实测）；
    字体名一律裸写（`Inter, Noto Sans SC, ...`，与 `tokens.css` 的 `--ui-font` 同序去引号）；
    模板见 `content/environment/setup-wsl2.qmd` 的路线图。
  - mermaid 视觉（中性灰 opencode 风、明暗自适应）由 `theme/css/mermaid.css` 的 `--mermaid-*` 变量驱动
    （含 SVG 内联样式的 `!important` 兜底，以及「排版守卫」段把页面断行规则挡在 SVG 外），
    依赖 `_quarto.yml` **不配置** `mermaid.theme`。
- **指令块（只给要敲的命令）：不加 `PS>` / `$` 前缀**，保证复制按钮只复制纯命令。
  多行命令每行一条、**命令之间空一行**；
  shell 由语言围栏（`powershell` / `bash`）+ 代码块前的正文说明（如"在 PowerShell（管理员）中执行："），
  不再单独加环境名条。
- **演示块（命令 + 预期输出）：统一用 `$` 作为唯一提示符**，`$` 后跟命令、输出紧跟其后，与命令同块；
  PowerShell 与 Bash 演示块均用 `$`（即全站只有 `$` 一种提示符，不再出现 `PS>`）。
- **性质相近的命令可合并演示块**：同一主题的多条查看命令（如多个 `--version`）合并到一个块，
  每条命令上方 `#` 注释标明身份（如「# g++：编译器版本」），命令对之间空一行；
  正文只负责介绍（判据 + 挑代表演示），不逐条铺正文、不逐条分块（细则见 quarto-docs skill 的 authoring.md）。
- **代码配色完全交给 GitHub 风格高亮**：`highlight-style: github-light` / `github-dark`（已在 `_quarto.yml` 配置）
  ——已实测与 opencode 代码取色逐项一致，`code.css` 不再为代码块/终端额外设置配色或外壳（`.console`）样式。
  唯一微调：bash/powershell 的运算符 `.op` 着 opencode 红（亮 `#BF3441` / 暗 `#F97583`，见 `code.css`；
  C++ 等语言的括号/分号保持正文色）。
- **每块代码都要有说明**：代码块上方用一句正文说明（这条命令 / 这段源码做什么）。
  说明段为次要灰色、与代码块收紧；**切勿**给代码块本身（`pre`）着灰色——代码文本必须保持高对比正文色。
- **正文用中文标点**：中文正文使用全角标点（，。：；！？「」（）），代码块与内联代码（`...`）内保持 ASCII 标点不变。
- C++ 示例统一放 `code/`，编译选项 `-std=c++20 -Wall -Wextra`（见「示例源码」）。

## 章节标题约定

- 章节 `.qmd` 用 YAML `title:`，**不要**再写同文本的 `# H1`；页面内小节从 `##` 开始。
- **小节间横线（`---`）**：每个 `##` / `###` 标题前加一条 `---`（上下各空一行），形成 opencode 风的分节；
  标题本身**不要**再加下边框（已由 `---` 承担）。
  首页 `index.qmd` 与 part 索引页（含 `.hero-eyebrow`）不加 `---`。
- **标题层级归并（H2 伞 + H3 子）**：多个内容高度相关、同属一个大阶段的同级 `##` 小节，应收拢为一个 `##` 伞标题，
  各块降为 `###` 子标题，避免平铺过多同级 H2 导致结构破碎。
  改前先 grep 确认无 `@sec-` / `#anchor` 交叉引用这些标题，以免断链。
  `content/environment/setup-wsl2.qmd` 即采用：章首 `## 本章目标` 以目标列表 + 路线图作总览，
  其后 `## 准备与安装` 下挂 `### 先决条件` / `### 安装 WSL2`（内含基本验证与常见问题 callout）/ `### 启动与关闭` 的写法。
- 每章（位于 `content/` 下）YAML **只需** `title:`，**不要**写 `description:`
  ——Book 章节页既不把 `description` 渲染进标题块，章节页也不需要该元信息。
  章节可见引言用**正文普通段落**写在标题下（不套 `.description` 样式）。
  书籍首页 `index.qmd`（不在 `content/` 下）保留 `title:` + `description:`，其 `description` 渲染为 Hero 引导段
  （见下「首页」条）。
- **规范**：标题（h1）之下首块须为**正文引言段落**（普通段落，不套特殊样式），且仅写**动机与目标**
  （承接已知 → 指出限制与动机 → 引出本章问题，1–3 句），**不预演/罗列本节 `##` 小节内容**（渐进式披露）；
  细节留到各小节展开。
  callout / note / tip 应置于引言之后，**禁止**顶在标题之下。
  示例见 `content/environment/setup-wsl2.qmd`（其引言即渐进式写法）。
- 首页 `index.qmd` 同样用 `title:` + `description:`，description 显示为 Hero 引导段。
- 标题块内面包屑（`准备开发环境与工具链 > 章节`）桌面端（≥992px）**显示**、与标题同栏左对齐
  （窄屏由 Quarto 生成的 `d-none` 隐藏，改显次级导航里的面包屑；
  次级导航面包屑的 ≥992px 隐藏规则只作用于 `nav.quarto-secondary-nav .quarto-page-breadcrumbs`，
  不要写回全局 `.quarto-page-breadcrumbs`——会被标题块实例上的 `d-lg-block !important` 架空）。
  条目为 flex 行、分隔符为 SVG chevron（mask + currentColor 几何居中，左右等距：
  左距 = 元素 margin-left、右距 = li 的 flex gap，勿改回 `>` 字符——字形在字框内光学偏高）
  （`.quarto-page-breadcrumbs .breadcrumb-item`）；
  其→标题间距由 `.quarto-title-breadcrumbs { margin-bottom: 0.5rem }` 控制。
- **章节收尾与结构**：章末用「本章回顾」（重点句直接讲重点：结果 + 确认方式 + 下一步；
  成就列表仅在有多项增量时用，不复读本章目标）
  与「下一步」（站内规划章节）/「相关资源」（外部链接）双段；
  关键步骤用 `.callout-important` 强调；可用 ```` ```{mermaid} ```` 画流程/架构图
  （注意带花括号，见上「代码块约定」例外条）。
  原理与实操**不显式分段**，靠「说明在前、命令在后」的节奏隐式体现，保持备忘录随手查的质感。

## 示例源码

- C++ 示例统一放 `code/`，按主题建目录：`code/<主题>/<小写下划线>.cpp`，
  `<主题>` 与 `content/` 章节目录同名（如 `content/environment/` ↔ `code/environment/`）；
  编译选项统一 `-std=c++20 -Wall -Wextra`。
  新建示例目录可直接用 `cpp-project` skill 的 `init_project.py`（`code/` 下默认 bare 布局，仅生成 `main.cpp`）。
- **代码风格：排版 LLVM / 命名 Google / 异常启用**，
  唯一出处 `.opencode/skills/cpp-content/references/cpp/code-style.md`；
  配置在仓库根 `.clang-format`（2 空格缩进、80 列）与 `.clang-tidy`
  （modernize + Core Guidelines 子集 + Google 命名规则）。
- 校验：`python .opencode/skills/cpp-content/scripts/verify_examples.py --style`
  （clang-format 为硬门槛，clang-tidy 出报告；工具缺失时降级为警告；解释器解析见「运行 Python 脚本」）。
- 默认运行环境：Windows 上的 WSL2。

## 目录职责

- `content/`：备忘录章节（`.qmd`）；`code/`：C++ 示例源码（与 content 主题同名目录）。
- `theme/scss/`：明暗主题变量（仅 `.scss`）；`theme/css/`：按域拆分的组件规则（`.css`）；
  `theme/includes/`：fonts/footer 注入片段。
- `scripts/`：仓库级构建/CI 脚本（如 `defer-mermaid.py`，发布时由 Actions 执行）与 `python.json`
  （本机指定的 Python 解释器，gitignore）。
- agent 工作流工具放各 skill 自己的 `scripts/`（scaffold / verify / check / init 等），**不**进根 `scripts/`，
  保持 skill 自包含。
- `.opencode/skills/**` 与 `.opencode/package.json`（锁定插件版本）随仓库分发；
  `.opencode/node_modules/`、`.opencode/plans/`、`/scripts/python.json` 不入库
  （根 `.gitignore` 覆盖；clone 后 `npm install` / 解析协议重建，见 github-ops skill）。

## 仓库格式约定

- 行尾与编码以根 `.gitattributes` 为准：文本一律 **LF**（`* text=auto eol=lf`），
  二进制扩展名显式 `binary`；编码一律 **UTF-8 无 BOM**
  （PowerShell 5.1 写文件需用 `UTF8Encoding($false)`，见 quarto-docs pitfalls 第 5 条）。
- 首次提交用 `git add --renormalize .` 落地行尾策略；此后新增文件自动遵循。
