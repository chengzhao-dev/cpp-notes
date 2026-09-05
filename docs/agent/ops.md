# Agent 运维细则

由 `ops.md` 与 `ops.md` 合并而来（两者都是 agent 侧细则，分开放会被反复成对读取）。日常命令见根 [`AGENTS.md`](../../AGENTS.md)。

## 渲染与预览

- 改 `theme/scss/`、`theme/css/` 或 `theme/includes/fonts.html` 会触发整本重渲染（明暗两套 SASS 各编译一次）。
- 日常查看优先 `python scripts/agent/run.py render`（内部 `quarto render` + 自动校验），只有需要热更新时才开 `quarto preview`。
- **不要每次 preview 都清缓存**；下面「彻底清缓存」只在改完主题/`_quarto.yml` 后样式仍不生效时才用。
- `_book/`、`.quarto/` 是生成产物，不手动编辑、也不读进上下文（用 `check_dom_contracts.py` 验结构）。
- mermaid 懒加载：`scripts/build/defer-mermaid.py` 在 CI 渲染后执行，本地 `run.py render` 不自动跑。

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

不要对压缩 CSS 做宽模式全串扫描。跑 `python scripts/agent/run.py check`（含 layout 项），
或直接用 `check_layout.py`（单次字面匹配，不做全量正则）。

## 产物契约（改 DOM/主题前后都要跑）

`scripts/agent/check_dom_contracts.py` 固化了四条历史契约：复制按钮 hover（兄弟 DOM + scaffold 选择器）、
触屏无 hover 兜底、打印不隐藏 `.code-copy-outer-scaffold`、favicon 已注入并发布。
Quarto 升级最常破的就是这几条。破了就 FAIL 并给修复方向；`--verbose` 展开。

## Python 工具脚本

均为 Python ≥ 3.12，**运行时仅用标准库**。格式用 Black（见 `.config/python/pyproject.toml`）。Windows 优先使用 `.config/python/runtime.json` 指定的解释器，例如 `D:/ProgramData/miniforge3/python.exe`；若终端已配置仓库解释器，才使用简写 `python`。

| 路径 | 用途 |
|---|---|
| `scripts/cpp/` | C++ 工程脚手架与基础工程模板（`init_project.py` + `templates/`） |
| `scripts/build/` | 渲染后处理（`defer-mermaid.py`） |
| `scripts/maint/` | 文档与站点资产维护（`gen_tasks.py`、`gen_favicon.py`） |
| `scripts/agent/` | Agent 侧工具：`run.py`（统一入口）、`scope.py`（作用域）、`check_dom_contracts.py`、`check_skill_size.py` |
| `.config/cpp/` | C++ 工程配置源（由 `init_project.py` 复制到新工程） |
| `.config/python/` | Python 项目配置与本机解释器（`runtime.json` 不入库） |
| `.config/python/` | Python 项目配置与运行时说明 |
| `.cursor/skills/*/scripts/` | 领域校验：编译、脚手架、链接检查等 |

**新建脚手架/校验 → 写 Python 脚本，不新建 skill。**

### 解释器

环境变量 `CPP_MEMO_PYTHON` → `.config/python/runtime.json` → 自动搜索（≥3.12）。`run.py` 会拒绝低于 Python 3.12 的解释器。
本仓库工具脚本自身要打印中文，故 Windows 上建议设 `$env:PYTHONIOENCODING='utf-8'`，否则 PowerShell 的 GBK 控制台会把中文打成乱码。

中文源文件必须以 UTF-8 无 BOM、LF 保存。禁止使用系统代码页或 GBK 读取后回写；PowerShell 5.1 写文件应改用 Python `encoding="utf-8"` 或显式 `UTF8Encoding($false)`。修改 `.qmd`、Skill 文档或主题 CSS 后先运行 `python scripts/agent/check_encoding.py`，检查失败时从 Git 可读版本恢复并重新应用补丁。

代码块统一左对齐并保留源码缩进；表格负责字段对齐。正文中的冒号只作简短引出，短命令直接放入正文；代码块注释必须简短，并放在对应代码行上方。

### Black（可选本地工具，非 CI 门槛）

PowerShell 不会展开 `.cursor/skills/*/scripts/` 这类通配路径，需显式列出目录：

```powershell
$dirs = @("scripts", ".cursor/skills/cpp-content/scripts",
          ".cursor/skills/quarto-docs/scripts", ".cursor/skills/quarto-theme/scripts")
& $py -m black --config .config/python/pyproject.toml $dirs
& $py -m black --check --config .config/python/pyproject.toml $dirs
```

文档中的一两条短命令直接写入正文；需要顺序或用途说明的连续命令才使用代码块，并把简短注释放在对应命令上方。代码、命令和 transcript 全部左对齐，transcript 与语言代码块共享字体和布局。

代码块的背景、边框、字体和间距统一使用 GitHub Light / GitHub Dark 令牌。transcript 关闭语法高亮，只承担命令与输出展示；不要使用 CSS 按命令名、括号或 `$` 位置强制改色。

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
- [ ] 在 `docs/structure.md` 或对应 skill 中登记用途

## 开发环境配置

仓库根仅保留 `.editorconfig`；C++ 配置源使用工具约定的 `.config/cpp/.clang-format`、`.config/cpp/.clangd`、`.config/cpp/.clang-tidy`、`.config/cpp/.vscode/`。
配置源统一位于 `.config/cpp/`，由 `init_project.py` 复制到新工程；
`bare`、`simple` 与 `complete` 布局都会生成这些配置，`--no-clang` 可关闭生成；其中 `complete` 还会生成一键构建脚本。

`build-and-run.sh` 里的 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` 生成 `build/compile_commands.json`，
clangd 会逐级向上查找并自动进入 `build/`；未构建过的文件由项目 `.clangd` 的兜底参数接管。

Windows 下 `run.py verify` 和 `run.py build` 会调用 `wsl.exe`，按需启动默认 WSL2 Ubuntu，在其中执行编译器和 CMake。默认只返回精简结论；仅在失败排查时使用 `--verbose`，避免将完整编译流水带入上下文。
