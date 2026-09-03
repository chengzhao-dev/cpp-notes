---
name: cpp-content
description: C++ 语言知识、代码风格、可编译示例。涉及 RAII、STL、模板、性能、UB、工具链、章节骨架与 verify_examples 时使用。默认中文。
---

# Skill: cpp-content

C++ 内容专家。默认 C++20、WSL2（g++/clang++）。全景索引见 `../_CATALOG.md`。

## 任务路由

| 任务 | 必读 |
|---|---|
| 写 `<part>/<chapter>` | 该章任务单「必读」指定的那**一个** `references/cpp/<topic>.md`（由 `run.py scope` 给出） |
| 代码风格 / 注释留白 | `references/cpp/code-style.md` |
| 工具链 / 构建 | `references/cpp/toolchain.md` |

**脚本**：`scripts/scaffold_chapter.py`、`scripts/verify_examples.py`（统一经 `run.py verify` 调用）。
**工程脚手架**：`scripts/cpp/init_project.py`（bare/simple）。

## 核心约定

- `-std=c++20 -Wall -Wextra`；完整示例带 `int main`
- 示例与章节同名对齐：`code/<part>/<name>.cpp` ↔ `content/<part>/`；需要 CMake/一键脚本的章用目录式 `code/<part>/<chapter>/`，构建产物固定落其 `build/`（不入库、**不读**、不校验）
- 只处理 `run.py scope` 给出的那一个单元，其余 `code/**` 不看
- 文件名纯 ASCII；注释写在被说明代码的上一行，逻辑块之间空一行（见 `code-style.md`）

## 草稿 → 章节

1. `run.py scope <part>/<chapter>` 取读写边界
2. `scaffold_chapter.py --topic … --part … --title …`
3. 扩写 qmd + 示例 → `run.py verify`
4. 注册 `_quarto.yml`
