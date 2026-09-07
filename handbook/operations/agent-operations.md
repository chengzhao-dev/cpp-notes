# Agent 运维细则

本文件集中记录 Agent 侧的渲染、脚本、校验和维护细则。日常命令见根 [`AGENTS.md`](../../AGENTS.md)。

## 渲染与预览

- 改 `theme/scss/`、`theme/css/` 或 `theme/includes/fonts.html` 会触发整本重渲染（明暗两套 SASS 各编译一次）。
- 日常查看优先 `python .cursor/tools/run.py render`（内部 `quarto render` + 自动校验），只有需要热更新时才开 `quarto preview`。
- **不要每次 preview 都清缓存**；下面「彻底清缓存」只在改完主题/`_quarto.yml` 后样式仍不生效时才用。
- `_book/`、`.quarto/` 是生成产物，不手动编辑、也不读进上下文（用 `check_dom_contracts.py` 验结构）。
- mermaid 懒加载：`handbook/scripts/build/defer-mermaid.py` 在 CI 渲染后执行，本地 `run.py render` 不自动跑。

### preview 在 Windows 上卡死

```powershell
Get-Process quarto,deno -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item -LiteralPath .quarto -Recurse -Force
quarto preview
```

### 改 _quarto.yml 主题后样式不生效

SASS 缓存落在 `.quarto/` 与全局目录：

```powershell
Get-Process quarto,deno -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item -LiteralPath .quarto -Recurse -Force
Remove-Item -LiteralPath $env:LOCALAPPDATA\quarto -Recurse -Force
Remove-Item -LiteralPath $env:USERPROFILE\.cache\quarto -Recurse -Force
quarto render --to html
```

### 校验 grid 布局是否生效

不要对压缩 CSS 做宽模式全串扫描。跑 `python .cursor/tools/run.py check`（含 layout 项），
或直接用 `check_layout.py`（单次字面匹配，不做全量正则）。

## 产物契约（改 DOM/主题前后都要跑）

`.cursor/tools/check_dom_contracts.py` 固化了四条历史契约：复制按钮 hover（兄弟 DOM + scaffold 选择器）、
触屏无 hover 兜底、打印不隐藏 `.code-copy-outer-scaffold`、favicon 已注入并发布。
Quarto 升级最常破的就是这几条。破了就 FAIL 并给修复方向；`--verbose` 展开。

## Python 工具脚本

均为 Python ≥ 3.12，**运行时仅用标准库**。格式用 Black（见 `.config/python/pyproject.toml`）。日常命令统一使用 `python scripts/...`，不把个人电脑上的绝对解释器路径写入文档。

| 路径 | 用途 |
|---|---|
| `handbook/scripts/cpp/` | C++ 工程脚手架与基础工程模板（`init_project.py` + `templates/`） |
| `handbook/scripts/build/` | 渲染后处理（`defer-mermaid.py`） |
| `handbook/scripts/maint/` | 文档与站点资产维护（`gen_tasks.py`、`gen_favicon.py`） |
| `.cursor/tools/` | Agent 侧工具：`run.py`（统一入口）、`scope.py`（作用域）、`check_dom_contracts.py`、`check_skill_size.py` |
| `.config/cpp/` | C++ 工程配置源（由 `init_project.py` 复制到新工程） |
| `.config/python/` | Python 项目配置与本机解释器（`runtime.json` 不入库） |
| `.config/python/` | Python 项目配置与运行时说明 |
| `.cursor/skills/*/scripts/` | 领域校验：编译、脚手架、链接检查等 |

**新建脚手架/校验 → 写 Python 脚本，不新建 skill。**

### Skill 维护与体量控制

修改 `.cursor/skills/` 前先读取 `skill-maintenance`。L1 `SKILL.md` 只保留任务路由和关键约束；L2 reference 只承载一个主题的按需知识。先运行 `check_skill_size.py --verbose`，再搜索已有相近规则。

新规则优先合并到职责匹配的现有文件，并删除重复表述。若仍超出 L1/L2 预算，先压缩措辞、合并相关主题和移除一次性案例；精简后仍超出时，同一 skill 新增独立主题的 L2 reference。只有出现独立任务领域和独立触发条件时，才创建新的 L1 skill。

