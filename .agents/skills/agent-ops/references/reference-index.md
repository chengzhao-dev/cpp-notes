# Skills 与 Knowledge 完整索引

只在维护 skills 目录、合并 reference、调整路由或检查覆盖时读取。普通章节和普通 skill 任务按 `SKILL.md` 的局部路由读取目标文件，不加载本索引。

## L2 reference

| 文件 | 管什么 | 何时读 |
| --- | --- | --- |
| `.agents/skills/agent-ops/references/refactor-guidelines.md` | 分层加载、SKILL 骨架和重构纪律 | 新建、合并或删除 skill/reference |
| `.agents/skills/agent-ops/references/repository-structure.md` | 目录职责、章节对齐和生成物边界 | 判断路径归属或读取范围 |
| `.agents/skills/agent-ops/references/plan-artifacts.md` | 计划落盘、来源和完整性 | Plan Mode 结束后的计划文件 |
| `.agents/skills/agent-ops/references/reference-index.md` | 完整 L2 与知识库目录 | 维护 skills 路由和覆盖 |
| `.agents/skills/code-review/references/review-checklists.md` | C++ 与文档审查清单 | 执行只读审查 |
| `.agents/skills/cpp-content/references/cpp/teaching-method.md` | 章节设计、示例递进和资料分工 | 新写或重构章节 |
| `.agents/skills/cpp-content/references/cpp/cpp.md` | 语言基础、术语、标准版本 | language-basics 或标准语义 |
| `.agents/skills/cpp-content/references/cpp/stl.md` | 容器、迭代器和算法 | standard-library 与 reference |
| `.agents/skills/cpp-content/references/cpp/modern-cpp.md` | RAII、智能指针、移动和模板 | memory 与进阶内容 |
| `.agents/skills/cpp-content/references/cpp/performance-and-pitfalls.md` | 性能、剖析、常见 bug 与 UB | performance 和 debugging |
| `.agents/skills/cpp-content/references/cpp/engineering.md` | 工程、构建和项目布局 | 工具链与工程章节 |
| `.agents/skills/cpp-content/references/cpp/cmake-teaching.md` | CMake 目标导向的教学顺序 | CMake 与工程章节 |
| `.agents/skills/cpp-content/references/cpp/code-style.md` | 命名、文件与目标注释、格式工具 | 写示例或运行风格检查 |
| `.agents/skills/cpp-content/references/cpp/effective-rules.md` | 规则建议、理由和边界 | 写设计建议 |
| `.agents/skills/cpp-content/references/cpp/examples-practice.md` | 示例、错误对照和练习 | 添加示例或练习 |
| `.agents/skills/cpp-content/references/tasks/getting-started.md` | 章节任务、读写边界和验收 | 写任一章前 |
| `.agents/skills/github-ops/references/git-workflow.md` | git 操作和硬约束 | 任何 git 操作 |
| `.agents/skills/github-ops/references/github-pages.md` | Pages 发布与排错 | 发布和部署 |
| `.agents/skills/github-ops/references/ci.md` | Actions 工作流 | 修改 `.github/workflows/*` |
| `.agents/skills/github-ops/references/pr-and-cli.md` | gh、PR 和 Issue 流程 | 建 PR 或发版 |
| `.agents/skills/quarto-docs/references/zh/writing-principles.md` | 中文技术文档九项原则 | 所有中文文档任务 |
| `.agents/skills/quarto-docs/references/zh/chapter-writing.md` | C++ 学习轨迹笔记页面骨架、术语和新手路径 | 写改正文 |
| `.agents/skills/quarto-docs/references/zh/writing-style-core.md` | 旧链接兼容，内容已合并 | 仅旧引用 |
| `.agents/skills/quarto-docs/references/zh/cpp-chapter-writing.md` | 旧链接兼容，内容已合并 | 仅旧引用 |
| `.agents/skills/quarto-docs/references/zh/cpp-notes-writing.md` | 旧链接兼容，内容已合并 | 仅旧引用 |
| `.agents/skills/quarto-docs/references/zh/section-focus-and-density.md` | 小节主线、段落和提示密度 | 重排正文 |
| `.agents/skills/quarto-docs/references/zh/project-tree-and-diagram-focus.md` | 目录树和 Mermaid 主线 | 展示工程结构或图表 |
| `.agents/skills/quarto-docs/references/zh/chinese-review-routing.md` | 中文句式与措辞检索入口 | 润色措辞 |
| `.agents/skills/quarto-docs/references/quarto/authoring.md` | QMD 结构、代码来源、链接和答案 | 写改 QMD |
| `.agents/skills/quarto-docs/references/quarto/terminal-validation.md` | 命令、输出、诊断和验证回流 | 写终端步骤 |
| `.agents/skills/quarto-docs/references/quarto/basics.md` | Book 结构、front matter 和标题层级 | 改 `_quarto.yml` 或骨架 |
| `.agents/skills/quarto-docs/references/quarto/rendering-and-output.md` | HTML 取值、三栏预算和渲染排错 | 调格式或排错 |
| `.agents/skills/quarto-theme/references/theme-system.md` | 设计令牌、字体、布局和组件 | 修改主题资源 |

## Knowledge

| 文件 | 覆盖内容 |
| --- | --- |
| `knowledge/agent-ops/codex-context-compaction.md` | 上下文压缩 |
| `knowledge/agent-ops/context-budget-governance.md` | 分层预算 |
| `knowledge/agent-ops/plan-artifact-source.md` | 计划来源 |
| `knowledge/agent-ops/repository-navigation.md` | 仓库导航 |
| `knowledge/cpp-content/style/naming-format.md` | 命名格式 |
| `knowledge/cpp-content/style/teaching-source-comments.md` | 源码与目标注释 |
| `knowledge/cpp-content/toolchain/build-toolchain.md` | 构建链 |
| `knowledge/cpp-content/toolchain/library-and-executable-linking.md` | 库链接与 Android 交付背景 |
| `knowledge/github-ops/github-pages-deployment.md` | Pages 部署 |
| `knowledge/github-ops/repository-hygiene.md` | 仓库卫生 |
| `knowledge/quarto-docs/output/html-output.md` | HTML 输出 |
| `knowledge/quarto-docs/rendering/rendering-constraints.md` | 渲染约束 |
| `knowledge/quarto-docs/writing/chapter-and-environment-cases.md` | 环境页案例 |
| `knowledge/quarto-docs/writing/chapter-page-pattern.md` | 页面模式 |
| `knowledge/quarto-docs/writing/chinese-style-cases.md` | 中文案例 |
| `knowledge/quarto-docs/writing/inline-code-boundaries.md` | 行内代码边界 |
| `knowledge/quarto-docs/writing/landing-page-pattern.md` | 入口页模式 |
| `knowledge/quarto-docs/writing/project-tree-and-diagram-focus.md` | 目录树边界 |
| `knowledge/quarto-docs/writing/section-focus-and-density.md` | 段落密度 |
| `knowledge/quarto-docs/writing/troubleshooting-flow-pattern.md` | 排错流程 |

`knowledge/README.md` 是知识库规范和新增流程入口。新增或迁移知识后运行 `kb-index`、`kb-check` 和 `kb-eval`。
