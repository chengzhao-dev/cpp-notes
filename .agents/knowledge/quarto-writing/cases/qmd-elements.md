---
kb_id: "cpp-quarto-qmd-elements-cases-v1"
title: "Quarto 元素写法正反对照"
domain: "quarto-writing"
subdomain: "cases"
tags: [heading_lead, code_block, callout, multi_command_block, execution_location]
level_range: [0, 9]
dependencies: ["cpp-quarto-qmd-element-cases-v1"]
created: "2026-09-29"
updated: "2026-09-30"
chunk_strategy: "semantic_heading"
estimated_tokens: 500
---

# Quarto 元素写法正反对照

元素细则见标识 `cpp-quarto-qmd-element-cases-v1` 的知识文件；本文件保存正反对照，检索单元是「正确 + 不佳 + 改写」。

## 标题导语与冒号对照

```text
重复：
## 建立 Linux 开发环境
本节安装 WSL2、Ubuntu 和 C++ 工具链，得到后续示例使用的 Linux 开发环境。

改写：
## 安装 WSL2 和 Ubuntu
以管理员身份打开 Windows PowerShell，执行下面的命令安装 WSL2 和默认的 Ubuntu 发行版。
```

```text
动作句（句号收束）：
在 Ubuntu 终端执行下面的命令，更新软件包索引并安装工具链。

结果引导（全角冒号）：
程序输出如下：
```

## 代码块前后重复对照

```text
重复：下面是一段 Bash 命令，用来配置 CMake 工程。
改写：在工程根目录配置 CMake 工程。

重复：下面是 main.cpp 的完整源码。
改写：先通读源码，再让编译器把它变成可执行程序。
```

块后正文同义复述块内注释是同一类重复：

```text
重复（块内注释写输出目录，块后再讲一遍）：
# 把可执行文件输出到构建目录下的 bin
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
执行后可执行文件会生成在 build/bin 目录下。

改写（块后只补注释没覆盖的信息）：
（同一代码块）重新配置后生效，`build/bin` 只在构建目录中出现。
```

## 递进片段合并对照

同一小节内递进依赖的同源片段（后块使用前块已展示的常量、类型或函数，中间只有短导语、没有图或独立验证盒子打断）必须合并为一个围栏，禁止拆成连续多块、每块配半句导语。判定与豁免见标识 `cpp-quarto-qmd-element-cases-v1` 的知识文件「完整示例与语法片段的边界」。

```text
不佳（常量、使用常量的函数拆成两个连续同源围栏，各配半句导语；首句已点名后块符号）：
 kMaxCount 是本程序允许的最大数量，各处都从这里读取：
```{.cpp filename="片段：常量"}
inline constexpr int kMaxCount = 3;
```

超过 kMaxCount 的请求会被拒绝：
```{.cpp filename="片段：判定"}
bool IsAllowed(int count) { return count <= kMaxCount; }
```

改写（合并为一个围栏，块前一句交代整组递进定义，块后列表分项）：
允许数量与上限判定是同一组递进定义：kMaxCount 固定上限，IsAllowed 用它拒绝超限请求：

```{.cpp filename="片段：上限与判定"}
inline constexpr int kMaxCount = 3;
bool IsAllowed(int count) { return count <= kMaxCount; }
```

- kMaxCount：调整上限只改这一处；
- IsAllowed：请求入口都经过这个判定。
```

判定信号：导语点名了后块才出现的符号，或同一条依赖链被拆成多个围栏、每块各配半句导语。仍允许拆块：「片段 + 完整示例」成对、多源文件各一块（入口、头、实现）、中间有图或独立验证盒子打断。

## 多命令块与执行位置对照

```text
模糊：
cmake --build build --verbose
ls -l build/bin/app

逐条说明：
# 重新构建并显示每条实际执行的编译命令
cmake --build build --verbose
# 确认可执行文件是否已经生成
ls -l build/bin/app
```

```text
模糊：先确认当前目录是工程根目录，再查看构建输出。
改写：先用 ls CMakeLists.txt 确认当前位于工程根目录，再重新构建。
```

## 正确形态正例

```text
正确（闭环：说明条件 → 动作 → 结果）：
代码块前：进入示例目录，准备编译 main.cpp。
代码块内：```{.bash filename="WSL Ubuntu（工程根目录）"} cmake -S . -B build
代码块后：成功后生成构建计划，下一步编译可执行文件。
```

正例的判定条件：块前导语讲当前动作与位置，块后说明看到什么算成功；filename 写明运行环境；命令注释一条一个职责。
