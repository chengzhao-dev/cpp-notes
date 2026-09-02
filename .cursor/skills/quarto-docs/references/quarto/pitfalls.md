# 常见坑与排查

本文件是渲染/发布/编码/路径类问题的排查处。**章节标题 `title:` vs `# H1` 重复**、**文件名特殊字符**两项已分别在 `basics.md` 与 `../../../cpp-content/references/cpp/cpp.md` 给出规范，此处只做索引与补充坑。

> 速查：`self-contained` 已弃用 → `embed-resources` · 选项必须嵌套 `format: html:` 下 · 路径用相对、纯 ASCII · 拿不准 YAML 先查官方 `llms.txt`

## 1. `self-contained` 已弃用

- 老教程里的 `self-contained: true` 已弃用，现代写法是 `embed-resources: true`。
- 两者目的一致：把所有依赖内嵌为单一 HTML 文件。
- 若看到 "deprecated" 警告：直接改名为 `embed-resources: true`。
- 确认选项嵌套在 `format: html:` 下，不是顶层。

## 2. 渲染后仍有 `_files/` 依赖目录

- 说明 `embed-resources` 未生效：检查拼写与缩进、是否嵌套在 `html:` 下。
- 单文件场景目标：渲染结果应是**一个 .html 文件**，无伴随目录。
- 动态 JS 加载的资源（部分高级特性如 zoom、speaker notes）无法内嵌，属于已知限制。

## 3. 路径与资源 404

- 图片/资源用相对路径引用，发布到项目站点后 URL 前缀变化时相对路径仍有效。
- 不要写死 `https://...` 绝对 URL 到内部资源。
- GitHub Pages 项目站点区分大小写路径；文件大小写不一致会导致 404。

## 4. 主题/TOC 不生效

- 先硬刷新浏览器（Ctrl+Shift+R）排除缓存。
- 确认 `toc: true`、`theme:` 在 `format: html:` 下。
- TOC 只收录 `##` 级别及以下的真实 Markdown 标题；`**加粗**` 或裸 `<h2>` 不会进入。

## 5. 中文乱码/编码

- 源文件保存为 UTF-8（无 BOM）；全仓库文本编码统一 UTF-8 无 BOM、行尾统一 LF（`.gitattributes` 约定，见 github-ops skill 的 git-workflow.md）。
- front matter 可设 `lang: zh`。
- 若 PDF 场景中文缺字需字体，但 HTML 场景通常无需处理。
- **PowerShell 5.1 写文件默认 UTF-8 会带 BOM**：`Out-File`/`Set-Content -Encoding utf8` 产出带 BOM 文件；
  需要无 BOM 时用 `[System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))`，
  或改用 Python 脚本（`encoding="utf-8"` 默认无 BOM）写入。

## 6. 渲染失败排查顺序

1. 看完整报错（Quarto 会指出是 YAML 解析、Lua 过滤器、还是代码执行失败）。
2. 常见 YAML 错误：缩进/冒号、选项嵌套层级错误（如把 `sidebar` 错放 `format.html` 下，实际应在 `website` 下）。
3. 代码执行失败（knitr/jupyter）：检查依赖是否安装、`cache` 是否过期（清掉 `_cache/` 重试）。
4. 单文件找不到：确认命令在项目根目录运行，`quarto render` 默认全项目。

## 7. 发布到 GitHub 但页面没更新

- 检查 GitHub Actions 是否成功（失败则看日志）。
- branch 部署方式：确认选择的分支与目录正确（如 `main` + `/docs`）。
- 缓存/CDN 延迟：等待几分钟或强刷新。
- `gh-pages` 方式：确认推送成功且远端仓库存在对应分支。

## 8. 文档关键词速查（避免幻觉 YAML）

- 拿不准选项名/默认值/嵌套层级时，**不要凭记忆写 YAML**，去查官方参考：
  - Quarto LLM 优化文档：`quarto.org/llms.txt`
  - 单页把 `.html` 换成 `.llms.md`（如 `https://quarto.org/docs/reference/formats/html.llms.md`）
  - 普通文档：`https://quarto.org/docs/reference/formats/html.html`

## 9. 路径/名称含特殊字符导致渲染失败

- **症状**：`quarto render` 报 `recoverEncode: invalid argument (cannot encode character '\8209')`，错误栈在 `main.lua` 的 `writeFullIndex`/`io.open`。
- **根因**：项目路径或目录名含非 ASCII 特殊字符。例如目录名 `cpp‑memo` 中间的连字符其实是 **U+2011（non-breaking hyphen）**，并非普通 `-`（U+002D）。Quarto 的 Windows Lua 过滤器写 crossref 索引文件时无法编码该字符。
- **规避**：**项目/目录/文件名一律使用纯 ASCII 字符**；
  连字符一律用普通 `-`（U+002D），不要用全角、U+2011 等特殊连字符。
  规范见 `../../../cpp-content/references/cpp/cpp.md` 的命名规范；
  可用 `.cursor/skills/quarto-docs/scripts/check_ascii_names.py` 校验整个仓库。
- **排查**：用字节级确认是否有隐藏特殊字符，例如在 PowerShell 中把目录名转成字节查看是否出现 `E2 80 91`（U+2011 的 UTF-8）：
  ```powershell
  $d = Get-ChildItem -LiteralPath "D:\Github" -Force
  [System.Text.Encoding]::UTF8.GetBytes($d[0].Name) -join " "
  ```

## 10. YAML `title:` 与同文本 `# H1` 重复 → 页面出现两个标题 / 结构错乱

- **症状**：页面顶部标题重复出现两遍；Book 的章节结构错位。
- **根因**：`.qmd` 里同时写了 YAML `title:` 和文本相同的顶层 `# H1`。Quarto 把 YAML 标题渲染到 `<header>`，把 `# H1` 渲染成另一个一级章节。
- **规避**：章节标题**二选一**——用 YAML `title:`，不要再写同文本 `# H1`；页面内小节从 `##` 开始。开篇可见文字写正文顶部；普通章节**不要写** `description:`（`description:` 仅 `index.qmd` 封面页可见）。规范见 `basics.md` 的「章节标题约定」。

## 11. `---` 前无空行 → 前一段被解析为 setext 二级标题（H2）

- **症状**：某段文字莫名变成大号二级标题，后面的 `##` 小节结构错位；TOC / 侧栏出现意料外的标题。
- **根因**：本仓库约定每个 `##`/`###` 前写一条 `---` 作章节分隔线（docs 分节）。若 `---` 紧接前一段、中间**没有空行**，Markdown 的 setext 语法会把「前一段文本 + `---`」当成一个二级标题（h2）。
- **规避**：`---` 的**前后都各留一个空行**（前段文本 → 空行 → `---` → 空行 → 标题）。YAML front matter 里的 `---` 不受影响（位于文件最顶，由 front matter 解析器处理）。章节分隔写法见 `authoring.md` 的「章节横线」节。
