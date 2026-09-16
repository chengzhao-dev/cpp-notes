# HTML 输出与渲染排错

## HTML 输出配置

> 速查：外观选项集中在根目录配置的格式块下 · 目录收至三级标题放右侧 · 本仓库不用行号、长行换行、代码块不折叠。回顾答案使用 `.answer` 并渲染为原生 details

选项语义、作用域层级与生效边界的**唯一出处是知识库**，本文件只留本仓库的取值和写作口径：

```powershell
& .agents/skills/agent-ops/scripts/run.ps1 kb-search "html 输出选项" --domain quarto-docs --subdomain html_output
& .agents/skills/agent-ops/scripts/run.ps1 kb-search --toc "代码块显示"
```

### 本仓库的现行取值

全部写在根目录 `_quarto.yml` 的 `format: html:` 下，章节 front matter 不重复设置：

| 选项 | 取值 | 备注 |
|---|---|---|
| `theme` | `light: [cosmo, .agents/skills/quarto-theme/assets/theme/scss/theme-light.scss]` + `dark: [darkly, …]` | 内置主题与项目样式叠加，顺序决定覆盖关系 |
| `highlight-style` | `light: github-light` + `dark: github-dark` | 明暗分别指定，语义颜色交给引擎 |
| `filters` | `.agents/skills/quarto-docs/scripts/answer-disclosure.lua` | 将正文 `.answer` 转为默认收起的原生 `details` |
| `toc` / `toc-depth` / `toc-location` | `true` / `3` / `right` | 右侧目录最多到 H3，窄屏会折叠，不作唯一定位手段 |
| `number-sections` | `false` | 因此标题不手填序号，见 `basics.md` |
| `code-copy` / `code-overflow` | `true` / `wrap` | 长行换行，不让读者横向拖动 |
| `grid` | sidebar 240 / body 800 / margin 208 / gutter 1rem | 页面栅格 |
| `lang` | `zh` | 影响部分 HTML 行为与提示框默认词 |

本仓库**不开启**代码行号（`code-line-numbers`）与代码折叠（`code-fold`）：取舍依据见 `cpp-tooling-quarto-html-v2` 的知识文件。

站点 QMD 代码块使用 `{.语言 filename="标题"}`。Quarto 会把标题渲染为 `.code-with-filename-file`，外观与复制按钮位置由主题统一控制。标题缺失由 `check_docs.py` 拦截。

### 改动约定

1. 改 `format: html:` 任何取值都属于主题级改动，会触发整本渲染，先确认代价再走 `run.py render`。
2. 新增或删减 `.agents/skills/quarto-theme/assets/theme/css/**` 组件样式表时，同步修改配置里的样式表清单，否则新样式不参与渲染。
3. 页面视觉问题（提示符配色、文件名条、术语色）改 `.agents/skills/quarto-theme/assets/theme/**` 与设计令牌，不在文档里内联样式，也不改高亮配置。
4. 流程图使用图表专用围栏，配色由主题样式控制。配置里不指定图表主题名。
5. 拿不准选项名、默认值或嵌套层级时查官方参考页，不凭记忆写 YAML（入口见本文件 #8）。

### 验证

渲染后确认：目录深度与位置符合预期、明暗两套高亮都可读、没有遗留依赖目录（目标是站点而非单文件分发）。
主题或目录看起来没生效时先硬刷新排除缓存，再核对选项嵌套层级。

## 渲染与发布排查索引
按症状查此表：每条只给可执行处置。**行为成因与取舍**的唯一出处是知识库，用
`& .agents/skills/agent-ops/scripts/run.ps1 kb-search "<症状关键词>"` 取用
（可加 `--domain quarto-docs --subdomain rendering`）。本文件不重复解释根因，只保留编号、症状与处置。

> 速查：内嵌资源用 `embed-resources` 且必须嵌在 `format: html:` 下 · 路径用相对、纯 ASCII · 拿不准 YAML 先查官方 `llms.txt` · callout 只用内置 5 类 · `{{< include >}}` 必须包在带语言名的围栏里

### 1. `self-contained` 已弃用

- **症状**：渲染出现 deprecated 警告。
- **处置**：改名为 `embed-resources: true`，并确认它嵌套在 `format: html:` 下而非顶层。

### 2. 渲染后仍有 `_files/` 依赖目录

- **症状**：目标是单文件 HTML，产物仍带伴随目录。
- **处置**：核对 `embed-resources` 的拼写、缩进与嵌套层级。由 JS 运行时加载的资源无法内嵌（zoom、speaker notes 等），属已知限制，不要再改配置。

### 3. 路径与资源 404

- **症状**：本地正常，发布后图片或资源打不开。
- **处置**：改用相对路径，不要写死 `https://...` 指向内部资源，核对文件名大小写，站点托管区分大小写。

### 4. 主题/TOC 不生效

- **症状**：改了 `theme:` 或 `toc:` 页面没变化。
- **处置**：先硬刷新（Ctrl+Shift+R）排除缓存，再确认两者位于 `format: html:` 下。TOC 只收录 `##` 及以下的真实 Markdown 标题，`**加粗**` 与裸 `<h2>` 不会进入。

