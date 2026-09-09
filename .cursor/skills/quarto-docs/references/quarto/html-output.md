# HTML 输出配置

> 速查：外观选项集中在根目录配置的格式块下 · 目录收四级标题放右侧 · 本仓库不用行号、长行换行、不折叠

选项语义、作用域层级与生效边界的**唯一出处是知识库**，本文件只留本仓库的取值和写作口径：

```powershell
python .cursor/skills/agent-ops/scripts/run.py kb-search "html 输出选项" --domain tooling --subdomain html_output
python .cursor/skills/agent-ops/scripts/run.py kb-search --toc "代码块显示"
```

## 本仓库的现行取值

全部写在根目录 `_quarto.yml` 的 `format: html:` 下，章节 front matter 不重复设置：

| 选项 | 取值 | 备注 |
|---|---|---|
| `theme` | `light: [cosmo, .cursor/skills/quarto-theme/assets/theme/scss/theme-light.scss]` + `dark: [darkly, …]` | 内置主题与项目样式叠加，顺序决定覆盖关系 |
| `highlight-style` | `light: github-light` + `dark: github-dark` | 明暗分别指定，语义颜色交给引擎 |
| `toc` / `toc-depth` / `toc-location` | `true` / `4` / `right` | 右侧目录，窄屏会折叠，不作唯一定位手段 |
| `number-sections` | `false` | 因此标题不手填序号，见 `basics.md` |
| `code-copy` / `code-overflow` | `true` / `wrap` | 长行换行，不让读者横向拖动 |
| `grid` | sidebar 280 / body 800 / margin 240 / gutter 1.5em | 页面栅格 |
| `lang` | `zh` | 影响部分 HTML 行为与提示框默认词 |

本仓库**不开启**代码行号（`code-line-numbers`）与代码折叠（`code-fold`）：取舍依据见 `cpp-tooling-quarto-html-v2` 的知识文件。

## 改动约定

1. 改 `format: html:` 任何取值都属于主题级改动，会触发整本渲染，先确认代价再走 `run.py render`。
2. 新增或删减 `.cursor/skills/quarto-theme/assets/theme/css/**` 组件样式表时，同步修改配置里的样式表清单，否则新样式不参与渲染。
3. 页面视觉问题（提示符配色、文件名条、术语色）改 `.cursor/skills/quarto-theme/assets/theme/**` 与设计令牌，不在文档里内联样式，也不改高亮配置。
4. 流程图使用图表专用围栏，配色由主题样式控制；配置里不指定图表主题名。
5. 拿不准选项名、默认值或嵌套层级时查官方参考页，不凭记忆写 YAML（入口见 `pitfalls.md` #8）。

## 验证

渲染后确认：目录深度与位置符合预期、明暗两套高亮都可读、没有遗留依赖目录（目标是站点而非单文件分发）。
主题或目录看起来没生效时先硬刷新排除缓存，再核对选项嵌套层级。
