---
kb_id: "cpp-static-analysis-boundaries-v1"
title: "C++ 静态检查的项目边界"
domain: "cpp-teaching"
subdomain: "toolchain"
tags: [clang-tidy, clang-format, clangd, header-filter, system-headers, compile-commands, cmake, dependencies]
level_range: [0, 5]
dependencies: ["cpp-tooling-build-chain-v2"]
created: "2026-10-01"
updated: "2026-10-01"
chunk_strategy: "semantic_heading"
estimated_tokens: 1900
---

# C++ 静态检查的项目边界

## 日常门禁检查谁

项目质量门禁应把“传入 clang-tidy 的项目源文件”和“项目自己的头文件”作为范围。`compile_commands.json` 记录所有 CMake 编译单元的真实参数，但不表示数据库中的第三方源码都必须接受本项目的诊断规则。GoogleTest、系统库和生成目录属于依赖或构建环境，应由其自身维护或在单独的依赖审计中检查。

日常命令不传 `--system-headers`。该选项会扩大到系统头文件，不能用来实现“只检查自己库”。`--header-filter` 只决定头文件诊断的显示范围；它不能替代明确的源文件清单，也不能把依赖变成项目代码。

## CMake 与头文件标记

项目自己的 include 目录保持普通 `target_include_directories(... PUBLIC|PRIVATE ...)`，这样项目头文件能够进入诊断。第三方头文件用 imported target 提供的 system include，或在项目确实控制依赖目标时使用 CMake 的 `SYSTEM` 语义。这样做是噪声边界，不是安全证明：传递到项目接口的类型仍要由项目代码负责验证。

`--exclude-header-filter` 可补充排除构建树中的 FetchContent 目录，但不应依赖它掩盖错误的源文件清单。先排除不属于项目的编译单元，再用 header filter 控制项目头文件诊断，最后才处理依赖头的显示噪声。

## 如何读“warnings generated”

clang-tidy 的汇总数字是实例化和预处理路径的计数，不等于项目有同等数量的独立问题。看到大量数字时，先看诊断行中的绝对路径和检查名，按项目源文件、项目头文件、第三方头文件、系统头文件和汇总行分类。没有 `--system-headers` 时，不能把数字直接称为“系统库警告”。

## 动态下标与接口契约

`cppcoreguidelines-pro-bounds-constant-array-index` 是保守的静态规则，不理解跨函数的 `IsValid(position)` 前置条件。它指出动态 `operator[]` 缺少工具可见的边界证明，并不等同于编译错误或必然越界。

公共查询接口不应把非法坐标转换为 `std::size_t` 后再访问数组。先验证坐标，再使用 `std::array::at` 或项目明确规定的边界辅助函数；测试负数、行越界和列越界。只有在边界证明已经集中且访问方式确实安全时，才允许最窄范围的 `NOLINT(cppcoreguidelines-pro-bounds-constant-array-index)`，不能用全局关闭替代接口安全。

## 工具职责

`clang-format` 只检查排版；`clang-tidy` 负责静态规则；`clangd` 使用编译数据库提供编辑器诊断。编辑器的实时噪声不能替代脚本门禁，脚本也不应为了迎合某个未配置编译数据库的编辑器而扩大依赖范围。
