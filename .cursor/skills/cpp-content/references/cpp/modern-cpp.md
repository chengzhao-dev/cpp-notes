# 现代 C++ 核心要点

> RAII · 智能指针 · 移动语义 · const 正确性

## RAII

- 资源生命周期绑定对象：构造获取，析构释放。
- 禁止裸 `new`/`delete`；用容器、`unique_ptr`、`shared_ptr`。

## 智能指针

| 类型 | 用途 |
|---|---|
| `unique_ptr` | 独占所有权，默认首选 |
| `shared_ptr` | 共享所有权，注意循环引用 |
| `weak_ptr` | 打破 `shared_ptr` 循环 |

## 移动语义

- 右值引用 `T&&`；`std::move` 转义为右值（不移动，只 cast）。
- 移动构造/赋值标 `noexcept` 以利容器优化。
- 拷贝昂贵、临时可转移时用移动。

## const

- 能 `const` 就 `const`；参数按值/按 const 引用传递视情况而定。

## 章节落点

- `content/memory/raii.qmd`、`smart-pointers.qmd`、`move-semantics.qmd`
