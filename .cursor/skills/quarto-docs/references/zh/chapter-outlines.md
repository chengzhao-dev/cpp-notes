# 章节标题骨架知识库

低优先级、仅按需读取。写新章或重构已有章时再查本文件；日常任务和 `scope` 的 READ 清单不预读它。
本文件记录**具体某一章**采用的一二三级标题骨架，不与 `basics.md` 的通用标题规范重复。

## 使用方式

1. 目标章节已有骨架：按本文件的标题顺序生成或调整 `.qmd`，不自行增删一级层次。
2. 目标章节没有骨架：先用 `cpp-topic.qmd` 模板，定稿后把实际标题回填本文件，作为后续基线。
3. 通用规则（标题层级、callout 类型、冒号密度、终端块约定）以 `quarto-docs` 的 references 为准，本文件不复制这些规则。

## 骨架速览

- 一级：`##`（章标题来自 YAML `title:`，正文不写 `# H1`）。
- 二级：`###`，只写任务名称，不加 `1.1`、`2.3` 之类编号。
- 大节与小节都用无序号的自然语言标题；本书 `number-sections: false`，手动序号在增删小节后会与目录和正文引用错位。
- 章首是一段引言（动机 + 读者收益 + 推进顺序）；章末固定 `## 本章回顾`。
- Callout 放在所属小节的语义末尾，后面不再紧跟正文段落。
- 官方文档已有完整说明的内容：正文只留最关键判断，其余用官方链接指向。
- 关键命令在脚本头注释中集中解释（`g++` 直接编译、`cmake -G Ninja -B build -DCMAKE_BUILD_TYPE=Debug`、`cmake --build build`）；`cd`、`./app`、`--version` 一类不单独解释。

## getting-started/setup-wsl2

```text
引言（一段：环境分工 + 三步推进顺序 + 完成后可用什么）
## WSL 与 Ubuntu 环境搭建
### 启用 WSL2 并安装 Ubuntu
### 替换国内镜像源与系统更新
## C++ 核心依赖安装与验证
### 安装编译器、构建工具与调试器
### 配置智能提示语言服务
## Windows Terminal 开发环境集成
### 配置 Windows Terminal 为默认 WSL 终端
### 连接 VS Code Remote-WSL 开发环境
## 本章回顾
```

要点：换源的具体配置随 Ubuntu 版本变化，正文不写死路径和 `sed` 命令，用中文封装的链接指向镜像站官方使用帮助，`apt update`/`apt upgrade` 这类长期不变的操作直接写清；不预先运行版本命令验证工具链，改为安装后直接进入构建，失败时回到对应小节重装（见 `terminal-validation.md`）。「启用 WSL2 并安装 Ubuntu」末尾放虚拟机平台 warning，「替换国内镜像源与系统更新」末尾放镜像站选择 note，「安装编译器、构建工具与调试器」末尾放"不预检"tip，「配置 Windows Terminal 为默认 WSL 终端」末尾放终端职责边界 note。

## getting-started/first-program

```text
引言（一段：承接上一章 + 本章两条构建路径）
## 项目结构与源码准备
### 梳理工程目录与文件依赖
### 确认核心源码与预期输出
## 基于编译器的直接构建流程
### 设定编译标准与严格警告选项
### 执行单文件编译与运行验证
## 基于构建工具的自动化管理
### 编写项目构建规则文件
### 执行自动化配置与一键运行
## 常见问题
### 提示找不到 g++ 或 cmake
### 构建目录残留了旧的编译器或选项
## 本章回顾
```

要点：「梳理工程目录与文件依赖」的目录树用行尾 `#` 注释说明职责，包含 `build/` 与 `compile_commands.json`；「设定编译标准与严格警告选项」用表格交代 `-std=c++20 -Wall -Wextra -Werror -o`；「执行单文件编译与运行验证」用单条命令块串起「建目录 → 编译 → 运行 → 预期输出」；「执行自动化配置与一键运行」依次解释 `-G Ninja`、`-B build`、`-DCMAKE_BUILD_TYPE=Debug` 与 `cmake --build`。前者末尾放警告价值 tip，后者末尾放编译数据库 note。`main.cpp`、`CMakeLists.txt`、`build-and-run.sh` 三份示例都用带语言名的围栏包住 `{{< include >}}`。Debug 的实际效果是 `-g` 且不加优化，不写 `-O0`。

## 待补章节

`handbook/tasks/content/` 里已有任务单，但尚无骨架基线的 part：`core`、`stl`、`memory`、`debugging`、`toolchain`、`performance`、`cheatsheet`。生成或定稿后按上面的格式追加小节。