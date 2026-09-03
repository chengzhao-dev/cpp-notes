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

均为 Python ≥ 3.9，**运行时仅用标准库**。格式用 Black（见 `scripts/pyproject.toml`）。

| 路径 | 用途 |
|---|---|
| `scripts/cpp/` | C++ 工程脚手架（`init_project.py` + `templates/`） |
| `scripts/build/` | 渲染后处理（`defer-mermaid.py`） |
| `scripts/maint/` | 文档与站点资产维护（`gen_tasks.py`、`gen_favicon.py`） |
| `scripts/agent/` | Agent 侧工具：`run.py`（统一入口）、`scope.py`（作用域）、`check_dom_contracts.py`、`check_skill_size.py` |
| `scripts/config/` | 本机解释器（`python.json`，不入库） |
| `.cursor/skills/*/scripts/` | 领域校验：编译、脚手架、链接检查等 |

**新建脚手架/校验 → 写 Python 脚本，不新建 skill。**

### 解释器

`scripts/config/python.json` → 环境变量 `CPP_MEMO_PYTHON` → 自动搜索（≥3.9）。
本仓库工具脚本自身要打印中文，故 Windows 上建议设 `$env:PYTHONIOENCODING='utf-8'`，否则 PowerShell 的 GBK 控制台会把中文打成乱码。

### Black（可选本地工具，非 CI 门槛）

PowerShell 不会展开 `.cursor/skills/*/scripts/` 这类通配路径，需显式列出目录：

```powershell
$dirs = @("scripts", ".cursor/skills/cpp-content/scripts",
          ".cursor/skills/quarto-docs/scripts", ".cursor/skills/quarto-theme/scripts")
& $py -m black --config scripts/pyproject.toml $dirs
& $py -m black --check --config scripts/pyproject.toml $dirs
```

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

仓库根的 `.editorconfig` / `.clang-format` / `.clangd` / `.vscode/` 是**工作区级**配置：
打开仓库即格式化与补全可用，无需先建工程。`scripts/cpp/templates/` 下的同名模板保留，
供 `init_project.py` 复制进**脱离本仓库使用**的独立工程。改排版规则时两处一起改，避免漂移。

`build-and-run.sh` 里的 `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` 生成 `build/compile_commands.json`，
clangd 会逐级向上查找并自动进入 `build/`；未构建过的文件由根 `.clangd` 的兜底参数接管。
