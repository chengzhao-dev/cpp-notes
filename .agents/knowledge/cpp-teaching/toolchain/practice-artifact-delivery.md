---
kb_id: "cpp-practice-artifact-delivery-v1"
title: "工程应用中的 C++ 产物与 Android 影像交付"
domain: "cpp-content"
subdomain: "toolchain"
tags: [practice, executable, static_library, shared_library, android, imaging, abi, sdk, simulation]
level_range: [0, 5]
dependencies: ["cpp-library-and-executable-linking-v1"]
created: "2026-09-16"
updated: "2026-09-16"
chunk_strategy: "semantic_heading"
estimated_tokens: 650
---

# 工程应用中的 C++ 产物与 Android 影像交付

## 分册边界

`getting-started` 负责让读者配置、编译和运行通用 C++ 工程；`practice` 负责解释这些产物在真实工程中的职责。Android 影像页面是背景说明，不替代 NDK、Gradle 或 JNI 实现教程。

## Android 影像中的产物顺序

开发期先用可执行文件读取测试图像并验证算法，再把稳定的核心封装成按 ABI 提供的 `.so` SDK，通过 JNI 接入 App、相机或系统模块。可执行文件便于调试和回归，动态库承担上线集成；二者关注点不同，不能把仿真程序直接当作最终交付物。

## 动态库 SDK 的兼容边界

SDK 除 `.so` 外通常还包含头文件、模型、配置和集成文档。跨语言边界宜暴露稳定的 C 风格接口，避免直接传递复杂 C++ 对象；ABI、签名、包体和发布策略仍由具体 Android 工程决定。
