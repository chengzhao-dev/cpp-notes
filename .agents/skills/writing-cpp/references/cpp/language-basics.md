# C++ 语言基础教学顺序

本文件只规定 `language-basics` 的页面边界、示例递进和后续顺序。基础类型的标准语义与设计原因见 `primitive-types-and-numeric-safety.md` 及知识条目 `cpp-primitive-types-numeric-safety-v1`；页面骨架遵循 `quarto-docs`。

## 基础类型与变量

`types-and-variables` 以“基础类型与变量”为标题，只建立“值属于类型，名字绑定变量”的心智模型。生活化场景只能在引言中说明为什么程序需要保存数量、比例、状态和字符；正文、标题和完整示例使用领域中性的变量名与输出。基础类型页覆盖 `int`、`double`、`bool`、`char`、声明、初始化、赋值以及全局作用域和块作用域；不得使用 `std::string`，字符串留到 `arrays-strings`。

`initialization-and-type-inference` 独立讲 C++11 列表初始化、值初始化、赋值、`auto` 和初始化列表推导。`auto` 是编译期推断，不是动态类型；花括号拒绝窄化转换。普通变量初始化默认使用 `{}`，`auto` 初始化统一使用 `auto value = expression;`，避免把 `initializer_list` 细节误当成常规写法。

## 常量与数值安全

`constants` 讲“常量与配置”，使用领域中性的上限、阈值和比例说明 `const`、`constexpr`、初始化要求和命名。指针常量、成员常量和复杂配置对象后置。

`type-safety-and-numeric-bounds` 承载基础类型相关边界：`sizeof`、`std::size_t`、`<limits>`、`<cstdint>`、符号混用、溢出与未定义行为、`static_cast`、浮点精度、`NaN`、`Inf`、除零和 `bool` 输出。危险行为只用注释或可观察的安全边界演示。

## 页面与构建边界

语言基础分册不重复 CMake 配置。各章保持扁平源文件，由分册根 `CMakeLists.txt` 收集成同名可执行文件。正文用最小片段解释规则，完整源码位置和观察重点合并进 `## 本章回顾`。

## 后续顺序

语言基础按“基础类型与变量 → 初始化与推断 → 常量 → 数值安全 → 运算 → 控制 → 函数 → 字符串与数组 → 自定义类型与引用”推进。新章节必须先登记任务矩阵，前一章已讲过的语法不复制完整示例。

## 验证边界

新增或拆分页面后运行 `verify --changed`、编码检查、`check --profile fast` 和 `render`；知识库改动后运行 `kb-index --rebuild`、`kb-check` 与 `kb-eval`。正文承诺的输出必须来自实测，任务矩阵状态必须与当前文件一致。
