# cpp-notes

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

**C++ 笔记**是一份基于 [Quarto Book](https://quarto.org/docs/books/) 的中文 C++ 教程，面向希望边读边编译的初学者。[在线阅读](https://chengzhao-dev.github.io/cpp-notes/)。教学顺序参考 [LearnCpp.com](https://www.learncpp.com/)，标准语义以 [cppreference](https://en.cppreference.com/w/cpp/language) 等资料交叉核对。

## 从哪里开始

按照下面的顺序阅读，先完成一次可运行的开发闭环，再扩展语言和工程知识：

1. [搭建开发环境](content/getting-started/index.qmd)：配置 WSL2 上的 Ubuntu、VS Code 和 CMake。
2. [写出第一个 C++ 程序](content/getting-started/first-program.qmd)：用 `main.cpp` 完成编译、运行和 CMake 构建。
3. 进入语言基础，再学习标准库、对象管理、调试和性能。

首页负责入口，入门索引负责章节顺序，正文负责一个完整学习任务。仓库结构和章节关系见 [`handbook/repository-structure.md`](handbook/repository-structure.md)。

## 开发环境

Windows 提供图形界面，WSL2 提供 Ubuntu 开发环境；VS Code 用于编辑项目，CMake 负责配置和构建。仓库工具要求 Python 3.12，解释器选择规则见 [`handbook/operations/agent-operations.md`](handbook/operations/agent-operations.md)。示例源码位于 `code/`。

完成环境配置后，在 WSL2 Ubuntu 中进入示例目录，运行 `bash build-and-run.sh` 即可构建并运行当前工程。Windows 下的仓库脚本会按需调用默认 WSL2，不需要手动保持 WSL 会话。

## 本地阅读与校验

```bash
quarto preview
```

修改文档或示例后，优先使用增量 C++ 校验，再运行轻量检查：

```powershell
python scripts/agent/run.py verify --changed
python scripts/agent/run.py check
git diff --check
```

只有修改主题、Quarto 全局配置或需要确认页面布局时，才运行 `run.py render`。详细规则见 [`AGENTS.md`](AGENTS.md) 和 [`handbook/operations/agent-operations.md`](handbook/operations/agent-operations.md)。

本地的 `code/**/build/`、`.cache/`、`.tmp/` 和 `.quarto/` 都是生成物或缓存，不属于教程源码，也不会提交到 Git。

## 仓库结构

```
├── content/          # 章节
├── code/             # 示例
├── theme/            # HTML 主题
├── scripts/          # Python 工具（cpp/ build/ maint/ agent/）
├── handbook/         # 项目说明、任务清单与 Agent 运维规则
├── .config/          # C++ 与仓库工具配置
└── .cursor/skills/   # Agent 规范（见 AGENTS.md）
```

## 修改与提交

大更新先按内容、工具和主题等逻辑分组，再分别暂存和提交。提交信息使用 `docs:`、`feat:`、`fix:`、`refactor:` 或 `chore:` 前缀；不要使用 `git add -A`，也不要提交构建产物、本机缓存和个人解释器路径。

提交前至少检查 `git status --short`、`git diff --cached --check`、`run.py verify --changed` 和 `run.py check`。只有明确需要发布时才推送到 `main`；GitHub Actions 会负责渲染并部署 Pages。

## 发布

推送到 `main` 后，GitHub Actions 渲染 Book，并把 `_book/` 推到 `gh-pages` 分支（Pages：Deploy from a branch → `gh-pages` / `(root)`）。

目录职责与内容路线图的**单一真源**是 [`handbook/repository-structure.md`](handbook/repository-structure.md)；
README 只保留入口和使用说明；具体维护规则、写作规范和脚手架细节分别见 [`AGENTS.md`](AGENTS.md)、[`handbook/operations/agent-operations.md`](handbook/operations/agent-operations.md) 和 `.cursor/skills/`。
