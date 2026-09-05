# AGENTS.md

**C++ 笔记** Quarto Book：面向新手的 Linux C++ 渐进式中文教程。目录职责与内容路线图见 [`handbook/repository-structure.md`](handbook/repository-structure.md)。

## 上下文纪律（每次任务先照此办）

1. 先跑一次 `python scripts/agent/run.py scope <part>/<chapter>`（或 `theme` / `dev` / `repo`），**只读**它列出的 UNIT + READ；DENY 内的文件不读、不检索、不索引。
2. `_book/**`、`code/**/build/**`、`.quarto/**` 永不入上下文：`build/` 里的 CMake 生成物（`CMakeCXXCompilerId.cpp` 等）含 `int main`，误读会污染示例校验与写作判断。三层拦截：`.gitignore` + `.cursorignore`/`.cursorindexingignore`（访问与索引）+ `verify_examples.py` 的 `SKIP_DIRS` 剪枝。产物检查走 `run.py check`（脚本内部读大文件，只回一行结论）。
3. 诊断逃生舱：只有当某项 check 报 FAIL 需定位、或出现断言未覆盖的新症状时，才允许真读产物，且先一句声明理由；查明后把结论回写成 `check_dom_contracts.py` 的一条断言（经验只沉淀一次）。
4. 子代理阈值：预计要读 >8 个文件、或需全仓检索时，派 sub-agent 侦察并只回一段摘要；≤3 个文件本地直读更省。编辑类任务不派（改动须回主线程）。
5. 一次任务只读路由指向的那一个 reference；跨章引用只写 `@sec-` 锚点，不去读对方正文。
6. 改 `theme/**` 或 `_quarto.yml` 会触发整本重渲染：先声明代价，再 `run.py render`，之后只看校验结果、不回读 HTML。

## Skill 路由

| 领域 | Skill |
|---|---|
| 写作 / qmd / 中文润色 | `quarto-docs` |
| C++ 内容、示例、工具链 | `cpp-content` |
| HTML 主题与设计令牌 | `quarto-theme` |
| Git / Actions / Pages（未明确要求不 commit/push） | `github-ops` |

全部 reference 的「管什么 · 何时读」：`.cursor/skills/_CATALOG.md`；改 skill 先读 `skill-maintenance`；按章任务与读写边界：`handbook/tasks/INDEX.md`。

## 命令（统一经 run.py，避免 PowerShell 引号与 GBK 反复重试）

| 命令 | 用途 |
|---|---|
| `run.py check` | 一次跑完 layout / callouts / dom / ascii / links / size |
| `run.py render` | 渲染 Book 并自动跑 check |
| `run.py verify [--changed] [--style]` | 编译校验 C++ 示例；`--changed` 只校验改动内容，规则变更自动回退全量（Windows 按需启动 WSL） |
| `run.py build <part>/<chapter>` | 在 WSL 中按需构建示例，顺带生成 clangd 编译数据库 |
| `run.py scope <目标>` / `run.py status` | 作用域清单 / 精简 git 状态 |

排错细则见 [`handbook/operations/agent-operations.md`](handbook/operations/agent-operations.md)。
格式：Python ≥3.12 仅标准库，解释器见 runtime 配置；文本 LF、UTF-8 无 BOM；C++ 与 CMake 统一 2 空格。
中文文件禁止使用系统代码页或 GBK 读写；修改 `.qmd`、Skill 或主题 CSS 后先运行 `check_encoding.py`，再运行 `run.py check` 或 `render`。代码块和终端 transcript 使用 GitHub 明暗色板、等宽字体并左对齐；短命令写正文，连续命令用代码块，注释放在命令上方。Windows 下 Python 使用配置的 3.12 解释器；C++ 校验由 `run.py` 经 WSL 执行，默认只输出结论，失败时再用 `--verbose`。
