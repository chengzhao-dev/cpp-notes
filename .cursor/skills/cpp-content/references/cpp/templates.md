# 模板与泛型

> 函数模板 · 类模板 · concepts（C++20）

## 基础

- 模板在编译期实例化；定义通常放头文件。
- 类型推导：`auto`、`decltype`、`T&&` 转发。

## C++20 concepts

- 约束模板参数，错误信息更清晰。
- 例：`template<std::integral T>`。

## 最佳实践

- 优先标准库 + concepts，避免 SFINAE 技巧除非必要。
- CTAD（类模板参数推导）简化 `vector v{1,2,3}`。

## 章节落点

- core 卷 `references` 后或 toolchain 卷按需
