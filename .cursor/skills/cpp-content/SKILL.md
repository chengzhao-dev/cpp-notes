---
name: cpp-content
description: C++ 语言知识、代码风格、可编译示例。涉及 RAII、STL、模板、性能、UB、工具链、章节骨架与 verify_examples 时使用。默认中文。
---

# Skill: cpp-content

C++ 内容专家。默认 C++20、WSL2（g++/clang++）。全景索引见 `../_CATALOG.md`。

## 任务路由

| 任务 | 必读 |
|---|---|
| 写 `<part>/<chapter>` | 该章任务单「必读」指定的那**一个** `references/cpp/<topic>.md`（由 `run.py scope` 给出） |
| 代码风格 / 注释留白 | `references/cpp/code-style.md` |
| 工具链 / 构建 | `references/cpp/toolchain.md` |

**脚本**：`scripts/scaffold_chapter.py`、`scripts/verify_examples.py`（统一经 `run.py verify` 调用）。Windows 下由 `wsl.exe` 按需启动默认 WSL2 Ubuntu；skill 不保持常驻 WSL 会话。
**工程脚手架**：`scripts/cpp/init_project.py`（code/ 下默认 complete，也支持 bare/simple）。`simple` 只生成 CMake 最小工程；需要一键构建和运行时使用 `complete`。

新建章节工程。Windows 使用仓库配置的 Python 3.12：

```powershell
D:/ProgramData/miniforge3/python.exe D:/Github/cpp-notes/scripts/cpp/init_project.py `
  --name first-program `
  --dir D:/Github/cpp-notes/code/getting-started
```

脚本会创建 `D:/Github/cpp-notes/code/getting-started/first-program`，生成 `main.cpp`、`CMakeLists.txt`、`build-and-run.sh`、clangd/clang-format 配置和 VS Code 配置。随后运行 `python scripts/agent/run.py build getting-started/first-program`，或在 WSL2 Ubuntu 中运行 `bash /mnt/d/Github/cpp-notes/code/getting-started/first-program/build-and-run.sh`。

验证约定：修改 C++ 示例后运行一次 `python scripts/agent/run.py verify`；只验证单个章节时使用 `python scripts/agent/run.py build <part>/<chapter>`。默认输出为精简结论，只有失败排查时才追加 `--verbose`，避免把编译流水回传到上下文。

## 核心约定

- `-std=c++20 -Wall -Wextra`；完整示例带 `int main`
- 示例与章节同名对齐：`code/<part>/<name>.cpp` ↔ `content/<part>/`；需要 CMake/一键脚本的章用目录式 `code/<part>/<chapter>/`，构建产物固定落其 `build/`（不入库、**不读**、不校验）
- 只处理 `run.py scope` 给出的那一个单元，其余 `code/**` 不看
- 文件名纯 ASCII；注释写在被说明代码的上一行，逻辑块之间空一行（见 `code-style.md`）

## 草稿 → 章节

1. `run.py scope <part>/<chapter>` 取读写边界
2. `scaffold_chapter.py --topic … --part … --title …`
3. 扩写 qmd + 示例 → `run.py verify`
4. 注册 `_quarto.yml`