Shell 脚本内的普通变量使用小写下划线（`project_dir`、`build_dir`、`target`）；只有真正需要导出的全局配置才使用大写下划线常量。C++ 与 Python 沿用各自既有规范，见 `code-style.md` 与 `.config/python/pyproject.toml`。

构建脚本用文件头注释集中解释三条关键命令——`g++ -std=c++20 -Wall -Wextra -Werror main.cpp -o build/bin/app`、`cmake -G Ninja -B build -DCMAKE_BUILD_TYPE=Debug`、`cmake --build build`；`cd`、`./app`、`--version` 一类简单命令不单独解释。

每条规则只保留一个权威出处，不为单次案例创建通用规则。新增或拆分后同步更新父级 `SKILL.md`、`.cursor/skills/_CATALOG.md` 和路由说明，并运行体量、编码、仓库检查及 `git diff --check`。

重构文档、代码或 skill 时，先阅读原文件、相关引用和任务边界，再在原内容上局部调整。除非用户明确要求，或原结构确实无法安全修复，不直接删除后重新生成。需要改名、提取或拆分时，先比较新旧文件的职责和关联，完成后从整体检查术语、链接、顺序和重复内容。目录、文件名、版本号和命令输出可通过磁盘或环境获得时，先实际获取；无法确认的内容只写检查方法，不伪造结果。

### 解释器与外部工具选择

仓库脚本要求 Python 3.12 或更高版本，运行时只依赖标准库。解释器按以下顺序选择：环境变量 `CPP_MEMO_PYTHON`、`.config/python/runtime.json`、PATH 中自动搜索的符合版本要求的解释器，最后使用当前可执行解释器；`run.py` 会拒绝低于 Python 3.12 的解释器。

外部工具遵循同一协议：环境变量 `CPP_MEMO_<TOOL>` 优先，其次读取运行时配置，最后用 PATH 搜索；找不到时立即失败并说明工具名和配置变量。文档和 skills 统一使用 `python scripts/...`，这样命令不绑定某台电脑的安装位置；不要把个人绝对路径写回仓库。
本仓库工具脚本自身要打印中文，故 Windows 上建议设 `$env:PYTHONIOENCODING='utf-8'`，否则 PowerShell 的 GBK 控制台会把中文打成乱码。

中文源文件必须以 UTF-8 无 BOM、LF 保存。禁止使用系统代码页或 GBK 读取后回写；PowerShell 5.1 写文件应改用 Python `encoding="utf-8"` 或显式 `UTF8Encoding($false)`。修改 `.qmd`、Skill 文档或主题 CSS 后先运行 `python .cursor/tools/check_encoding.py`，检查失败时从 Git 可读版本恢复并重新应用补丁。

代码块统一左对齐并保留源码缩进；表格负责字段对齐。正文中的冒号只作简短引出，短命令直接放入正文；代码块注释必须简短，并放在对应代码行上方。

### Black（可选本地工具，非 CI 门槛）

PowerShell 不会展开 `.cursor/skills/*/scripts/` 这类通配路径，需显式列出目录：

```powershell
$dirs = @("scripts", ".cursor/skills/cpp-content/scripts",
          ".cursor/skills/quarto-docs/scripts", ".cursor/skills/quarto-theme/scripts")
& $py -m black --config .config/python/pyproject.toml $dirs
& $py -m black --check --config .config/python/pyproject.toml $dirs
```

文档中的一两条短命令直接写入正文；需要顺序或用途说明的连续命令才使用代码块。Linux/WSL 命令使用 `bash`，用户输入行以 `$ `开头；PowerShell 使用 `powershell`，不使用 `$ `提示符；C++ 和 CMake 分别使用 `cpp`、`cmake`。注释放在对应行上方，并使用该语言的原生注释语法。真实输出使用紧跟命令块的 `text` 块；代码块之间保留一个空行。

代码块的背景、边框、字体和间距统一使用 GitHub Light / GitHub Dark 令牌。`text` 关闭语法高亮，只承担目录树或命令输出展示；不要使用 CSS 按命令名、括号或 `$` 位置强制改色。

