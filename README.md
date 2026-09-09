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
`.cursor/skills/agent-ops/references/repository-structure.md`。新增 part 时在上一节之后追加同名小节，编号从 1 重新开始。

## 仓库结构

```text
cpp-notes/
├── content/                          # Quarto 章节正文，按 part 分子目录
│   └── getting-started/              # 入门 part：index/setup-wsl2/first-program.qmd
├── code/                             # 与章节对应的 C++ 示例，build/ 与 .cache/ 是产物
│   └── getting-started/first-program/
├── knowledge/                        # 精简领域知识库（回答「为什么」）
│   ├── README.md                     # 知识库规范与新增知识闭环
│   ├── agent-ops/  cpp-content/  github-ops/  quarto-docs/
├── .cursor/
│   ├── manifest.json                 # 项目能力清单
│   ├── mcp/                          # 项目级 MCP 服务（server.py）
│   └── skills/
│       ├── catalog.md                # skill/reference/knowledge 全景路由表（先读这里）
│       ├── agent-ops/                # 统一入口 run.py、scope 与各项检查脚本
│       ├── code-review/              # 只读缺陷审查
│       ├── cpp-content/              # C++ 内容：references/cpp/、references/tasks/、模板与校验
│       ├── github-ops/               # git、gh CLI、Pages、CI 操作清单
│       ├── python-tools/             # 知识库管道、脚手架与维护脚本
│       ├── quarto-docs/              # .qmd 写法与中文技术文档格式
│       └── quarto-theme/             # 主题 css/scss、设计令牌与布局校验
├── .github/workflows/                # pages.yml（发布）与 render-check.yml（PR 校验）
├── _quarto.yml                       # Book 配置与章节注册
├── index.qmd                         # 站点首页
├── AGENTS.md                         # 项目级 Agent 入口：结构、命令与读取边界
└── LICENSE                           # MIT 许可
```

章节、示例和任务矩阵按相同的 part 与 chapter 名称对齐：`content/<part>/<chapter>.qmd`、
`code/<part>/<chapter>`（单文件 `.cpp` 或同名工程目录）、
`.cursor/skills/cpp-content/references/tasks/<part>.md` 里的一行。索引产物在 `temp/knowledge-index/`，
重构报告在 `temp/refactor/`，两者都不入库。

## 内容范围

当前路线从入门环境和第一个程序开始，逐步覆盖：

- C++ 语言基础，包括变量、类型、函数和控制流；
- 标准库，包括容器、算法和迭代器；
- 对象管理，包括生命周期、RAII、智能指针和移动语义；
- 工程实践，包括 CMake、多文件项目、调试和性能。

具体章节状态和目录关系见 `.cursor/skills/agent-ops/references/repository-structure.md`。
