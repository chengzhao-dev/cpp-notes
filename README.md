# cpp-notes

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

**C++ 笔记**是一份面向初学者的中文 C++ 学习笔记，记录从可运行示例出发学习语言、标准库和工程实践的过程。所有示例在 Linux 上编译运行，Windows 用户通过 WSL2 获得同样的环境。

在线阅读：<https://chengzhao-dev.github.io/cpp-notes/>。建议边阅读边编译和运行示例，只读不写无法验证任何结论。

## 从哪里开始

路线按 part 分组，每组内部从 1 开始编号，依次读完即可完成该组目标。

### getting-started：环境与第一个程序

1. [搭建 WSL2 开发环境](content/getting-started/setup-wsl2.qmd)：启用 WSL2 上的 Ubuntu，换用国内镜像源，装好编译器、构建工具与编辑器。
2. [写出第一个 C++ 程序](content/getting-started/first-program.qmd)：用 `main.cpp` 完成一次直接编译，再用 CMake 与 Ninja 自动构建出同一个可执行文件。

### 后续 part

语言基础、标准库、对象管理、调试与性能等 part 尚未开始写作。章节状态与目录关系见
`.agents/skills/agent-ops/references/repository-structure.md`。新增 part 时在上一节之后追加同名小节，编号从 1 重新开始。

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
├── .agents/
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
`.agents/skills/cpp-content/references/tasks/<part>.md` 里的一行。索引产物在 `temp/knowledge-index/`，
重构报告在 `temp/refactor/`，两者都不入库。

## 内容范围

当前路线从入门环境和第一个程序开始，逐步覆盖：

- C++ 语言基础，包括变量、类型、函数和控制流。
- 标准库，包括容器、算法和迭代器。
- 对象管理，包括生命周期、RAII、智能指针和移动语义。
- 工程实践，包括 CMake、多文件项目、调试和性能。

页面本身怎么组织由两类模式约定：教学正文的块序列与入口卡片页的三层结构。依据在知识库 `quarto-docs` 域，分别用 `run.py kb-search "块序列" --domain quarto-docs` 与 `run.py kb-search "卡片" --domain quarto-docs` 查询。
