---
kb_id: "cpp-tooling-build-chain-v2"
title: "C++ 构建与工具链决策依据"
domain: "cpp-content"
subdomain: "toolchain"
tags: [toolchain, cmake, compiler_flags, sanitizer, warnings, optimization, header]
level_range: [0, 9]
created: "2026-09-09"
updated: "2026-09-11"
chunk_strategy: "semantic_heading"
estimated_tokens: 296
---

# C++ 构建与工具链决策依据

## 最小构建链

本项目在 Windows 的 WSL2 Linux 环境中使用 GCC 或 Clang 与 CMake。先让最小程序编译和运行，再把命令固化为 CMake 目标。MSVC 仅作为对照，不是主线前置条件。

## 编译与诊断

示例使用 C++20、常见警告和可重复的构建配置。Sanitizer 用于调试和未定义行为专题。不要把未启用的诊断选项留在入门示例中。优化必须先测量基线，再报告收益、代价和适用范围。

## CMake

用目标属性表达语言版本、包含路径、编译选项和链接依赖，避免依赖全局变量。配置、构建和运行是独立步骤，每一步都应有可观察产物。

### 版本要求只写在构建配置里

`cmake_minimum_required` 是版本要求的唯一落点。构建配置、脚手架模板和示例脚本不写宿主发行版名与其版本号。发行版会随时间升级，写死的名称与版本在读者照着操作时必然过期，还会让同一条要求同时存在于正文、脚本和模板三处，三份记录很容易互相矛盾。

版本号的取值与本机实测的 CMake 基线保持一致，正文、示例和脚手架使用同一个数字，避免读者按环境章节完成安装后又遇到版本分叉。需要交代某条要求来自哪个环境时，写“与本机实测基线一致”，真正的版本号留在一次实测输出的 `text` 块里，不复制进配置文件。
