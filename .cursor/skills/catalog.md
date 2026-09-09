# Skills 目录索引

本文件是 skill 与 reference 的全景路由表：一次看清「有什么、管什么、何时读」。行数与字符上限由
`.cursor/skills/agent-ops/scripts/check_skill_size.py` 强制（L1 `SKILL.md` ≤45 行 / ≤3000 字符，
L2 `references/**/*.md` ≤160 行 / ≤6000 字符，全部 `name + description` ≤8000 字符）。

## skill 与 knowledge 的分工

同一个知识点只允许有一个出处：怎么做（流程、格式约定、硬约束）留 `references/`；为什么（领域结论与取舍依据）进
`knowledge/`。`references/` 需要领域依据时只写一行检索入口
（`python .cursor/skills/agent-ops/scripts/run.py kb-search "<查询>" --domain <domain>`），不复制正文。

新增或迁移 `knowledge/` 文件后必须跑 `run.py kb-index` 与 `run.py kb-check`；`kb-eval` 负责召回率与 Token 预算验收。
索引产物在 `temp/knowledge-index/`（已 gitignore），缺失时子命令自动重建。

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
| `code-review/references/review-checklists.md` | C++ 代码与文档两份审查清单 | 执行只读审查时按对象取用 |
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
| `quarto-docs/references/zh/writing-style-core.md` | 通用章节组织与展示 | 写改任何正文 |
| `quarto-docs/references/zh/cpp-chapter-writing.md` | C++ 教学章节专项规则 | C++ 章节与示例 |
| `quarto-docs/references/zh/chinese-review-routing.md` | 句式与措辞案例的知识库路由 | 段落衔接、长句或措辞润色 |
| `quarto-docs/references/quarto/authoring.md` | 正文结构、文档元素、代码块与交叉引用 | 写改任何 `.qmd` 正文 |
| `quarto-docs/references/quarto/terminal-validation.md` | 命令块、实测输出与安装验证边界 | 展示 Ubuntu/WSL 命令或排查步骤 |
| `quarto-docs/references/quarto/basics.md` | Book 结构、front matter、标题层级（规范唯一出处） | 改 `_quarto.yml` 或章节骨架 |
| `quarto-docs/references/quarto/rendering-and-output.md` | HTML 现行取值、改动约定与编号陷阱索引 | 调 format/html 选项或渲染异常排错 |
| `quarto-theme/references/theme-system.md` | 设计令牌、主题文件结构、组件规则与新增流程 | 改 `assets/theme/**` 任何文件 |

## knowledge 领域依据（回答「为什么」）

| 文件 | domain | 管什么 |
|---|---|---|
| `knowledge/README.md` | — | 知识库规范、检索不变量与新增知识闭环；新建或迁移知识文件前必读 |
| `knowledge/agent-ops/codex-context-compaction.md` | `agent-ops` | 宿主上下文压缩对长任务的影响与应对契约 |
| `knowledge/cpp-content/toolchain/build-toolchain.md` | `cpp-content` | 构建工具链选型与版本决策依据 |
| `knowledge/github-ops/github-pages-deployment.md` | `github-ops` | Pages 部署方式与分支策略依据 |
| `knowledge/github-ops/repository-hygiene.md` | `github-ops` | 仓库一致性与忽略规则依据 |
| `knowledge/quarto-docs/output/html-output.md` | `quarto-docs` | Quarto HTML 输出选项与生效边界 |
| `knowledge/quarto-docs/rendering/rendering-constraints.md` | `quarto-docs` | Quarto 渲染行为与失效模式依据 |
| `knowledge/quarto-docs/writing/chinese-style-cases.md` | `quarto-docs` | 中文段落、句式与措辞案例 |
| `knowledge/quarto-docs/writing/chapter-and-environment-cases.md` | `quarto-docs` | 章节、环境与命令展示案例 |

**禁止**：写正文时读 `quarto-theme/assets/theme/css/*`；查 `build/` 产物；为「了解一下」整包读
`references/`；把宿主个性化说明（用户全局配置里的六项原则，仓库内不存在该文件）列为阅读项。