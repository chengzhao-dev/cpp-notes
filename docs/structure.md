# cpp-notes 项目框架

Quarto Book 中文 C++ 教程。阅读体例参考 [LearnCpp.com](https://www.learncpp.com/)，HTML 布局参考 [Cursor 文档](https://cursor.com/cn/docs)。

## 根目录职责

| 路径 | 职责 |
|---|---|
| `_quarto.yml` / `index.qmd` | Quarto Book 配置与首页（必须在根） |
| `content/` | 章节 `.qmd`，按 part 分子目录 |
| `code/` | 示例源码，目录名与 `content/` part 对齐；单文件 `code/<part>/<name>.cpp`，需构建工程的章用 `code/<part>/<chapter>/`（其 `build/` 为产物，不入库、不读、不校验） |
| `theme/` | 明暗 SCSS + 按域 CSS + includes + 自托管字体 |
| `.config/` | C++ 工程配置源与仓库工具配置 |
| `scripts/` | 仓库级 Python（见下表） |
| `docs/` | 项目元信息、任务清单、Agent 运维细则 |
| `.cursor/skills/` | Cursor 项目 skills |

### scripts/ 子目录

| 路径 | 用途 |
|---|---|
| `scripts/cpp/` | C++ 工程脚手架与基础工程模板（`init_project.py` + `templates/`）；`code/` 下默认生成完整工程 |
| `scripts/build/` | 渲染后处理（`defer-mermaid.py`） |
| `scripts/maint/` | 文档与站点资产维护（`gen_tasks.py`、`gen_favicon.py`） |
| `scripts/agent/` | Agent 侧工具：`run.py` 统一入口、`scope.py` 作用域解析、`check_dom_contracts.py` 产物契约、`check_skill_size.py` 体积护栏 |

## Skill 与脚本分工

| 类型 | 位置 | 示例 |
|---|---|---|
| 可执行脚手架 / 校验 | `scripts/` 或 skill 内 `scripts/` | `init_project.py`、`verify_examples.py`、`check_callouts.py` |
| 写作 / 领域规范 | `.cursor/skills/*/references/` | `writing-style-core.md`、`code-style.md` |
| 任务清单 | `docs/tasks/` | `INDEX.md`、各章任务单文件（已完成任务归档在 `infra/DONE.md`） |
| Python 格式 | `.config/python/pyproject.toml` + `docs/agent/ops.md` | Black 格式化 |

**不做 skill 的重复**：C++ 工程脚手架只用 `scripts/cpp/init_project.py`，不建 `cpp-project` skill。

## 内容路线图

渐进式 part（每章对应 `docs/tasks/content/<part>/<chapter>.md` 一个任务）：

| Part | 章节 |
|---|---|
| **getting-started** | `setup-wsl2`✅、`first-program`✅、`cmake-intro`（`install-toolchain` 已并入 `setup-wsl2` 的「安装 C++ 构建工具链」节，不再单列成章） |
| **core** | `intro`、`variables`、`operators`、`control-flow`、`functions`、`arrays-strings`、`structs-classes`、`references` |
| **stl** | `intro-stl`、`vector`、`map-set`、`iterators`、`algorithms` |
| **memory** | `stack-heap`、`raii`、`smart-pointers`、`move-semantics` |
| **performance** | `profiling`、`cache-locality`、`rvo-nrvo` |
| **debugging** | `gdb-basics`、`sanitizers`、`common-bugs` |
| **toolchain** | `cmake-targets`、`clang-tools`、`project-layout` |
| **cheatsheet** | `syntax-ref`、`stl-ref` |

目录对齐：`content/<part>/` ↔ `code/<part>/` ↔ `docs/tasks/content/<part>/`。

## 章节体量预算

| 类型 | 目标行数 | 结构上限 |
|---|---|---|
| 环境/安装章 | 120–180 | 引言 2 句 · 目标 ≤4 · mermaid 0–1 · 步骤 H3 ≤5 · FAQ ≤3 |
| 语言概念章 | 100–150 | 动机 1 段 · 代码 1–2 块 · callout 0–1 · FAQ ≤2 |
| 进阶/迁移 | 独立章 | 不进主线章（如 WSL 磁盘迁移） |

**清晰优先于行数**：在句子中说明完整，不为达标堆叠小节（见 `writing-style-core.md`「新手可读性」）。

## Agent 写单章工作流

1. 读 `docs/tasks/content/<part>/<chapter>.md` 读写边界
2. `python .cursor/skills/cpp-content/scripts/scaffold_chapter.py --topic … --part …`
3. 扩写 `.qmd`（`authoring.md` + `writing-style-core.md`）
4. 写 `code/<part>/*.cpp`，跑 `verify_examples.py`
5. `_quarto.yml` 注册；更新 part 索引页与 `docs/tasks/INDEX.md`

## 扩展文档

- 渲染与脚本运维：`docs/agent/ops.md`
- 上下文预算与省 token 实测：`docs/agent/context-budget.md`
- 任务作用域怎么定：`python scripts/agent/run.py scope <part>/<chapter>`
- Python 脚本规范：`docs/agent/ops.md`
- 任务总表：`docs/tasks/INDEX.md`
