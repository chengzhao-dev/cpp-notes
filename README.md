# C++ 笔记

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

**C++ 笔记**是一份面向初学者的中文 C++ 笔记。它以 Linux 为运行环境，从可以运行的程序开始，逐步介绍 C++ 语言、工具链和工程构建。

在线阅读：<https://chengzhao-dev.github.io/cpp-notes/>

## 阅读顺序

阅读入口为 [入门与构建](content/getting-started/index.qmd)。六个页面按下面的顺序逐页完成：

1. [搭建 WSL2 开发环境](content/getting-started/setup-wsl2.qmd)
2. [写出第一个 C++ 程序](content/getting-started/first-program.qmd)
3. [用 CMake 构建程序](content/getting-started/cmake-project.qmd)
4. [构建多文件 C++ 工程](content/getting-started/multi-file-project.qmd)
5. [构建静态库](content/getting-started/static-library.qmd)
6. [构建动态库](content/getting-started/shared-library.qmd)

建议边读边输入命令。只阅读不运行，无法确认环境和程序是否正常。

## 准备环境

你需要一台可以安装 WSL2 的 Windows 电脑。第一章会说明如何安装 Ubuntu 和 C++ 工具。后续命令都在 Ubuntu 终端中执行。

## 运行示例

示例源码位于 `code/getting-started/`。需要编译运行的章节都提供 `build-and-run.sh`：首程序直接调用 `clang++`，CMake 与库工程依次完成配置、构建和运行。

## 仓库结构

```text
cpp-notes/
├── content/     # 笔记正文
├── code/        # 与正文对应的 C++ 示例
├── knowledge/   # 内容取舍的依据
├── .agents/     # 自动化规则和维护工具
├── _quarto.yml  # 网站配置
├── index.qmd    # 网站首页
└── README.md    # 本文件
```

需要修改仓库或运行检查时，先阅读 [AGENTS.md](AGENTS.md)。它记录了开发命令、读取边界和验收要求。
