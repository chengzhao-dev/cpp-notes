---
kb_id: "cpp-naming-format-v1"
title: "C++ 命名与格式化决策依据"
domain: "cpp-teaching"
subdomain: "style"
tags: [cpp, naming, format, clang_format, clang_tidy, google, pascal_case, snake_case, include_order, header_order]
level_range: [0, 9]
created: "2026-09-15"
updated: "2026-09-28"
chunk_strategy: "semantic_heading"
estimated_tokens: 620
---

# C++ 命名与格式化决策依据

## 主标准与命名表

本仓标识符命名以 [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) 为唯一主标准：类型与函数使用 `PascalCase`，变量、参数和类数据成员使用 `snake_case`，类私有成员追加 `_` 结尾，常量与枚举子使用 `k` 加 PascalCase，命名空间使用 `lower_case`，宏使用 `UPPER_CASE`。查询型访问器与修改器同样使用 PascalCase，与普通函数保持同一套规则，不在教学代码里混用两套函数命名。

函数与变量小驼峰（Qt、WebKit 组合）曾是本仓的选型，该历史决策已于 2026-09-28 废止：Qt Coding Style 与 WebKit Code Style Guidelines 不再作为命名依据，两仓（cpp-notes 与 cpp-board-games）统一按 Google 命名落地。规则由 `.clang-tidy` 的 `readability-identifier-naming` 配置；代码审查负责处理工具无法判断的语义质量。

## 有意偏离

除命名表外，本仓保留以下与 Google 指南的偏离：`.cpp` 与 `.h` 扩展名（不用 `.cc`）、`#pragma once`（不用 include guard）、C++20、异常可用。它们与现有 Clang/LLVM、CMake 和教学示例保持一致。命名与排版分离配置，避免把 `clang-format` 误当成命名检查器。

## 格式化边界

`.clang-format` 使用 `BasedOnStyle: Google`、`Standard: c++20`、80 列和 2 空格缩进，因此 include 分组、组内排序和基础排版直接复用 Google 风格。Google 的 include 顺序是相关头文件、C 系统头文件、C++ 标准库头文件、其他库头文件、项目头文件，各组之间保留一个空行。

## 参考入口

- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [LLVM Coding Standards](https://llvm.org/docs/CodingStandards.html)
