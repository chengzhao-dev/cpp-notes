# Skills 目录索引

本文件是 skill 与 reference 的全景路由表：一次看清「有什么、管什么、何时读」。行数与字符上限由
`.agents/skills/agent-ops/scripts/check_skill_size.py` 强制（L1 `SKILL.md` ≤45 行 / ≤3000 字符，
L2 `references/**/*.md` ≤160 行 / ≤6000 字符，全部 `name + description` ≤8000 字符）。

## skill 与 knowledge 的分工

同一个知识点只允许有一个出处：怎么做（流程、格式约定、硬约束）留 `references/`，为什么（领域结论与取舍依据）进
`knowledge/`。`references/` 优先写稳定 `kb_id`，确需检索时再给一行带 `--domain` 的 `run.ps1 kb-search`
入口，不复制知识正文。

新增或迁移 `knowledge/` 文件后必须跑 `run.py kb-index` 与 `run.py kb-check`。`kb-eval` 负责召回率与 Token 预算验收。
索引产物和其他项目临时文件统一在 `temp/<用途>/`（已 gitignore），缺失时子命令自动重建。`.tmp/` 不再作为生成目录。

## L1 入口（每次只读命中的那一个）

| Skill | 管什么 | 不适用时转交 |
|---|---|---|
| `agent-ops/SKILL.md` | Agent 运行入口、Skills 分层、MCP、仓库重构与统一验收 | 写正文转 `cpp-content`/`quarto-docs`，改样式转 `quarto-theme` |
| `code-review/SKILL.md` | Defect-First 只读审查 C++ 示例与文档 | 需要动手改文件时转对应内容 skill |
| `cpp-content/SKILL.md` | 中文 C++20 教程、示例与练习的正确性与递进 | 页面结构转 `quarto-docs`，样式转 `quarto-theme` |
| `github-ops/SKILL.md` | git 工作流、gh CLI、PR/Issue、Pages 发布与 CI 操作清单 | 正文与 skill 内容改动转对应 skill |
| `python-tools/SKILL.md` | 本仓库 Python 工具、知识库管道、脚手架与运行时选择 | 检查项编排转 `agent-ops`，知识正文转 `knowledge/` |
| `quarto-docs/SKILL.md` | `.qmd` 正文写法、Book 结构、中文技术文档格式 | 渲染参数取值转 `quarto-theme`，C++ 语义转 `cpp-content` |
| `quarto-theme/SKILL.md` | HTML 主题、设计令牌与布局契约 | 正文写法与 `.qmd` 结构转 `quarto-docs` |

## L2 reference（按需读取，禁止整包加载）

| 文件 | 管什么 | 何时读我 |
|---|---|---|
| `agent-ops/references/refactor-guidelines.md` | 三层加载契约、SKILL.md 骨架、重构纪律 | 新建、合并、改名或删除 skill/reference |
| `agent-ops/references/repository-structure.md` | 目录职责、章节对齐、生成物边界、运行入口 | 不确定某个路径归谁、或要判断该读什么 |
| `code-review/references/review-checklists.md` | C++ 代码与文档两份审查清单（含文档删改连续性与 Callout 密度检查） | 执行只读审查时按对象取用 |
| `cpp-content/references/cpp/teaching-method.md` | 章节设计、示例递进与资料分工 | 新写或重构章节 |
| `cpp-content/references/cpp/cpp.md` | 语言基础、术语译名、标准版本与资料交叉校验 | core/getting-started 章，或涉及标准语义 |
| `cpp-content/references/cpp/stl.md` | 容器、迭代器、算法 | stl 与 cheatsheet 章 |
| `cpp-content/references/cpp/modern-cpp.md` | RAII、智能指针、移动语义、模板与泛型 | memory 章与进阶章按需 |
| `cpp-content/references/cpp/performance-and-pitfalls.md` | 缓存局部性、RVO/NRVO、剖析、常见 bug 与 UB | performance 与 debugging 章 |
| `cpp-content/references/cpp/engineering.md` | 工程、构建与项目布局的写作约定与命令块格式 | toolchain/getting-started 工程类章 |
| `cpp-content/references/cpp/cmake-teaching.md` | CMake 目标导向的教学顺序 | 写 CMake 或工程章 |
| `cpp-content/references/cpp/code-style.md` | 命名、注释、留白与格式化工具 | 写示例代码或跑 `verify --style` |
| `cpp-content/references/cpp/effective-rules.md` | 规则型内容的建议、理由与边界 | 写设计建议或最佳实践 |
| `cpp-content/references/cpp/examples-practice.md` | 示例、错误对照与练习闭环 | 添加示例或练习 |
| `cpp-content/references/tasks/<part>.md` | 8 个 part 任务矩阵：一行一章，含读写边界、状态与验收 | 写任一章前（`run.py scope` 会自动列出） |
| `github-ops/references/git-workflow.md` | git 操作清单与硬约束 | 任何 git 操作前 |
| `github-ops/references/github-pages.md` | Pages 发布操作清单与本仓库现行工作流 | 发布排错 |
| `github-ops/references/ci.md` | Actions 工作流现状与改动约定 | 改 `.github/workflows/*` |
| `github-ops/references/pr-and-cli.md` | gh CLI 与 PR/Issue 流程 | 建 PR、处理 Issue 或发版 |
| `quarto-docs/references/zh/writing-principles.md` | 中文技术文档九项总原则与 Checklist | 所有中文文档任务，优先级最高 |
| `quarto-docs/references/zh/writing-style-core.md` | 通用章节主线、父级 H2 与 H2 导语边界、引言衔接、同级标题命名、新手首次成功路径、狭窄表格口径、常见错误与本章回顾分工 | 写改任何正文 |
| `quarto-docs/references/zh/cpp-chapter-writing.md` | 环境章、构建章骨架与 C++ 教学递进（含引言体量、共享环境阶段分层、官方文档边界、换源影响前置、可选发行版分支、拆分接入、三步诊断流与回顾边界） | C++ 章节与示例 |
| `quarto-docs/references/zh/cpp-notes-writing.md` | 项目受众、工具箱边界、章节与示例对齐、可验证性 | C++ Notes 项目正文或说明文档 |
| `quarto-docs/references/zh/section-focus-and-density.md` | 小节主线、父级标题分组、长段合并/拆分、正文与 Callout 重量平衡、提示符分层、结果型 Callout 及预告接力、区块密度与一跳指针 | 重排段落、代码块和参数解释 |
| `quarto-docs/references/zh/project-tree-and-diagram-focus.md` | 工程目录树、真实源码边界与 Mermaid 主线 | 展示项目结构或整理图表邻接内容 |
| `quarto-docs/references/zh/chinese-review-routing.md` | 句式与措辞案例的知识库路由 | 段落衔接、长句或措辞润色 |
| `quarto-docs/references/quarto/authoring.md` | 正文结构、删改后的动作衔接、代码来源标题、引言与提示框边界、可折叠答案、链接间距与交叉引用 | 写改任何 `.qmd` 正文 |
| `quarto-docs/references/quarto/terminal-validation.md` | 命令块、输出到输入的接力、环境状态切换、代码块前标点、总注释与例外、按需保留的成功判据、三步诊断流、诊断步骤标签与验证回流、FAQ 直答边界、修复动作匹配与可核验外部入口 | 展示 Ubuntu/WSL 命令或排错步骤 |
| `quarto-docs/references/quarto/basics.md` | Book 结构、front matter、标题层级（规范唯一出处） | 改 `_quarto.yml` 或章节骨架 |
| `quarto-docs/references/quarto/rendering-and-output.md` | HTML 现行取值、三栏预算、代码标题、改动约定与编号陷阱索引 | 调 format/html 选项或渲染异常排错 |
| `quarto-theme/references/theme-system.md` | 设计令牌、Fixel/LXGW Screen/Bright Code 字体分包、代码后续间距、标题节奏、首页 Hero、主题文件结构、组件规则、可折叠答案与新增流程 | 改 `assets/theme/**` 任何文件 |

