---
name: cpp-content
description: C++ 语言知识、代码风格、可编译示例。涉及 RAII、STL、模板、性能、UB、工具链、章节骨架与 verify_examples 时使用。默认中文。
---

# Skill: cpp-content

C++ 内容专家。默认 C++20、WSL2（g++/clang++）。

## 任务路由（[docs/tasks/INDEX.md](../../../docs/tasks/INDEX.md)）

| 任务 | 必读 |
|---|---|
| 写 `<part>/<chapter>` | 对应 `references/cpp/<topic>.md` + `quarto-docs` 的 authoring + writing-style-core |
| 代码风格 | `references/cpp/code-style.md` |
| 工具链/构建 | `references/cpp/toolchain.md` |

**脚本**：`scripts/scaffold_chapter.py`、`scripts/verify_examples.py`  
**工程**：`scripts/cpp/init_project.py`（bare/simple）

## 核心约定

- `-std=c++20 -Wall -Wextra`；完整示例带 `int main`
- 示例：`code/<part>/<name>.cpp` ↔ `content/<part>/`
- 文件名纯 ASCII

## 草稿 → 章节

1. 读 `references/cpp/<topic>.md` 大纲  
2. `scaffold_chapter.py --topic … --part … --title …`  
3. 扩写 qmd + 示例 → `verify_examples.py`  
4. 注册 `_quarto.yml`

## 分工

写作 → `quarto-docs`；主题 → `quarto-theme`；Git → `github-ops`。
