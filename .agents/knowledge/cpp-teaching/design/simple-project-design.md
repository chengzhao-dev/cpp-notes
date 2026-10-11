---
kb_id: "cpp-simple-project-design-v1"
title: "简单项目的职责划分"
domain: "cpp-teaching"
subdomain: "design"
tags: [design, class, struct, abstraction, boundaries, comments]
level_range: [0, 4]
dependencies: ["cpp-language-basics-path-v1", "cpp-teaching-source-comments-v1"]
created: "2026-10-04"
updated: "2026-10-04"
chunk_strategy: "semantic_heading"
estimated_tokens: 700
---

# 简单项目的职责划分

## 具体对象优先

简单项目先以领域中已经存在的对象组织代码。`struct` 适合承载轻量值，`enum class` 表示封闭状态，`class` 用于把状态与必须同时维护的规则放在一起。不要因为使用了 C++ 就预设继承树、工厂、接口或注册表。

## 按变化原因划分边界

一个类应负责一组一起变化的状态和规则。例如棋盘的格子状态、坐标检查和不可覆盖写入可以属于 `Board`；回合与胜负可属于更高层的 `Game`；终端、文件、网络和协议格式属于外层适配。核心规则不依赖这些输入输出方式。

## 先缩小接口

只服务类内部存储的换算或检查应保持 private。只有无状态规则确实被外部多个调用方需要时，才考虑公开静态成员或自由函数。提取公共工具的前提是第二处真实、稳定且语义相同的使用，而不是名称看起来可复用。

## 注释服务使用者

文件头说明文件用途；类型说明领域含义；公开成员说明结果、失败条件和不变量；private 辅助逻辑说明前置条件。注释不解释已经由签名或语法清楚表达的类型、初始化、关键字或逐行流程。中文邻接注释优先使用简短完整句，避免架构行话。
