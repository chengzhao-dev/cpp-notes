---
kb_id: "cpp-exception-message-format-v1"
title: "异常与错误文案规范"
domain: "cpp-teaching"
subdomain: "conventions"
tags: [exceptions, error-messages, out-of-range, logging]
level_range: [0, 5]
dependencies: [cpp-naming-format-v1]
created: "2026-10-01"
updated: "2026-10-01"
chunk_strategy: "semantic_heading"
estimated_tokens: 650
---

# 异常与错误文案规范

本文件与姊妹仓 `bg-exception-message-format-v1` 对等：规定教学代码何时用异常、何时用结果类型，以及 `what()` 文案。本仓启用异常；不用 Abseil/glog 等日志框架讲课。

## 何时抛异常

- **契约违反 / 硬边界**：前置条件失败（越界下标、缺失键的检查路径）可抛 `std::out_of_range` 等标准异常。
- **业务结果**：可恢复的拒绝用结果类型或布尔/枚举返回，不把正常分支写成 `throw`。
- **进程边界**：`main` 可捕获后写 `std::cerr`；不把异常当正常循环控制流。

## what() 文案格式

1. **语言**：英文。中文留给面向读者的 CLI/教程旁白。
2. **句式**：`<ApiName>: <subject> <reason>`，单行。
3. **示例**：`MarkAt: position is outside the board`。
4. **禁止**：中英混杂、堆栈式长文、用日志宏代替异常消息。

容器上 `operator[]` 与 `at` 的语义对照见标识 `cpp-subscript-and-at-v1` 的知识文件。
