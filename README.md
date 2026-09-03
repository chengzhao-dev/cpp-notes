# cpp-notes

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

**C++ 笔记**——基于 [Quarto Book](https://quarto.org/docs/books/) 的中文 C++ 教程，体例参考 [LearnCpp.com](https://www.learncpp.com/)，布局参考 [Cursor 文档](https://cursor.com/cn/docs)。在线阅读：<https://chengzhao-dev.github.io/cpp-notes/>。

## 环境

Linux / WSL2（g++、CMake）。示例在 `code/`；新建工程：

```bash
python scripts/cpp/init_project.py --name <name> --dir code/<part>
```

编辑器配置已放在仓库根：`.editorconfig`（换行/缩进）、`.clang-format`（排版）、
`.clangd` + `.vscode/`（WSL 下的补全与保存即格式化）。示例跑一次
`bash code/<part>/<chapter>/build-and-run.sh` 即生成 clangd 用的编译数据库。

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
├── scripts/          # Python 工具（cpp/ build/ maint/ agent/ config/）
├── docs/             # 框架与任务清单（见 docs/structure.md）
└── .cursor/skills/   # Agent 规范（见 AGENTS.md）
```

## 发布

推送到 `main` 后，GitHub Actions 渲染 Book，并把 `_book/` 推到 `gh-pages` 分支（Pages：Deploy from a branch → `gh-pages` / `(root)`）。

目录职责与内容路线图的**单一真源**是 [`docs/structure.md`](docs/structure.md)；
上方结构树只是速览。Agent 协作规范见 [`AGENTS.md`](AGENTS.md)。

## 内容规划

`getting-started` → `core` → `stl` → `memory` → `performance` → `debugging` → `toolchain` → 速查表。详见 [`docs/structure.md`](docs/structure.md)。
