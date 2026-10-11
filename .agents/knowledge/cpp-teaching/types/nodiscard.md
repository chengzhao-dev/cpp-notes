---
kb_id: "cpp-nodiscard-v1"
title: "nodiscard 属性的教学边界"
domain: "cpp-teaching"
subdomain: "types"
tags: [nodiscard, attribute, return-value, result-type, clang-tidy, selection]
level_range: [1, 5]
dependencies: ["cpp-language-basics-path-v1", "cpp-primitive-types-numeric-safety-v1"]
created: "2026-09-30"
updated: "2026-09-30"
chunk_strategy: "semantic_heading"
estimated_tokens: 600
---

# nodiscard 属性的教学边界

## 为什么单独成页

### 独立的心智模型与工具链检查

`[[nodiscard]]` 是属性而非类型修饰：编译器对“标注函数的返回值被丢弃”发警告，把“结果不能无视”从文档变成编译期检查。它有独立的工具链检查（clang-tidy `modernize-use-nodiscard`，clangd 在编辑器内实时报告），塞进返回值速查会冲淡选型表，也不属于 const 家族，故单独成页。

### 页面位置与前置

页面跟在 `return-value-guide` 之后、仍属 language-basics 分册：先有“结果类型表达成败”的返回值选型，再讲“调用方不能无视这个结果”的属性标注。前置章节已覆盖函数调用、`enum class` 与 `static_cast`。

## 采纳范围（与工程仓库一致）

标注面向“结果携带信息、忽略会出错”的函数：查询型 const 成员（`MarkAt`、`Status`）与结果型 API（`Apply` → `ApplyResult`）；不在几乎所有非 void 函数上无差别铺开，标注的价值来自稀缺。有意丢弃用 `static_cast<void>` 写明，不用编译选项全局关闭警告。姊妹仓库的采纳决策见标识 `bg-google-cpp-style-v1` 的知识文件。

## 教学边界

页面不展开属性语法全集（自定义属性、`[[maybe_unused]]` 等留给后续主题）；示例只覆盖“标注 → 正常处理结果 → 有意丢弃写明”三种形态。
