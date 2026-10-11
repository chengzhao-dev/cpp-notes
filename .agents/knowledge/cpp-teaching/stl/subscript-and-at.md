---
kb_id: "cpp-subscript-and-at-v1"
title: "下标与 at 的检查边界"
domain: "cpp-teaching"
subdomain: "stl"
tags: [stl, array, vector, at, operator-subscript, out-of-range]
level_range: [1, 4]
dependencies: [cpp-exception-message-format-v1]
created: "2026-10-01"
updated: "2026-10-01"
chunk_strategy: "semantic_heading"
estimated_tokens: 900
---

# 下标与 at 的检查边界

本章知识支撑 `content/standard-library/subscript-and-at.qmd`：多容器共享「未检查访问 vs 检查后抛异常」的共性，正文只用 `std::array` 演示。

## 模糊共性

同一容器上：

- **`operator[]`（下标）**：调用方已保证位置合法时的快速路径；越界是未定义行为（直至实现启用 C++26 硬化契约）。
- **`at`**：运行期检查；失败抛 `std::out_of_range`。

语法注意：写成 `cells_.[i]` 是非法语法；合法下标是 `cells_[i]`。clangd 报错先查语法，再谈越界语义。

## 族 A — 按下标（与 array 同类）

越界时 `[]` 未定义行为，`at` 抛 `std::out_of_range`：

- `std::array`
- `std::vector`
- `std::deque`
- `std::basic_string` / `std::string`
- `std::basic_string_view` / `std::string_view`
- `std::span`：本仓库锁定 C++20 时以 `[]` 为主；`at` 自 C++26 起才进入标准，正文勿假称 C++20 已有 `span::at`

## 族 B — 按键（对照，勿与族 A 混谈）

- `std::map` / `std::unordered_map`：`operator[]` 在键缺失时**插入**默认值；`at` 在键缺失时抛 `std::out_of_range`。
- `set` / `unordered_set` / `multimap`：无 `operator[]` / `at`。

## 工程用法提示

已证明下标合法后仍可用 `at` 作双保险（如棋盘 `CellIndex` 之后）。契约失败文案见标识 `cpp-exception-message-format-v1` 的知识文件。姊妹仓井字棋 `MarkAt` 在 `IsValid` 失败时显式抛 `std::out_of_range`，再读 `cells_.at(...)`。
