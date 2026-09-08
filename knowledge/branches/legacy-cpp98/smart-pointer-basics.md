---
kb_id: "cpp-core-pointer-roadmap-v1"
title: "C++ 智能指针入门（C++98/03 经典写法）"
domain: "cpp_core"
subdomain: "memory_pointers"
tags: [pointer, smart_pointer, auto_ptr, RAII, memory]
level_range: [4, 5]
dependencies: ["cpp-core-pointer-roadmap-v0"]
created: "2024-05-01"
updated: "2024-05-01"
chunk_strategy: "semantic_heading"
estimated_tokens: 900
---

# C++ 智能指针入门（C++98/03 经典写法）

> 本分支保留历史写法，用于对照现代代码；不要在新代码里照抄 auto_ptr。

## 为什么 C++98 需要智能指针

### 裸指针的释放责任
1. new 出来的对象必须有人 delete，否则泄漏
2. 构造函数之后、delete 之前若提前 return 或抛异常，delete 执行不到
3. 多个持有者共享一个指针时，谁 delete 都可能是错的
4. 数组要用 delete[]，标量用 delete，写错即未定义行为
5. 典型症状：只在长时间运行后出现的内存增长，以及偶发的二次释放崩溃
6. 归属清晰的前提是每一条 delete 路径都能静态看出，异步回调里这条通常断

## auto_ptr：C++98 的唯一标准选择

### 语义与限制
1. std::auto_ptr 用所有权转移表达独占：拷贝即移交
2. 拷贝之后原对象变成空指针，再解引用即未定义行为
3. 因为拷贝会改对方，auto_ptr 不能放进 vector 等标准容器
4. 没有 make 辅助函数，只能写成 std::auto_ptr<T>(new T(args))
5. 异常安全只在构造那一步生效，转移之后责任已易手

### 手工写引用计数为什么不够
1. 自己加一个 int count 字段，需要在每次拷贝时递增、每次销毁时递减
2. 拷贝赋值要先增新再减旧，否则自赋值会把对象释放掉
3. 多线程下递增递减不是原子的，计数本身就会竞态
4. 循环引用让计数永远不归零，这就是后来 weak_ptr 的动机

## 里程碑

### 能对照解释新旧写法
1. 能说明 auto_ptr 为什么被废弃：拷贝语义与容器要求冲突
2. 能解释 unique_ptr 删掉拷贝、只留移动之后解决了哪一条
3. 能指出本文件里所有做法在现代 C++ 中的替代品
