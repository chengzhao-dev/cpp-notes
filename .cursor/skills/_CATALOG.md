# Skills 目录索引

给 `scope.py` 与 agent 用的全景表：一次看清「有什么、管什么、何时读」，避免因不知道存在而漏读（降质）或整包多读（费 token）。
行数上限由 `scripts/agent/check_skill_size.py` 强制（L1 SKILL ≤45、L2 reference ≤160）。

| 文件 | 管什么 | 何时读我 |
|---|---|---|
| `quarto-docs/references/quarto/authoring.md` | 正文结构、代码块、终端命令块约定 | 写/改任何 `.qmd` 正文 |
| `quarto-docs/references/quarto/authoring-elements.md` | 图表、表格、Callout、FAQ、交叉引用 | 章里要放图/表/提示框/FAQ |
| `quarto-docs/references/quarto/basics.md` | Book 结构、front matter、标题层级（规范唯一出处） | 改 `_quarto.yml` 或章节骨架 |
| `quarto-docs/references/quarto/html-output.md` | HTML 输出选项与产物形态 | 调 format/html 选项 |
| `quarto-docs/references/quarto/pitfalls.md` | 渲染陷阱与根因（编号索引） | 渲染报错或表现异常 |
| `quarto-docs/references/zh/writing-style-core.md` | 中文写作风格核心 | 写/改任何中文正文 |
| `quarto-docs/references/zh/avoid-words.md` | 润色禁词表 | 润色阶段 |
| `quarto-docs/references/zh/cases-index.md` | 案例索引 | 需要范例时（再按需读单个 case） |
| `cpp-content/references/cpp/code-style.md` | C++ 命名、注释与留白、工具 | 写示例代码或跑 `--style` |
| `cpp-content/references/cpp/cpp.md` | 语言基础要点 | core / getting-started 章 |
| `cpp-content/references/cpp/stl.md` | 容器 / 迭代器 / 算法 | stl 与 cheatsheet 章 |
| `cpp-content/references/cpp/modern-cpp.md` | RAII、智能指针、移动语义 | memory 章 |
| `cpp-content/references/cpp/performance.md` | 缓存局部性、RVO/NRVO、剖析 | performance 章 |
| `cpp-content/references/cpp/pitfalls-ub.md` | 常见 bug 与未定义行为 | debugging 章 |
| `cpp-content/references/cpp/toolchain.md` | g++/CMake/WSL 工具链与构建约定 | 环境、构建、CMake 章 |
| `cpp-content/references/cpp/engineering.md` | 项目布局与 CMake 目标 | toolchain 章 |
| `cpp-content/references/cpp/templates.md` | 模板与泛型 | 进阶章按需 |
| `quarto-theme/references/design-tokens.md` | 设计令牌（颜色/字号/间距唯一出处） | 改任何 `theme/**` |
| `quarto-theme/references/theme-structure.md` | 主题文件结构与装配顺序 | 新增/调整 css 文件 |
| `github-ops/references/git-workflow.md` | 分支、提交、禁止事项 | 任何 git 操作前 |
| `github-ops/references/github-pages.md` | Pages 部署与 gh-pages 约定 | 发布排错 |
| `github-ops/references/actions.md` | CI 工作流 | 改 `.github/workflows/*` |
| `github-ops/references/gh-cli.md`、`issues-releases.md` | gh CLI 与 PR/Issue | 按需 |

**禁止**：写章节正文时读 `theme/css/*`；查 build 产物；为「了解一下」而整包读 references。
