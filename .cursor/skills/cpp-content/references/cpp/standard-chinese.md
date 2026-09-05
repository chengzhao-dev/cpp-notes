# C++ 标准术语与中文资料

本文件规定中文 C++ 教程如何处理标准术语、版本和中文资料，避免译名漂亮但语义不准确。

## 术语写法

首次出现时使用“中文名称（英文名称）”，必要时补充标准拼写。例如：资源获取即初始化（Resource Acquisition Is Initialization，RAII）、未定义行为（undefined behavior，UB）。后续固定使用一种中文名称，并保留英文术语作为检索入口。

普通概念不用反引号；命令、路径、文件名、关键字、API、配置键和代码字面量保留反引号。不要把整句说明或卡片标题包进反引号。

## 版本边界

涉及 C++20、C++23 或 C++26 的特性必须标注版本。正文说明读者当前需要的行为和用法，参考链接补充完整限制；不要把实验性或较新标准特性写成所有编译器都支持。

标准库内容至少核对：

- 参数和返回值的语义；
- 复杂度和异常保证；
- 生命周期、所有权和迭代器失效；
- 特性首次进入的标准版本；
- GCC、Clang 或 CMake 当前工具链的支持边界。

## 中文资料的使用层次

中文 cppreference 和 CMake 中文文档适合查找中文术语、页面结构和常见说明。它们与英文原版、ISO C++ 草案和工具官方文档交叉确认后，才作为正文事实依据。中文资料存在译名差异时，选择最容易理解且能链接到英文术语的表达。

不要为了追求“标准”把正文写成规范条文。先给使用场景和最小示例，再在“限制”或“深入”段落说明精确语义。

## 推荐校验入口

| 目标 | 入口 |
|---|---|
| 语言和标准库语义 | [cppreference](https://en.cppreference.com/w/cpp/language) / [中文站](https://zh.cppreference.com/w/cpp/language) |
| 标准草案原文 | [eel.is C++ draft](https://eel.is/c++draft/) |
| 设计与接口原则 | [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) |
| CMake 语义 | [CMake 官方文档](https://cmake.org/cmake/help/latest/) / [中文文档](https://cmake.com.cn/cmake/help/latest) |

资料入口用于继续查阅，不代替当前章节对结论、命令和成功判据的说明。
