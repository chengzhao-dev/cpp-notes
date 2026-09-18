---
kb_id: "cpp-cpp-preprocessing-headers-linking-v1"
title: "预处理、头文件、声明与链接的边界"
domain: "cpp-content"
subdomain: "toolchain"
tags: [preprocessor, include, header, translation_unit, declaration, definition, compiler, linker, pragma_once, include_guard]
level_range: [0, 5]
dependencies: ["cpp-tooling-build-chain-v2"]
created: "2026-09-18"
updated: "2026-09-18"
chunk_strategy: "semantic_heading"
estimated_tokens: 900
---

# 预处理、头文件、声明与链接的边界

## 预处理与链接

### include 与翻译单元

预处理阶段处理 `#include`，使当前翻译单元能够看到被包含文件的内容。教学上应把它解释为“让声明在这里可见”，不能笼统说成把库的实现复制进程序。标准库头文件提供类型和函数声明，项目头文件通常提供跨源文件共享的接口声明；函数实现仍由对应源文件提供。

尖括号和引号表达不同的头文件查找意图。`#include <string>` 通常用于标准库或外部库，`#include "greeting.h"` 通常用于项目头文件。具体搜索目录由编译器实现和 `-I` 等编译参数决定，因此不能把某一种写法解释成跨工具链固定的完整路径规则。

`#include` 本身不完成链接。它不会把 `greeting.cpp` 的函数定义加入当前翻译单元，也不会替编译器找到库的二进制实现。头文件重复包含保护只控制声明文本是否重复进入翻译单元，不改变链接输入。

### 声明、定义与链接输入

函数声明告诉编译器名称、返回类型和参数类型，使调用点能够通过类型检查。函数定义提供函数体和可链接的实现。一个多文件程序可以让 `main.cpp` 包含 `greeting.h` 中的声明，让 `greeting.cpp` 提供定义，再把两个源文件分别编译并交给链接器。

调用点缺少声明时，编译阶段就无法判断调用是否合法；声明存在但链接输入缺少定义时，编译可能成功，链接阶段会报告类似 `undefined reference to makeGreeting()` 的错误。诊断文字的前后缀可能随平台和工具链变化，教学示例应保留函数名这一稳定片段。

### pragma once 的标准边界

`#pragma once` 是广泛支持的实现扩展，不属于 ISO C++ 标准。不同编译器通常会依据文件身份判断同一头文件是否已经包含，但特殊文件系统、符号链接和工具链边界属于实现行为，不能写成绝对保证。本项目采用 `#pragma once` 作为头文件重复包含保护；这是项目选择，不是语言标准要求。

需要严格 ISO 可移植性时，可以使用传统的宏 include guard。两者都只解决重复包含问题，不能替代正确的声明、定义或链接配置。