### 5. 中文乱码/编码

- **症状**：中文变成「锟/鐜/绔」类字串，或文件带 BOM、行尾变 CRLF。
- **处置**：改 `.qmd` 或 Skill 文档后先跑 `run.ps1 check --profile fast`。失败时从 Git 可读版本恢复再重做修改，**不要**对已乱码文本反向转码。全仓库统一 UTF-8 无 BOM、LF（`.gitattributes` 约定，见 github-ops skill 的 `git-workflow.md`）。front matter 可设 `lang: zh`。
- **注意**：PowerShell 5.1 的 `Out-File`/`Set-Content -Encoding utf8` 会附带 BOM，需显式无 BOM 或改用 Python 写入，不要让系统代码页参与中文读写。
- **自检**：`run.ps1 check --profile fast` 的 `encoding` 项已覆盖 BOM、行尾与乱码特征。

### 6. 渲染失败排查顺序

1. 看完整报错，先判断失败阶段：YAML 解析、Lua 过滤器、还是代码执行。
2. YAML 阶段：核对缩进/冒号与选项嵌套层级（如 `sidebar` 属于 `website` 而非 `format.html`）。
3. 代码执行阶段（knitr/jupyter）：检查依赖是否安装、`cache` 是否过期（清 `_cache/` 重试）。
4. 找不到单文件：确认在项目根目录执行，`quarto render` 默认作用于整个项目。

### 7. 发布到 GitHub 但页面没更新

- **处置顺序**：先看 Actions 是否成功（失败查日志）→ 分支部署核对分支与目录（如 `main` + `/docs`）→ `gh-pages` 方式确认推送成功且远端存在该分支 → 最后才考虑缓存或 CDN 延迟（等几分钟或强刷新）。

### 8. 文档关键词速查（避免幻觉 YAML）

- **规则**：拿不准选项名、默认值或嵌套层级时不要凭记忆写 YAML，先查官方参考：
  - Quarto LLM 优化文档索引：`quarto.org/llms.txt`
  - 单页把 `.html` 换成 `.llms.md`（如 `https://quarto.org/docs/reference/formats/html.llms.md`）
  - 普通文档页：`https://quarto.org/docs/reference/formats/html.html`

### 9. 路径/名称含特殊字符导致渲染失败

- **症状**：`quarto render` 报 `recoverEncode: invalid argument (cannot encode character '\8209')`，错误栈在 `main.lua` 的 `writeFullIndex`/`io.open`。
- **处置**：项目、目录、文件名一律纯 ASCII，连字符一律用普通 `-`（U+002D）。可用 `.agents/skills/quarto-docs/scripts/check_ascii_names.py` 校验整个仓库。命名规范见 `../../../cpp-content/references/cpp/cpp.md`。
- **定位隐藏字符**（把目录名转成字节，查看是否出现 `E2 80 91`）：

```powershell
$d = Get-ChildItem -LiteralPath "D:\Github" -Force
[System.Text.Encoding]::UTF8.GetBytes($d[0].Name) -join " "
```

### 10. YAML `title:` 与同文本 `# H1` 重复 → 页面出现两个标题

- **症状**：标题重复出现两遍，Book 章节结构错位。
- **处置**：章节标题**二选一**，用 YAML `title:` 后不再写同文本 `# H1`，页面内小节从 `##` 开始。开篇可见文字写正文顶部。普通章节**不要写** `description:`（仅 `index.qmd` 封面页可见）。规范唯一出处见 `basics.md`「章节标题约定」。

### 11. `---` 紧接段落 → 前一段被解析为 setext 二级标题

- **症状**：某段文字莫名变成大号 H2，TOC 出现意料外标题。
- **处置**：本仓库约定小节（`##`/`###`）前**不写** `---` 分隔线（分隔靠 H2 默认下边框，见 `authoring.md`）。确需水平线时前后各留一个空行。YAML front matter 的 `---` 不受影响。

### 12. 自定义 `.callout-*` 类被静默丢弃 → 提示框退化成普通小节

- **症状**：源文件写了 `::: {.callout-best-practice}`，渲染后没有左色条提示框，且块内 `## 标题` 混进右侧目录。
- **处置**：只用内置 `note`/`tip`/`warning`/`important`/`caution` 五类，标题写在块内首行 `## …`，并保留全局中文类型标题。「最佳实践 / 关键洞察 / 深入」三层语义到内置类型的映射见 `authoring.md`「Callout 提示框」。
- **自检**：渲染后跑 `run.ps1 check --profile book`，`callouts` 项会扫描 `_book/**/*.html`，出现退化的 `<section class="levelN … callout-…">` 即返回退出码 1。

### 13. `{{< include >}}` 引用代码文件未加属性围栏 → 乱码式排版、目录被污染

- **症状**：渲染出的脚本失去高亮与等宽底色，`#` 注释行变成大号标题，含 `*`、`_` 的行变成斜体或粗体，右侧目录多出假标题。
- **处置**：`{{< include >}}` 整体放进 `{.cpp filename="main.cpp"}` 形式的属性围栏，按扩展名选语言并把 `filename` 写成真实文件名，**没有一个例外**。规则见 `authoring.md`「代码块」。
