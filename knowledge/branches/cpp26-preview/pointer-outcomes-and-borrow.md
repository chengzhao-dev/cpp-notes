---
kb_id: "cpp-core-pointer-roadmap-v3"
title: "C++ 指针路线图增强版（C++26 preview：所有权与借用）"
domain: "cpp_core"
subdomain: "memory_pointers"
tags: [pointer, smart_pointer, RAII, ownership, borrowing, lifetime, cache, memory_model]
level_range: [0, 10]
dependencies: ["cpp-core-pointer-roadmap-v2"]
supersedes: "cpp-core-pointer-roadmap-v2"
created: "2026-09-08"
updated: "2026-09-08"
chunk_strategy: "semantic_heading"
estimated_tokens: 1200
---

# C++ 指针路线图增强版（C++26 preview：所有权与借用）

> 本分支是预览，标准未定稿，编译需要工具链支持；结论以最新 WD 文本为准。

## Level 10：所有权与借用（C++26 preview）

### 为什么裸观察指针仍然不够
1. 裸指针只表达"这里有个地址"，不表达指向的对象何时失效
2. 观察者与被观察者的生命周期约束只能写在注释里，编译器看不到
3. 悬垂来自"仍然可读"，而不是"看起来像空"：空指针检查治不了它
4. 迭代器失效、容器重分配、异步回调，都是同一类失效时机问题
5. 结果：跨模块传裸指针等于把安全证明交给 code review

### 静态所有权与借用预览
1. 目标是把"谁拥有、谁借用、借多久"变成可检查的声明
2. 借用有效期由契约表达，工具链在调用点上做静态匹配
3. 对已有代码的正确姿势：先用 unique_ptr 收拢所有权，再标注观察语义
4. 不要用预览语法重写能工作的 RAII 代码，收益不确定且不可移植
5. 过渡期把生命周期约定写成断言与注释，等标准定稿后再机械化

## 版本差异对照

### 相对 v2 的增量
1. v2 的 Level 0-9 全部保留，本节只追加 Level 10，不改变学习顺序
2. 新增术语：借用、有效期、观察契约，与智能指针三件套并列
3. 决策流程补一条：不拥有且可能失效时，先问能否缩短生命周期再选 weak_ptr
4. 工程建议：优先在接口边界标注，内部实现保持简单
5. 里程碑：能向他人解释"所有权收拢"和"借用标注"的先后次序

### 当前不可依赖的部分
1. 语法拼写与关键字仍在演进，任何代码示例都可能失效
2. 主流工具链的诊断覆盖不完整，报错文案不稳定
3. 与异常、协程交互的规则尚无定论
4. 因此本分支只作为路线图注记，不进入日常检索的默认排序
