# cpp-notes

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

**C++ 笔记**是一份基于 [Quarto Book](https://quarto.org/docs/books/) 的中文 C++ 教程。内容参考 [LearnCpp.com](https://www.learncpp.com/)，页面布局参考 [Cursor 文档](https://cursor.com/cn/docs)。[在线阅读](https://chengzhao-dev.github.io/cpp-notes/)。

## 环境

Windows 负责宿主系统和图形界面，WSL2 提供 Ubuntu 开发环境；工具链使用 g++、clangd 和 CMake。仓库工具要求 Python 3.12。示例在 `code/`；新建一个可直接构建的章节工程：

Windows 下使用仓库配置的 Python 3.12：

```powershell
D:/ProgramData/miniforge3/python.exe D:/Github/cpp-notes/scripts/cpp/init_project.py `
  --name first-program `
  --dir D:/Github/cpp-notes/code/getting-started
```

脚本会自动创建 `D:/Github/cpp-notes/code/getting-started/first-program`，其中 `--dir` 是父目录，`--name` 是最终项目目录名。脚手架从 `.config/cpp/` 读取配置；C++ 与 CMake 示例统一使用 2 空格缩进。

生成后运行 `D:/ProgramData/miniforge3/python.exe scripts/agent/run.py build getting-started/first-program`。Windows 会按需调用默认 WSL2 Ubuntu，完成配置、构建和运行，并生成 clangd 使用的编译数据库。仓库根目录已正确配置 Python 时，也可以使用 `python scripts/cpp/init_project.py --name <name> --dir code/<part>`。

## 本地渲染

```bash
quarto render
quarto preview
```

排错见 [`docs/agent/ops.md`](docs/agent/ops.md)。

## 结构

```
├── content/          # 章节
├── code/             # 示例
├── theme/            # HTML 主题
├── scripts/          # Python 工具（cpp/ build/ maint/ agent/）
├── docs/             # 框架与任务清单（见 docs/structure.md）
├── .config/          # C++ 与仓库工具配置
└── .cursor/skills/   # Agent 规范（见 AGENTS.md）
```

## 发布

推送到 `main` 后，GitHub Actions 渲染 Book，并把 `_book/` 推到 `gh-pages` 分支（Pages：Deploy from a branch → `gh-pages` / `(root)`）。

目录职责与内容路线图的**单一真源**是 [`docs/structure.md`](docs/structure.md)；
上方结构树只是速览。Agent 协作规范见 [`AGENTS.md`](AGENTS.md)。

## 内容规划

`getting-started` → `core` → `stl` → `memory` → `performance` → `debugging` → `toolchain` → 速查表。详见 [`docs/structure.md`](docs/structure.md)。