## knowledge 领域依据（回答「为什么」）

| 文件 | domain | 管什么 |
|---|---|---|
| `knowledge/README.md` | — | 知识库规范、检索不变量与新增知识闭环。新建或迁移知识文件前必读 |
| `knowledge/agent-ops/codex-context-compaction.md` | `agent-ops` | 宿主上下文压缩对长任务的影响与应对契约 |
| `knowledge/cpp-content/toolchain/build-toolchain.md` | `cpp-content` | 默认 clang++/libc++ + CMake + Ninja 构建链、缓存恢复与版本决策依据 |
| `knowledge/github-ops/github-pages-deployment.md` | `github-ops` | Pages 部署方式与分支策略依据 |
| `knowledge/github-ops/repository-hygiene.md` | `github-ops` | 仓库一致性与忽略规则依据 |
| `knowledge/quarto-docs/output/html-output.md` | `quarto-docs` | Quarto HTML 输出选项与生效边界 |
| `knowledge/quarto-docs/rendering/rendering-constraints.md` | `quarto-docs` | Quarto 渲染行为、840px 三栏预算、字体分包与覆盖范围、列表内代码后续间距、代码来源标题、参考站点分工与首页边界 |
| `knowledge/quarto-docs/writing/chinese-style-cases.md` | `quarto-docs` | 中文段落、标题导语、长段合并/拆分、正文与 Callout 重量平衡、结果型 Callout 及预告接力、块前标点、句式、措辞、直编改写与文件名密度案例 |
| `knowledge/quarto-docs/writing/chapter-and-environment-cases.md` | `quarto-docs` | WSL2 引言体量、父级标题分组、工具链 H3 归组、提示符结果型 Callout 及预告接力、删改后的环境动作衔接、官方文档边界、新手首次成功路径、总注释取舍、换源影响前置、可选发行版分支与命令接力、安装及工程命令案例 |
| `knowledge/quarto-docs/writing/troubleshooting-flow-pattern.md` | `quarto-docs` | 常见错误三级导航、Quarto FAQ 边界、三步诊断流、步骤名加粗、故障引言与验证回流、CMake 缓存排错、命令块边界与故障分支的结构依据 |
| `knowledge/quarto-docs/writing/chapter-page-pattern.md` | `quarto-docs` | 教学正文块序列、环境/构建骨架、成功/失败分支与回顾答案折叠理由 |
| `knowledge/quarto-docs/writing/section-focus-and-density.md` | `quarto-docs` | 教学小节的主线收束、父级标题分组、长段拆分、正文/Callout 重量平衡与结果型 Callout 边界、预告与首句接力 |
| `knowledge/quarto-docs/writing/project-tree-and-diagram-focus.md` | `quarto-docs` | 工程目录树与图表的事实边界 |
| `knowledge/quarto-docs/writing/inline-code-boundaries.md` | `quarto-docs` | 行内代码标记边界与链接间距依据 |
| `knowledge/quarto-docs/writing/landing-page-pattern.md` | `quarto-docs` | 入口与卡片页的三层结构、卡片职责与承诺边界 |

**禁止**：写正文时读 `quarto-theme/assets/theme/css/*`，查 `build/` 产物，为「了解一下」整包读
`references/`。把宿主个性化说明（用户全局配置里的六项原则，仓库内不存在该文件）列为阅读项。
