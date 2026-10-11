---
kb_id: "cpp-naming-cases-v1"
title: "标识符命名正反对照"
domain: "cpp-teaching"
subdomain: "cases"
tags: [cpp, naming, google, pascal_case, snake_case]
level_range: [0, 9]
dependencies: ["cpp-naming-format-v1"]
created: "2026-09-29"
updated: "2026-09-29"
chunk_strategy: "semantic_heading"
estimated_tokens: 350
---

# 标识符命名正反对照

命名规则见标识 `cpp-naming-format-v1` 的知识文件；本文件保存正反对照，检索单元是「正确 + 不佳 + 改写」。

## 歧义映射命名对照

映射函数的名字必须让读者看出源端或目标端角色；单独的 `Of` / `To` 短后缀看不出两端是什么，禁止使用（依据 Google「descriptive；eschew abbreviation」）：

```text
不佳（MarkOf 看不出映射的两端）：
Mark MarkOf(Player player);

改写（名字同时含源端与目标端角色）：
CellState PlayerToCellState(Player player);
```

```text
不佳（To 悬空，目标类型只能去签名里找）：
std::string To(const Board& board);

改写（目标端进名字）：
std::string BoardToString(const Board& board);
```

## 访问器命名对照

```text
不佳（同一页混用 snake_case 访问器与 PascalCase 普通函数）：
int getX() const;
void Apply(Move move);

改写（访问器与普通函数统一 PascalCase）：
int X() const;
void Apply(Move move);
```

## 正确形态正例

```cpp
// 谓词：PascalCase，返回 bool，一眼可读。
constexpr bool IsValid(Position position);

// 映射：源端与目标端都在名字里。
CellState PlayerToCellState(Player player);
```

正例的判定条件：谓词 `Is/Are/Has` 开头；映射函数含源端或目标端角色；类型 PascalCase、变量与参数 snake_case、常量与枚举子 `k` 前缀。
