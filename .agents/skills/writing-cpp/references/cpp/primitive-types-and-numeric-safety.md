# 基础类型与数值安全参考

本文件只保留写作路由与验收要点；标准语义、设计理由和常见边界集中在知识条目 `cpp-primitive-types-numeric-safety-v1`。

## 正文必须覆盖

- 类型大小和范围不固定；`sizeof(T)` 返回 `std::size_t`。
- `<limits>` 查询数值属性；`<cstdint>` 提供可选的明确宽度整数。
- 有符号/无符号混用风险；无符号回绕与有符号溢出的差异。
- 未定义行为的教学边界：越界、空指针、未初始化读取不能直接执行。
- 隐式转换、`static_cast`、浮点转整数和大整数转小整数的丢失风险。
- 浮点容差、`NaN`、`Inf`、整数/浮点除零差异。
- `bool` 的 0/非 0 转换与 `std::boolalpha`。
- `char` 符号性、整数文字量和 `std::size_t` 与 `int` 混用的常见陷阱。

## 教学取舍

金额使用最小货币单位的整数；折扣率和比例可使用 `double`，但必须说明精度边界。示例保持 C++20、`-Wall -Wextra -Werror` 可编译，不运行未定义行为。

需要解释“为什么”时先检索 `cpp-primitive-types-numeric-safety-v1`，不要把知识库全文复制进 skill 或 QMD。
