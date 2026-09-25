---
kb_id: "cpp-naming-format-v1"
title: "C++ 命名与格式化决策依据"
domain: "writing-cpp"
subdomain: "style"
tags: [cpp, naming, format, clang_format, clang_tidy, google, qt, webkit, llvm, lower_camel, pascal_case, include_order, header_order]
level_range: [0, 9]
created: "2026-09-15"
updated: "2026-09-15"
chunk_strategy: "semantic_heading"
estimated_tokens: 620
---

# C++ 命名与格式化决策依据

## 标准差异

Google C++ Style Guide 当前规定函数使用 `PascalCase`，变量、参数和类成员使用 `snake_case`，类私有成员追加 `_`，常量使用 `k` 加混合大小写。它的价值主要在于 include 顺序、排版和常量约定，不是函数与变量统一使用小驼峰。

Qt Coding Style 与 WebKit Code Style Guidelines 对类使用首字母大写，对函数和变量使用首字母小写的 camelCase，因此更接近本项目希望函数和变量易于连续阅读的目标。LLVM Coding Standards 的函数使用小驼峰，但当前变量命名并非统一小驼峰，不能作为整套混合规则的唯一依据。本文件选择有明确来源的组合，而不是声称某个主流指南默认采用本项目规则。

## 项目规则

函数和方法使用小驼峰，并以动词或动词短语表达动作。变量、参数和普通成员使用小驼峰。类私有成员使用小驼峰并以 `_` 结尾。类、结构体、枚举和类型别名使用 `PascalCase`。常量使用 `kPascalCase`。命名空间使用 `lower_case`。宏使用 `UPPER_CASE`。访问器和修改器使用 `getCount()`、`setCount()`，不混入另一套下划线命名。

小驼峰让函数调用、局部变量和参数在句子式阅读中保持相似节奏，同时用类型的大驼峰和常量的 `k` 前缀保留边界。私有成员后缀继续显示类内部状态，常量前缀继续沿用 Google 的公开约定。规则由 `.clang-tidy` 配置，其中该工具的配置值 `camelBack` 对应本项目所说的小驼峰。代码审查负责处理工具无法判断的语义质量。

## 格式化边界

`.clang-format` 使用 `BasedOnStyle: Google`、`Standard: c++20`、80 列和 2 空格缩进，因此 include 分组、组内排序和基础排版直接复用 Google 风格。Google 的 include 顺序是相关头文件、C 系统头文件、C++ 标准库头文件、其他库头文件、项目头文件，各组之间保留一个空行。

本项目保留 C++20、libc++、`.cpp` 与 `.h` 扩展名、`#pragma once` 和异常。这些是有意调整：Google 使用 `.cc`、include guard 并限制异常，但本项目需要与现有 Clang/LLVM、CMake 和教学示例保持一致。命名与排版分离配置还能避免把 `clang-format` 误当成命名检查器。

## 参考入口

- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- [WebKit Code Style Guidelines](https://webkit.org/code-style-guidelines/)
- [LLVM Coding Standards](https://llvm.org/docs/CodingStandards.html)
