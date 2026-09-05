# 陷阱与未定义行为

> UB · 生命周期 · 常见 bug

## UB 典型来源

- 越界访问、use-after-free、数据竞争。
- 有符号整数溢出、错误 `reinterpret_cast`。

## 调试向

- `-fsanitize=address,undefined`（ASan/UBSan）。
- `-Wall -Wextra` 作基线；`-Werror` 可选。

排错先复现，再缩小范围，最后解释根因。不要只列出 UB 名称；示例应说明触发条件、可观察结果和最短验证办法。

## 常见误区

- 返回局部变量引用。
- `vector` 扩容后仍用旧指针/迭代器。
- 多线程无同步写共享数据。

## 章节落点

- `content/debugging/common-bugs.qmd`、`sanitizers.qmd`