### 临时文件治理

`.tmp/`、`.cache/`、Python 测试缓存和覆盖率产物均为本地生成物，已由根 `.gitignore` 统一排除。发现新的工具缓存时，先确认它不属于源码或配置，再补充对应忽略规则；不要把个人机器路径写入仓库。

### 中文注释约定（与 C++ 示例同一套排版理念）

| 位置 | 要求 |
|---|---|
| 模块 `"""…"""` | 中文：做什么、用法一行、退出码 |
| `argparse` help | 中文 |
| 用户可见 `print` | 中文；默认 terse，完整诊断藏在 `--verbose` |
| 行内 `#` | 写在被说明代码的**上一行**；仅记非显然逻辑（协议分支、WSL 路径、幂等等） |
| 逻辑块之间 | 空一行，别把不同步骤挤在一起 |

**禁止**：逐行翻译式注释、大段英文 docstring、重复模块说明。

### 新脚本 Checklist

- [ ] 放对目录（`scripts/<域>/` 或 skill `scripts/`）
- [ ] 中文模块 docstring + 中文 argparse help
- [ ] 仅标准库依赖；默认输出 ≤1 行结论
- [ ] 在 `handbook/repository-structure.md` 或对应 skill 中登记用途

## goal 模式下的上下文管理

仅适用于 goal 模式（自动跨轮推进同一个目标）。plan 与 build 模式由用户逐轮驱动，不需要主动压缩。

1. 目标跨轮持续，故每轮只推进一个可验证的子目标，收尾时把状态写进 `git status` 可见的文件，不靠对话记忆交接。
2. 上下文明显吃紧（约 70%–80%）时先压缩上下文再继续，不要压到接近上限才处理，否则当轮就可能中断。
3. 压缩会丢弃早期工具输出，因此压缩后立即重读 `run.py scope <目标>` 与必要产物，确认文件边界和已完成项，再继续编辑。
4. 可复现的事实（版本号、目录结构、链接可达性）在需要时重新实测，不从摘要里的旧结论取值。
5. 每轮结束前用一次 `run.py check` 收口，避免把未验证的中间态留给下一轮。

## 开发环境配置

仓库根仅保留 `.editorconfig`；C++ 配置源使用工具约定的 `.config/cpp/.clang-format`、`.config/cpp/.clangd`、`.config/cpp/.clang-tidy`、`.config/cpp/.vscode/`。
配置源统一位于 `.config/cpp/`，由 `init_project.py` 复制到新工程；
`bare`、`simple` 与 `complete` 布局都会生成这些配置，`--no-clang` 可关闭生成；其中 `complete` 还会生成一键构建脚本。

`build-and-run.sh` 里的 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` 生成 `build/compile_commands.json`，
clangd 会逐级向上查找并自动进入 `build/`；未构建过的文件由项目 `.clangd` 的兜底参数接管。

Windows 下 `run.py verify` 和 `run.py build` 会调用 `wsl.exe`，按需启动默认 WSL2 Ubuntu，在其中执行编译器和 CMake。默认只返回精简结论；仅在失败排查时使用 `--verbose`，避免将完整编译流水带入上下文。

日常修改使用 `.cursor/tools/run.py verify --changed`。它读取工作区、暂存区和未跟踪文件相对 `HEAD` 的路径，只验证修改的 `code/**/*.cpp` 和 `.qmd` 内嵌示例，并跳过 `build/`、`.cache/`、`.tmp/` 和 Python 缓存。修改 `.config/cpp/`、`handbook/scripts/cpp/`、C++ skill 校验脚本或 `run.py` 时，会自动回退全量 C++ 校验；没有相关改动时只输出 `SKIP`。`.cursor/tools/run.py check` 仍是轻量仓库检查，不会因此扫描全部 C++ 示例。

大更新先按逻辑分组，再使用显式路径暂存。文档、工具、主题和配置应尽量形成可独立回滚的提交；提交信息使用 `docs:`、`feat:`、`fix:`、`refactor:` 或 `chore:` 前缀。提交本身不会显著增加 token 消耗，真正昂贵的是全量编译、整本渲染和详细日志回传。
