---
kb_id: "cpp-tooling-build-chain-v2"
title: "C++ 构建与工具链决策依据"
domain: "cpp-content"
subdomain: "toolchain"
tags: [toolchain, cmake, compiler_flags, sanitizer, warnings, optimization, header]
level_range: [0, 9]
created: "2026-09-09"
updated: "2026-09-09"
chunk_strategy: "semantic_heading"
estimated_tokens: 700
---

# C++ 构建与工具链决策依据

## 最小构建链

本项目在 Windows 的 WSL2 Linux 环境中使用 GCC 或 Clang 与 CMake。先让最小程序编译和运行，再把命令固化为 CMake 目标；MSVC 仅作为对照，不是主线前置条件。

## 编译与诊断

示例使用 C++20、常见警告和可重复的构建配置。Sanitizer 用于调试和未定义行为专题；不要把未启用的诊断选项留在入门示例中。优化必须先测量基线，再报告收益、代价和适用范围。

## CMake

用目标属性表达语言版本、包含路径、编译选项和链接依赖，避免依赖全局变量。配置、构建和运行是独立步骤，每一步都应有可观察产物。
