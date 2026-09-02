# cpp-notes

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

**C++ 笔记**——基于 [Quarto Book](https://quarto.org/docs/books/) 的中文 C++ 教程，体例参考 [LearnCpp.com](https://www.learncpp.com/)，布局参考 [Cursor 文档](https://cursor.com/cn/docs)。在线阅读：<https://chengzhao-dev.github.io/cpp-notes/>。

## 环境

Linux / WSL2（g++、CMake）。示例在 `code/`；新建工程：

```bash
python scripts/cpp/init_project.py --name <name> --dir code/<part>
```

## 本地渲染

```bash
quarto render
quarto preview
```

排错见 [`docs/agent/render-ops.md`](docs/agent/render-ops.md)。

## 结构

```
├── content/          # 章节
├── code/             # 示例
├── theme/            # HTML 主题
├── scripts/          # Python 工具（cpp/ build/ maint/ config/）
├── docs/             # 框架与任务清单（见 docs/structure.md）
└── .cursor/skills/   # Agent 规范（见 AGENTS.md）
```

## 发布

推送到 `main` 后由 GitHub Actions 渲染并发布 Pages。

## 内容规划

`environment` → `core` → `stl` → `memory` → `performance` → `debugging` → `toolchain` → 速查表。详见 [`docs/structure.md`](docs/structure.md)。
