---
kb_id: "cpp-strong-types-v1"
title: "强类型包装的取舍"
domain: "cpp-teaching"
subdomain: "types"
tags: [strong_type, value_semantics, struct, units, types]
level_range: [2, 5]
dependencies: ["cpp-scoped-enums-v1", "cpp-list-initialization-v1"]
created: "2026-09-28"
updated: "2026-09-28"
chunk_strategy: "semantic_heading"
estimated_tokens: 700
---

# 强类型包装的取舍

## 动机与最小形式

### 为什么不直接用基础类型

同一底层类型承载不同领域含义（距离、时长、分数）时，类型系统无法阻止互相赋值与传参错位。轻量 `struct` 包装给值加上领域名字，让「不该混用」成为编译错误，代价是取值时显式写出 `.value` 的摩擦。

### 最小形式与已知边界

`struct Meters { double value{0}; };` 这样聚合包装沿用语言基础的聚合初始化与值语义复制规则。它是约定上的强类型：成员公开、仍可凭空构造不合理的值；更强的保证需要构造函数与不变量，属于自定义类型章节。取值封闭的领域值不使用包装，直接用 `enum class`（见标识 `cpp-scoped-enums-v1` 的知识文件）。

## 与项目值类型的分工

cpp-board-games 井字棋首批值类型只用 `enum class` 与普通聚合（`Position`、`Move` 这类数据组合），强类型包装不在首批；教学页对应 `content/language-advanced/strong-types.qmd` 与 `code/language-advanced/strong-types.cpp`，只建立动机与边界认知，不提前引入构造语法。
