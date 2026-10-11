# C++ 学习轨迹笔记

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

这里记录我的中文 C++ 学习过程。内容从 Linux 开发环境开始，走通单文件编译、最小程序结构、CMake、多文件工程和库，再进入语言基础。

在线阅读：<https://chengzhao-dev.github.io/cpp-notes/>

## 从这里开始

按下面的顺序阅读，每页都在上一页的基础上增加一个概念：

1. [准备 WSL2 C++ 开发环境](content/getting-started/setup-wsl2.qmd)
2. [第一个程序](content/getting-started/first-program.qmd)
3. [最小程序结构](content/getting-started/minimal-program-structure.qmd)
4. [用 CMake 构建 C++ 程序](content/getting-started/cmake-project.qmd)
5. [多文件工程](content/getting-started/multi-file-project.qmd)
6. [类型与变量](content/language-basics/types-and-variables.qmd)
7. [函数](content/language-basics/functions.qmd)
8. [分支和循环](content/language-basics/branch-and-loop.qmd)
9. [const 变量](content/language-basics/const-variables.qmd)
10. [constexpr](content/language-basics/constexpr.qmd)
11. [常量关键词](content/language-basics/constant-keywords.qmd)
12. [类与封装](content/language-basics/classes.qmd)

语言机制的工程用法见姊妹仓库 [cpp-board-games](https://github.com/chengzhao-dev/cpp-board-games)。[实现棋盘存储](https://github.com/chengzhao-dev/cpp-board-games/blob/main/content/tictactoe/03-board.qmd)用 `CellState` 保存每一格，[实现对局规则](https://github.com/chengzhao-dev/cpp-board-games/blob/main/content/tictactoe/04-game.qmd)拒绝非法落子并判定胜负与平局。

[工程应用分册](content/practice/index.qmd)接着构建[静态库](content/practice/static-library.qmd)和[动态库](content/practice/shared-library.qmd)，其中的[交付形态](content/practice/android-imaging.qmd)说明这些产物在真实项目里的职责。

建议边读边输入命令。章节示例放在 `code/getting-started/` 和 `code/language-basics/`，可以直接运行，也可以修改后重新构建。

## 仓库内容

| 路径 | 内容 |
| --- | --- |
| `content/` | 笔记正文 |
| `code/` | 正文使用的 C++ 示例 |
| `.agents/` | 维护规则、领域知识库（`knowledge/`）、检查脚本和网站主题 |

需要修改仓库时，先阅读 [AGENTS.md](AGENTS.md)。
