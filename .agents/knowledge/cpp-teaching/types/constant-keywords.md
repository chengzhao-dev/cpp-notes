---
kb_id: "cpp-constant-keywords-v1"
title: "const 家族的页面拆分与选型依据"
domain: "cpp-teaching"
subdomain: "types"
tags: [const, constexpr, consteval, constinit, const-member-functions, inline, odr, constant, selection, header]
level_range: [1, 5]
dependencies: ["cpp-language-basics-path-v1", "cpp-primitive-types-numeric-safety-v1", "cpp-const-member-functions-v1"]
created: "2026-09-29"
updated: "2026-10-06"
chunk_strategy: "semantic_heading"
estimated_tokens: 1300
---

# const 家族的页面拆分与选型依据

## 为什么拆成四页

### 单页承担不了的四个问题

“常量与配置”单页同时回答语义（`const` 保证什么）、机制（`constexpr` 与 `inline` 如何协作）、选型（同族关键词怎么挑）和成员函数承诺（尾部 const 管什么）四个问题，体量与检索粒度都不合适，后拆为 `const-variables`（语义与命名）、`constexpr`（编译期规则与头文件共享）、`constant-keywords`（对照与选型）三页；`const` 页更名为 `const-variables`，并新增 `const-member-functions`（成员函数尾部 const）第四页，页面边界见标识 `cpp-language-basics-path-v1` 的知识文件。

### 各页的检索定位

`const-variables` 页回答“const 变量保证什么、不保证什么”；`constexpr` 页回答“头文件里的常量怎么写、为什么加 inline”；对比页回答“遇到 consteval、constinit、宏时怎么选”；`const-member-functions` 页回答“成员函数尾部的 const 承诺什么、与参数和返回值上的 const 怎么区分”。检索教学依据时按问题性质选页。

## constexpr 页的结构笔记

`constexpr` 专页 YAML `title` 可用关键字本身；页内 `##` / `###` 尽量不重复该关键字。规划结构如下（与正文章节对齐）：

### 表达编译期规则

`constexpr` 要求初始化结果能在编译期确定；运行时才知道的值用 `const`。数组长度等编译期上下文只接受 `constexpr`。页内可附极简 `constexpr` 谓词函数，完整函数规则后置。

### 在头文件中共享常量

项目公共常量写在头文件、供多个 `.cpp` 包含时，常规写法是具名命名空间加 `inline constexpr`。命名空间作用域的 `const` / `constexpr` 变量默认内部链接：每份包含各有一份拷贝，通常无害但地址不共享。推荐次序：公共常量放具名命名空间的 `inline constexpr`；单文件常量就近放函数内或匿名命名空间；裸全局常量尽量不用。

### 对比头文件里的常量与函数

头文件里常量与函数对 `inline` 的要求不同，分点写清：

**命名空间变量需要 inline。** 命名空间（或类）作用域的变量要跨翻译单元共享同一实体时，显式写 `inline constexpr`（C++17 起变量可用 `inline`）。普通（非 const、非 inline）全局变量写在头文件里会在链接期报重复定义。

**自由函数不必写 inline。** 头文件中的 `constexpr` 自由函数隐式 `inline`，定义可直接放在头文件供多 `.cpp` 包含；显式再写 `inline` 冗余但不算错。函数局部的 `constexpr` 不参与链接，不能加 `inline`。

### constexpr 函数的定义为何要放头文件

`constexpr` 函数在编译期求值时，调用点必须看得到完整函数体；定义放在 `.cpp` 里，其他翻译单元只有声明，编译期调用直接失败。普通函数按「头文件声明、`.cpp` 定义」拆分后仍能链接，是因为链接器在链接期把调用接到定义上，编译期求值等不到链接期，定义必须随头文件进入每个用到它的翻译单元；多份拷贝由隐式 `inline` 在链接期合并，不产生重复定义。`constexpr` 页配 `Square` 简例与反面形态（声明在 `.h`、定义在 `.cpp`）讲这层机制。

### constexpr 头文件函数的滥用边界

定义随头文件是机制要求，不是把所有函数搬进头文件的理由：头文件函数体每改一次，所有包含它的 `.cpp` 都要重新编译，编译隔离失效。普通运行期函数维持「声明在头文件、定义在 `.cpp`」，`constexpr` 只留给需要编译期求值的函数（编译期查表、单位换算、`PlayerToCellState` 式简单映射）与希望内联的极小函数；联网复核同向依据：open-std「Don't constexpr All The Things」、Trail of Bits 常量关键字实践与 Jason Turner 的 Practical constexpr 系列。

### 标准演化

| 标准节点 | 与常量相关的变化 |
| --- | --- |
| C++11 | 引入 `constexpr` 变量与函数，函数限制严 |
| C++14 | 放宽 `constexpr` 函数能写的语句 |
| C++17 | 引入 `inline` 变量；头文件里 `inline constexpr` 成为公共常量常规写法；类内 `static constexpr` 数据成员隐式 `inline` |
| C++17 之前 | 头文件常量靠枚举、宏或单 `.cpp` 定义规避链接问题 |
| C++20 | 新增 `consteval` 与 `constinit` |

`consteval` 强制函数调用发生在编译期；`constinit` 保证静态存储期变量在编译期完成初始化但对象仍可修改。两者在基础分册只进对照表（`constant-keywords` 页），不开专页。

## 与工程仓库的边界

姊妹仓库 cpp-board-games 只写工程用法：井字棋库对外头文件把棋盘尺寸写成 `tictactoe` 命名空间内的 `inline constexpr`（`kRows`、`kCols`），映射与换算用 `constexpr` 自由函数（`PlayerToCellState`），运行期谓词按 Google 风格用 PascalCase（`IsValid`）。语言机制（本文件的结构与演化依据）只在 cpp-notes 讲，工程页只链接不重复。命名依据见标识 `cpp-naming-format-v1` 的知识文件。
