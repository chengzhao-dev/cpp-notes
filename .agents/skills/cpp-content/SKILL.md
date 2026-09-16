---
name: cpp-content
description: 编写准确、可验证、渐进式的中文 C++ 教程与示例。涉及语言、标准库、工程、工具链和 C++ 示例校验时使用。
metadata:
  short-description: 编写中文 C++20 教程与可运行示例
---

# Skill: cpp-content

面向初学者编写 C++20 教程，保留标准术语与行为边界。内容以读者任务为中心，不以语法清单为中心。页面结构交给 `quarto-docs`，样式交给 `quarto-theme`。

## 适用场景

- 新写或重构 C++ 章节、示例、练习与速查表，并校验示例可编译、输出与正文一致。
- **不适用**：主题 CSS（转 `quarto-theme`）、git 与发布（转 `github-ops`）、Agent 结构维护（转 `agent-ops`）。

## 任务路由

| 要做的事 | 读取 |
| --- | --- |
| 开工前定位作用域 | `& .agents/skills/agent-ops/scripts/run.ps1 scope <part>/<chapter>` |
| 章节设计与示例递进 | `references/cpp/teaching-method.md` |
| 语言 / 标准库 / 内存与模板要点 | `references/cpp/cpp.md`、`references/cpp/stl.md`、`references/cpp/modern-cpp.md`（按主题只读一个） |
| 术语核对、规则型内容、示例练习、代码风格 | `references/cpp/cpp.md`、`references/cpp/effective-rules.md`、`references/cpp/examples-practice.md`、`references/cpp/code-style.md` |
| 工程、CMake、工具链章写作与依据 | `references/cpp/engineering.md`、`references/cpp/cmake-teaching.md`。决策依据用 `run.py kb-search "<查询>" --domain cpp-content` |

## P0 硬约束

1. 写章前先读对应任务单，每章只解决一个读者任务。不整包读取 `references/`。
2. 示例必须可编译可运行：`-std=c++20 -Wall -Wextra`，完整示例带 `int main`，片段首行标 `// 片段`。代码命名、include 顺序和文件用途注释以 `references/cpp/code-style.md` 为准。
3. 正文里的输出必须来自实测。拿不到结果就不写、不伪造。
4. 示例路径与章节对齐：需要重复编译运行的章节使用 `code/<part>/<chapter>/`，至少提供源码和一个 `build-and-run.sh`。直接编译脚本调用 `clang++`，CMake 工程脚本依次配置、构建和运行。只有不进入重复构建流程的片段或无工程文件可省略脚本。单入口工程的 `main.cpp` 放工程根；消费端增长为多文件后再建带 `CMakeLists.txt` 的 `app/`。一章可登记多个独立工程，但每个工程只突出一个教学中心。模板在 `templates/projects/`，`build/` 不入库、不读、不校验。
5. 标注 C++ 版本并用 `cpp.md` 核对译名。正文按正确流程展开，warning/error 仅放 `常见错误`。其中的每个症状用 `###`，按“定位 → 修复 → 验证”的有序流程处理，修复动作必须点名具体对象，成功判据放在验证步骤。构建章以 CMake 配置和 `cmake --build <dir>` 为读者动作，后端工具只有直接执行时才进入正文。章节收尾、Callout、排错和回顾格式以 `quarto-docs` 对应 reference 为准，这里不复制第二套规则。

## 工作流程

1. 跑 `run.py scope <part>/<chapter>`，只读 UNIT 与 READ 所列文件。
2. 回答四问：读者遇到什么问题、完成后能做什么、需先理解什么、怎样最小验证。
3. 按「问题场景 → 心智模型 → 规则 → 最小示例 → 行为解释 → 限制与验证」组织正文。
4. 新建工程用 `init_project.py --name <name> --dir code/<part> --layout single|multi|static-library|shared-library`。模板会把目录名派生为 CMake 的 PascalCase 工程名。改示例跑 `run.ps1 verify --changed`，单章用 `run.ps1 build <part>/<chapter>`。

## 完成判据

- [ ] `verify --changed` 通过，正文承诺的输出与实测一致。
- [ ] 术语与版本标注对 `cpp.md` 无冲突。入门章节只讲当前任务用到的工具与命令。
