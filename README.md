# C++ 学习轨迹笔记

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

这里记录我的中文 C++ 学习过程。内容从 Linux 开发环境开始，逐步走到单文件编译、最小程序结构、CMake、多文件工程和库，再进入语言基础。

在线阅读：<https://chengzhao-dev.github.io/cpp-notes/>

## 从这里开始

按下面的顺序阅读，每页都在上一页的基础上增加一个概念：

1. [搭建 WSL2 开发环境](content/getting-started/setup-wsl2.qmd)
2. [写出第一个 C++ 程序](content/getting-started/first-program.qmd)
3. [拆开最小程序结构](content/getting-started/minimal-program-structure.qmd)
4. [用 CMake 构建程序](content/getting-started/cmake-project.qmd)
5. [构建多文件工程](content/getting-started/multi-file-project.qmd)
6. [构建静态库](content/getting-started/static-library.qmd)
7. [构建动态库](content/getting-started/shared-library.qmd)
8. [类型与变量](content/language-basics/types-and-variables.qmd)
9. [常量与不可变值](content/language-basics/constants.qmd)

建议边读边输入命令。章节示例分别放在 `code/getting-started/` 和 `code/language-basics/`，可以直接运行，也可以修改后重新构建。

## 仓库内容

| 路径 | 内容 |
| --- | --- |
| `content/` | 笔记正文 |
| `code/` | 正文使用的 C++ 示例 |
| `knowledge/` | 写作和工程决定的依据 |
| `.agents/` | 维护规则、检查脚本和网站主题 |

需要修改仓库时，先阅读 [AGENTS.md](AGENTS.md)。
