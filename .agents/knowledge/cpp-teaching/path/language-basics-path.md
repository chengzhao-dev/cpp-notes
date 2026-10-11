---
kb_id: "cpp-language-basics-path-v1"
title: "C++ 语言基础的教学顺序与边界"
domain: "cpp-teaching"
subdomain: "path"
tags: [cpp, language_basics, types, variables, constants, auto, scope, initialization, curriculum, build_boundary]
level_range: [0, 4]
dependencies: ["cpp-agent-context-budget-v1", "cpp-list-initialization-v1", "cpp-tooling-build-chain-v2"]
created: "2026-09-16"
updated: "2026-09-30"
chunk_strategy: "semantic_heading"
estimated_tokens: 760
---

# C++ 语言基础的教学顺序与边界

## 类型与变量的教学边界

### 先建立值、类型与名字的关系

初学者首先需要理解“程序怎样保存和改变一份数据”，而不是记住所有类型的大小和转换规则。页面先让读者创建有意义的变量，再说明类型决定可表示的值和允许的操作。

基础类型页只覆盖 `int`、`double`、`bool` 和 `char`，不使用 `std::string`。类型大小、范围、符号、溢出、转换、浮点精度与 `std::size_t` 集中放入 `cpp-primitive-types-numeric-safety-v1`，避免规则散落。

### 初始化、赋值、类型推断与作用域

初始化与赋值必须作为两种动作介绍：前者在创建变量时确定初始值，后者修改已有变量的值。列表初始化、空花括号和值初始化的取舍见标识 `cpp-list-initialization-v1` 的知识文件。

`auto` 是编译期类型推断，不是动态类型，也不会让变量在运行期改变类型。同时介绍全局作用域和块作用域；函数参数、生命周期、析构顺序和内存布局留到后续章节。

## 初始化与类型推断

初始化、赋值、`auto` 和初始化列表推导单独成页，基础类型页只保留变量与作用域的心智模型。普通变量初始化默认使用 `{}`，`auto` 初始化统一使用 `auto value = expression;`，避免把初始化列表的特殊规则误当成常规写法。

## 常量的四页拆分

### 为什么先讲 const 变量

`const` 解决的是“这个值不应通过该名字被修改”。先讲命名常量对可读性的帮助，再讲必须在创建时初始化、后续赋值会被编译器拒绝。`const-variables` 页不展开 `constexpr` 与 `inline`，文末链到下一页；原 `const` 页已更名为 `const-variables`，与后续 `const-member-functions` 页区分开（更名记录见 frontmatter updated）。

### constexpr 页的边界

`constexpr` 独立成页，承担编译期确定要求、头文件公共常量的 `inline constexpr` 写法（具名命名空间、内部链接对照）与 C++11→17→20 演化短表，并附极简 `constexpr` 谓词函数。模板与重度编译期求值仍后置到后续主题；“基础页只保留短 constexpr”的旧政策由本页边界取代。

### 对比页承载选型

`constant-keywords` 页用对照表比较 `const`、`constexpr`、`consteval`、`constinit` 与宏，只解决“什么时候用哪个”，不设独立示例，长示例复用前两页。

### 成员函数 const 页的边界

`const-member-functions` 页插在 `structs-and-value-types` 之后：教学上必须先有类型与对象，成员函数尾部的 `const` 才有承诺对象。页内为成员函数语法只给最小上下文（`对象.函数名(实参)` 调用与逐成员读写），完整函数语法仍由函数章展开；尾部 const、返回类型、参数与局部变量四处 `const` 用一张对照表收拢。依据见标识 `cpp-const-member-functions-v1` 的知识文件。

## 语言基础的页面与构建边界

语言基础分册的中心是语言规则与由语言衍生的概念：类型、作用域、常量性、表达式、控制流、函数和自定义类型。构建链已经在前一个分册作为独立任务跑通，语言基础章节不重复展开 CMake 配置。

各章保持扁平源文件，由分册根的单一 `CMakeLists.txt` 收集成同名可执行文件。正文用最小片段解释当前规则，完整源码保留在 `code/`，源码位置、构建入口和观察重点合并进 `## 本章回顾`。

## 语言基础路线

语言基础按“基础类型与变量 → 编写并调用函数 → switch 与 for → 初始化与推断 → const 变量 → constexpr → 常量关键词对比 → 数值安全 → 枚举 → 枚举类 → 命名空间 → 结构体与值类型 → 成员函数上的 const → 引用使用场景 → 指针使用场景 → ★ 传参选型速查 → ★ 返回值选型速查 → nodiscard → 把数据与操作放进类”推进。没有 `code/` 示例的课不写进这条顺序，也不在索引里预告。

1. 函数紧跟基础类型，`switch` 与 `for` 紧跟函数。类放在 `nodiscard` 之后；简单项目设计章接着用值类型、类与输入输出边界组织最小项目。
2. 引用与指针先讲场景选型：按现行 Google「Inputs and Outputs」规则建立“怎么选传参”的心智。
3. 每章先改任务矩阵状态再写正文；没有示例的课不注册进 `_quarto.yml`。

## 与主流教材的取舍

Learn C++ 与这本笔记一样，先写只按值传递整数的函数，再写 `switch` 与 `for`。*C++ Primer* 把语句放在函数前面；这里不跟着改，因为现有函数课用不到分支。SG20 建议先教 `enum class`。本笔记保留「先看普通枚举的两个问题，再写枚举类」，因为这一页的任务就是指出泄漏，不把普通枚举当成要用的工具。指针运算仍留在待办，不插进当前路径。`std::string` 与 `std::vector` 属于下一课，类型页继续不讲 `string`。

进阶与内存两条支线的次序：进阶由 language-advanced 分册承接（strong-types 已有，可续模板等）；内存按“stack-heap → raii → smart-pointers → move-semantics”推进，次序登记在对应任务矩阵。

新章节只在任务矩阵登记后创建，一次只引入一个主要变化。前一章已经演示过的语法不再复制完整示例，只保留理解当前规则所需的最短上下文。

## 值类型与分组章节的最小边界

`enums`、`enum-class`、`namespaces` 与 `structs-and-value-types` 插在数值安全之后、运算之前，为姊妹仓库 cpp-board-games 的项目值类型建模（如井字棋状态模型）提供最小语言集。枚举拆两页：`enums` 讲普通 `enum` 的两个问题，`enum-class` 讲限定名访问、与整数的显式转换、底层类型、成员注释写法与按值传参返回，两页都不讲位掩码与 `using enum`；命名空间章只讲分组、限定名与头文件禁用 `using namespace`；结构体章只讲聚合初始化、成员默认值与值语义复制，成员函数的 `const` 承诺单独进 `const-member-functions` 页，访问控制与引用留给原定章节。两张 ★ 速查（传参、返回值）插在指针场景章之后，按机制归并选型，细节回链场景章；`nodiscard` 页跟在返回值速查之后，用属性标注把“结果不能无视”变成编译期检查（依据见标识 `cpp-nodiscard-v1` 的知识文件）。

## 扩展与验证约束

教学页优先控制在 100 行和 4000 有效字符左右；达到 150 行或 5000 有效字符时必须先拆分或压缩。新增语言章节至少验证示例编译通过、正文承诺的输出与实测一致、任务矩阵状态准确，并确认知识检索能命中对应教学依据。

首次出现类型名、关键字和库类型时给出中文解释和英文检索词。`auto` 只能解释为编译期类型推断，不能写成“动态类型”；`const` 只能解释为不可通过该名字修改，不能承诺对象永远不变。
