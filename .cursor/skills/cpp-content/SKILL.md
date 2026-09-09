---
name: cpp-content
description: 编写准确、可验证、渐进式的中文 C++ 教程与示例。涉及语言、标准库、工程、工具链和 C++ 示例校验时使用。
metadata:
  short-description: 编写中文 C++20 教程与可运行示例
---

# Skill: cpp-content

面向初学者编写 C++20 教程，保留标准术语与行为边界；内容以读者任务为中心，不以语法清单为中心。页面结构交给 `quarto-docs`，样式交给 `quarto-theme`。

## 适用场景

- 新写或重构 C++ 章节、示例、练习与 cheatsheet，并校验示例可编译、输出与正文一致。
- **不适用**：主题 CSS（转 `quarto-theme`）、git 与发布（转 `github-ops`）、Agent 结构维护（转 `agent-ops`）。

## 任务路由

| 要做的事 | 读取 |
| --- | --- |
| 开工前定位作用域 | `python .cursor/skills/agent-ops/scripts/run.py scope <part>/<chapter>` |
| 章节设计与示例递进 | `references/cpp/teaching-method.md` |
| 语言 / 标准库 / 内存与模板要点 | `references/cpp/cpp.md`、`references/cpp/stl.md`、`references/cpp/modern-cpp.md`（按主题只读一个） |
| 术语核对、规则型内容、示例练习、代码风格 | `references/cpp/cpp.md`、`references/cpp/effective-rules.md`、`references/cpp/examples-practice.md`、`references/cpp/code-style.md` |
| 工程、CMake、工具链章写作与依据 | `references/cpp/engineering.md`、`references/cpp/cmake-teaching.md`；决策依据用 `run.py kb-search "<查询>" --domain cpp-content` |

## P0 硬约束

1. 写章前先读对应任务单，每章只解决一个读者任务；不整包读取 `references/`。
2. 示例必须可编译可运行：`-std=c++20 -Wall -Wextra`，完整示例带 `int main`，片段首行标 `// 片段`。
3. 正文里的输出必须来自实测；拿不到结果就不写、不伪造。
4. 示例路径与章节对齐：单文件 `code/<part>/<name>.cpp`，工程章 `code/<part>/<chapter>/`；`build/` 不入库、不读、不校验。
5. 涉及标准语义时标注 C++ 版本，并用 `cpp.md` 核对译名。

## 工作流程

1. 跑 `run.py scope <part>/<chapter>`，只读 UNIT 与 READ 所列文件。
2. 回答四问：读者遇到什么问题、完成后能做什么、需先理解什么、怎样最小验证。
3. 按「问题场景 → 心智模型 → 规则 → 最小示例 → 行为解释 → 限制与验证」组织正文。
4. 新建工程用 `python .cursor/skills/python-tools/scripts/scaffold/init_project.py --name <name> --dir code/<part>`；改示例跑 `run.py verify --changed`，单章用 `run.py build <part>/<chapter>`。

## 完成判据

- [ ] `verify --changed` 通过，正文承诺的输出与实测一致。
- [ ] 术语与版本标注对 `cpp.md` 无冲突；入门章节只讲当前任务用到的工具与命令。
