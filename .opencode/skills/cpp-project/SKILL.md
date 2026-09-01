---
name: cpp-project
description: 生成最小 C++ 项目骨架（CMakeLists.txt、main.cpp、tests、CMakePresets、.clang-format/.clang-tidy）。当用户要新建 C++ 工程/示例目录、在 code/ 下创建主题示例、需要 CMake 构建骨架或 debug/release/sanitize 预设、或为章节生成可运行工程时使用。只生成内容，不涉及 IDE。默认用中文回复。
---

# Skill: cpp-project

# C++ 项目脚手架（CMake / clang 配置 / 最小布局）

## 角色定位

你负责为本仓库（及任意路径）生成**可构建的最小 C++ 项目骨架**：源码、CMake、clang 配置、可选测试与预设。只生成内容，**不涉及 IDE**。模板与 `cpp-content` 的代码风格唯一出处（`../cpp-content/references/cpp/code-style.md`：排版 LLVM / 命名 Google / 异常启用）保持一致。

## 触发条件

- 新建 C++ 工程、示例目录（如在 `code/` 下创建主题目录）
- 需要 CMake 骨架、debug/release/sanitize 预设、最小测试
- 需要 `.clang-format` / `.clang-tidy` 落到新工程

## 生成脚本

`scripts/init_project.py`：

```bash
python .opencode/skills/cpp-project/scripts/init_project.py \
  --name <name> [--dir <parent>] [--layout auto|bare|simple|full] [--readme] [--no-clang]
```

- `--name` 必填，纯 ASCII（字母/数字/-/_，建议小写）。
- `--dir` 目标父目录，默认 `code/`，支持任意路径。
- `--readme` 可选生成 README.md（默认不生成）。

## 三档布局（--layout，默认 auto）

| 布局 | 内容 | 适用场景 |
|---|---|---|
| `bare` | 仅 `main.cpp` | `code/<主题>/` 下单文件验证代码；由 `cpp-content` 的 `verify_examples.py` 直接编译 |
| `simple` | `main.cpp` + `CMakeLists.txt` + `.gitignore` | 可独立构建的最小组件 |
| `full` | `src/` + `include/<name>/` + `tests/` + `CMakePresets.json`（debug / release / sanitize） | 组合用法：库 + 测试 + 预设 |
| `auto` | 目标在本仓库 `code/` 下 → `bare`；否则 → `simple` | 默认 |

## clang 配置策略（单源防漂移）

- **仓库内生成不复制**：根目录 `.clang-format` / `.clang-tidy` 沿目录向上自动生效。
- **仓库外生成**：优先复制仓库根配置；缺失时回退到本 skill 的 `templates/clang-format` / `templates/clang-tidy`（内置副本）。
- 根配置是**唯一事实源**；改动根配置后需同步内置副本。规则说明见 `../cpp-content/references/cpp/code-style.md`。

## 与兄弟 skill 的分工（单一信息源）

- **C++ 语言知识 / 书籍章节骨架** → `cpp-content`（其 `scaffold_chapter.py` 生成 `.qmd` 章节；本 skill 生成可运行工程，两者不重叠）。
- **风格规则唯一出处** → `../cpp-content/references/cpp/code-style.md`；本 skill 的模板只是它的可执行化身。
- **写作 / 主题 / GitHub** → `quarto-docs` / `quarto-theme` / `github-ops`，互不复制。
