# C++ 学习轨迹笔记

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

这里记录我的中文 C++ 学习过程。内容从 Linux 开发环境开始，走通单文件编译、最小程序结构、CMake、多文件工程和库，再进入语言基础。

在线阅读：<https://chengzhao-dev.github.io/cpp-notes/>

## 从这里开始

按下面的顺序阅读，每页都在上一页的基础上增加一个概念：

1. [准备 WSL2 C++ 开发环境](content/getting-started/setup-wsl2.qmd)
2. [编译并运行第一个 C++ 程序](content/getting-started/first-program.qmd)
3. [拆分最小 C++ 程序结构](content/getting-started/minimal-program-structure.qmd)
4. [用 CMake 构建 C++ 程序](content/getting-started/cmake-project.qmd)
5. [用 CMake 管理多文件工程](content/getting-started/multi-file-project.qmd)
6. [构建静态库并链接程序](content/getting-started/static-library.qmd)
7. [构建动态库并运行程序](content/getting-started/shared-library.qmd)
8. [类型与变量](content/language-basics/types-and-variables.qmd)
9. [常量与不可变值](content/language-basics/constants.qmd)

[工程应用分册](content/practice/index.qmd)从真实项目视角说明构建产物的交付职责，其中的[影像算法的交付形态](content/practice/android-imaging.qmd)可以随时阅读。

建议边读边输入命令。章节示例放在 `code/getting-started/` 和 `code/language-basics/`，可以直接运行，也可以修改后重新构建。

## 仓库内容

| 路径 | 内容 |
| --- | --- |
| `content/` | 笔记正文 |
| `code/` | 正文使用的 C++ 示例 |
| `.agents/knowledge/` | 写作和工程决定的依据 |
| `.agents/` | 维护规则、检查脚本和网站主题 |

需要修改仓库时，先阅读 [AGENTS.md](AGENTS.md)。
