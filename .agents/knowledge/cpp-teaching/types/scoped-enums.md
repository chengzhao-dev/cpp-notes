---
kb_id: "cpp-scoped-enums-v1"
title: "枚举类的语义与教学边界"
domain: "cpp-teaching"
subdomain: "types"
tags: [enum, enum_class, scoped_enum, types, strong_typing]
level_range: [1, 4]
dependencies: ["cpp-primitive-types-numeric-safety-v1", "cpp-list-initialization-v1"]
created: "2026-09-28"
updated: "2026-09-30"
chunk_strategy: "semantic_heading"
estimated_tokens: 700
---

# 枚举类的语义与教学边界

## 语义与默认取舍

### enum class 提供的约束

`enum class` 定义封闭取值集合：枚举值限定在类型名作用域内，与整数之间不发生隐式转换，同类型值之间可以 `==`、`!=` 比较和赋值；需要底层整数类型时在声明中显式指定。C++ Core Guidelines Enum.3 建议新代码使用 scoped enum；不写 `class` 的 unscoped `enum` 是历史惯性与 C 兼容需要，不作教学默认。

### 与整数的边界

枚举值不参与算术；需要编号时用 `static_cast<int>` 写出转换意图，只用于输出或与既有接口对接。这个摩擦是刻意的：把「状态被当成任意整数使用」挡在编译期。

## 教学边界

语言基础把枚举拆成两页：`enums.qmd` 讲普通 `enum` 的作用域泄漏与隐式转换两个问题，`enum-class.qmd`（配 `code/language-basics/enum-class.cpp`）讲 `enum class` 的限定名访问、与整数的显式转换、底层类型、行尾注释写法，以及枚举类作为值类型按值用在参数与返回值（示例 `CellState PlayerToCellState(Player player)`）；两张速查（`parameter-passing-guide.qmd`、`return-value-guide.qmd`）按机制归并选型。位掩码用途（`operator|` 重载）与 `using enum` 在运算符与自定义类型章节引入。

## 底层类型约定

Google C++ Style Guide 与 LLVM Coding Standards 都不强制 `enum class` 写底层类型，LLVM 仅在位域与紧凑布局时按需使用 `: uint8_t`。两仓工程代码把它定为默认约定：成员少的状态码类（`Player`、`Mark`、`GameStatus`、`ApplyResult`）写 `enum class Name : std::uint8_t`，让对象布局可预测、枚举的存储宽度一眼可见。这是有意偏离而非指南原文，依据见姊妹仓库标识 `bg-google-cpp-style-v1` 的知识文件「整型与枚举底层类型」。

## 与项目值类型的衔接

姊妹仓库 cpp-board-games 的井字棋状态模型把玩家、棋子、终局结果等封闭集合定义为带 `std::uint8_t` 底层类型的 `enum class`，数据组合用 `struct` 聚合；强类型包装属于进阶内容（见标识 `cpp-strong-types-v1` 的知识文件）。
