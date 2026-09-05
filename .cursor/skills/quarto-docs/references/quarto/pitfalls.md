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
- 不要让 PowerShell 的系统代码页参与中文文件的读取、转换或回写；这会把正常中文变成“锟/鐜/绔”等 UTF-8/GBK 乱码。
- 修改 `.qmd` 或 Skill 文档后，先运行 `python scripts/agent/check_encoding.py`；它会检查 UTF-8、BOM、行尾和常见乱码特征。
- 检查失败时从 Git 可读版本恢复，再重新应用修改；不要对已经乱码的文本盲目反向转码。

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

## 11. `---` 紧接段落、前后无空行 → 前一段被解析为 setext 二级标题（H2）

- **症状**：某段文字莫名变成大号二级标题，TOC / 侧栏出现意料外的标题。
- **根因**：Markdown 的 setext 语法会把「段落 + 紧接的 `---`」当成二级标题（h2）。本仓库约定小节（`##`/`###`）前**不写** `---` 分隔线（分隔靠 H2 默认下边框，见 `authoring.md`），所以章节标题不会触发此陷阱；但如果你主动用 `---` 作真正水平分割线，仍需小心。
- **规避**：若写 `---` 作水平线，其**前后都各留一个空行**（前段文本 → 空行 → `---` → 空行 → 后续内容）。YAML front matter 里的 `---` 不受影响（位于文件最顶，由 front matter 解析器处理）。章节分隔写法见 `authoring.md` 的「章节标题与开篇」节。

## 12. 自定义 `.callout-*` 类被静默丢弃 → 提示框退化成普通小节

- **症状**：源文件写了 `::: {.callout-best-practice}` / `{.callout-key-insight}`，渲染后页面上**没有**左色条提示框，只是一段普通正文；更糟的是它的 `## 标题` 出现在右侧目录里，和真正的小节混在一起。
- **根因**：Quarto（1.10 实测）只认 `note` / `tip` / `warning` / `important` / `caution` 五个内置 callout 类型。`callouts.lua` 依据 Attr 的 class 前缀识别类型，未知类型不产生 `Callout` 节点，整块按普通 `div` 走「带标题的章节」渲染路径；额外附加在内置类型上的 `.callout-*` 类同样被丢弃（不会保留到 `class` 属性）。主题里为这些名字准备的 CSS 选择器与令牌因此永不命中。
- **规避**：只用内置 5 类，标题写在块内首行 `## …`。本仓库的「最佳实践 / 关键洞察 / 深入」三层语义到内置类型的映射见 `authoring-elements.md`「Callout 提示框」。
- **自检**：渲染后执行 `python .cursor/skills/quarto-docs/scripts/check_callouts.py`，它扫描 `_book/**/*.html`：出现 `<section class="levelN … callout-…">` 即判为退化，返回退出码 1。
