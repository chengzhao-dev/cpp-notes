# cpp-notes

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

**C++ 笔记**是一份面向初学者的个人学习笔记，记录从可运行示例开始学习 C++ 语言、标准库和工程实践的过程。

在线阅读：[chengzhao-dev.github.io/cpp-notes](https://chengzhao-dev.github.io/cpp-notes/)。从入门路线开始，边阅读边编译和运行示例。

## 从哪里开始

路线按 part 分组，每组内部从 1 开始编号，依次读完即可完成该组目标。

### getting-started：环境与第一个程序

1. [搭建开发环境](content/getting-started/index.qmd)：启用 WSL2 上的 Ubuntu，换用国内镜像源，安装编译器与构建工具。
2. [写出第一个 C++ 程序](content/getting-started/first-program.qmd)：用 `main.cpp` 完成直接编译，再用 CMake 与 Ninja 自动构建。

开发环境的分工很简单：Windows 提供图形界面，WSL2 上的 Ubuntu 提供编译和运行环境，VS Code 用于编辑，CMake 负责构建。

### 后续 part

语言基础、标准库、对象管理、调试和性能等 part 尚未开始写作，路线和章节状态见
[`handbook/repository-structure.md`](handbook/repository-structure.md)。新增 part 时在上一节之后追加同名小节，编号从 1 重新开始。

## 仓库结构

下面的目录树展开项目中与阅读、示例和内容维护有关的部分。目录名和文件名均来自当前仓库；构建产物与缓存没有列出，正文也不再重复解释每个目录。

```text
cpp-notes/
├── content/                        # Quarto 章节正文，按 part 分子目录
│   └── getting-started/            # 入门 part：环境搭建与第一个程序
├── code/                           # 与章节对应的 C++ 示例和工程
│   └── getting-started/            # 入门 part 的示例工程，build/ 是产物
├── theme/                          # 页面主题
│   ├── assets/                     # 自托管字体与站点图标
│   ├── css/                        # 按域拆分的样式表
│   ├── includes/                   # 注入页面头部与尾部的 HTML 片段
│   └── scss/                       # 明暗两套 SCSS 变量
├── handbook/                       # 项目自身文档
│   ├── repository-structure.md     # 目录关系、章节路线图与体量预算
│   ├── operations/                 # Agent 运维、上下文预算与渲染细则
│   ├── tasks/                      # 各章任务单（读写边界与验收）
│   └── scripts/                    # 脚手架与维护脚本
├── .cursor/                        # Agent 配置
│   ├── mcp/                        # 项目级 MCP 服务
│   ├── skills/                     # 写作、C++、主题与运维 skills
│   └── tools/                      # 统一入口 run.py 与各项检查
├── _quarto.yml                     # Quarto Book 配置与章节注册
├── index.qmd                       # 站点首页
├── AGENTS.md                       # 项目级 Agent 入口：结构、命令与读取边界
├── CODEX-PERSONAL-INSTRUCTIONS.md  # 给 Codex 个性化设置使用的六项原则
├── LICENSE                         # MIT 许可
└── README.md                       # 仓库入口说明
```

章节、示例和任务清单按相同的 part 与 chapter 名称对应。例如，`content/getting-started/` 的示例位于 `code/getting-started/`，相关任务位于 `handbook/tasks/content/getting-started/`。

## Agent 六项原则

`CODEX-PERSONAL-INSTRUCTIONS.md` 单独保存六项原则，用于 Codex 个性化设置中的「Codex 说明」一栏：把该文件正文粘贴进输入框并保存，此后每个会话都会带上它。原因是这类全局行为约束放在宿主个性化设置里才会在执行过程中真正生效，项目内的规则文件只会被按需读取。

该文件只服务宿主设置。仓库内的 skills、任务单和检查脚本不把它列为阅读项，也不在任务中读取它；项目结构与命令约束仍见 [`AGENTS.md`](AGENTS.md)。

## 内容范围

当前路线从入门环境和第一个程序开始，逐步覆盖：

- C++ 语言基础，包括变量、类型、函数和控制流；
- 标准库，包括容器、算法和迭代器；
- 对象管理，包括生命周期、RAII、智能指针和移动语义；
- 工程实践，包括 CMake、多文件项目、调试和性能。

具体章节状态和目录关系见 [`handbook/repository-structure.md`](handbook/repository-structure.md)。