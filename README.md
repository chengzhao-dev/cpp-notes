# C++ 笔记

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

**C++ 笔记**是一份面向初学者的中文 C++ 笔记。它从可以运行的程序开始，逐步介绍 C++ 语言和工程构建方式。

在线阅读：<https://chengzhao-dev.github.io/cpp-notes/>

## 当前内容

当前提供两章入门内容：

- 在 Windows 上安装 WSL2 和 Ubuntu，准备 Clang/LLVM 编译与调试工具。
- 写出并运行第一个 C++ 程序，再使用 CMake 管理构建过程。

后面的语言基础、标准库和工程实践正在编写。

## 阅读顺序

1. [搭建 WSL2 开发环境](content/getting-started/setup-wsl2.qmd)
2. [写出第一个 C++ 程序](content/getting-started/first-program.qmd)

建议边读边输入命令。只阅读不运行，无法确认环境和程序是否正常。

## 准备环境

你需要一台可以安装 WSL2 的 Windows 电脑。第一章会说明如何安装 Ubuntu 和 C++ 工具。后续命令都在 Ubuntu 终端中执行。

## 运行示例

示例源码位于 `code/getting-started/`。每章会给出完整的编译和运行命令，你可以直接跟着操作，也可以用 `build-and-run.sh` 一次完成配置、构建和运行。

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
