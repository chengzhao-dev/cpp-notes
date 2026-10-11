---
kb_id: "cpp-const-member-functions-v1"
title: "成员函数尾部 const 的教学边界"
domain: "cpp-teaching"
subdomain: "types"
tags: [const, member-function, const-correctness, class, selection]
level_range: [1, 5]
dependencies: ["cpp-constant-keywords-v1", "cpp-language-basics-path-v1"]
created: "2026-09-30"
updated: "2026-09-30"
chunk_strategy: "semantic_heading"
estimated_tokens: 600
---

# 成员函数尾部 const 的教学边界

## 为什么单独成页

### 承诺对象是实例本身

成员函数的 `const` 写在参数列表末尾（`Mark MarkAt(Position position) const`），承诺的是“不修改实例自身（`*this`）”，与参数上的 `const`、返回类型上的 `const`、局部变量的 `const` 各管一段、互不替代。四处承诺一张对照表收拢，是这页的核心检索价值；`const-variables` 页的承诺对象是单个变量名，两者不混写。

### 插入位置的前提

页面插在 `structs-and-value-types` 之后：先有类型与对象，尾部 const 才有承诺对象。成员函数语法只给最小上下文（`对象.函数名(实参)` 调用、逐成员读写），完整函数语法仍由函数章展开，不提前讲访问控制、`mutable` 或运算符重载。

## 采纳范围（与工程仓库一致）

查询型 const 成员（`MarkAt`、`Status`）标尾部 const；修改型成员（`Apply`）不标，误标会被编译器拒绝。`[[nodiscard]]` 是独立的属性决策，不并入本页，见标识 `cpp-nodiscard-v1` 的知识文件。

## 与工程仓库的边界

姊妹仓库 cpp-board-games 的工程代码按本页选型写声明（`game_state.h` 的三个公共接口），工程章只写契约的工程问题，不展开语言机制；本页承担语言讲解，两仓通过外链衔接。依据登记在姊妹仓库标识 `bg-google-cpp-style-v1` 的知识文件。
