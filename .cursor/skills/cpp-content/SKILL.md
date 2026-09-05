---
name: cpp-content
description: 编写准确、可验证、渐进式的中文 C++ 教程与示例。涉及语言、标准库、工程、工具链和 C++ 示例校验时使用。
---

# Skill: cpp-content

面向初学者编写 C++20 教程，保留标准术语和行为边界；内容以读者任务为中心，不以语法清单为中心。

## 任务路由

写章先读任务单，再按主题读取一个或少数几个 `references/cpp/*.md` 和 `quarto-docs` 规则。章节结构读 `teaching-method.md`，标准术语读 `standard-chinese.md`，规则型内容读 `effective-rules.md`，示例与练习读 `examples-practice.md`，CMake 章节读 `cmake-teaching.md`；代码风格读 `code-style.md`，工具链读 `toolchain.md`。不要整包读取 references。

## 内容决策

先回答：读者遇到什么问题？完成本节后能做什么？需要先理解什么？怎样用最小示例验证？

概念按“问题场景 → 心智模型 → 规则 → 最小示例 → 行为解释 → 限制与验证”展开。规则型内容采用“建议 → 适用场景 → 原因 → 正例 → 边界 → 验证”；STL 补充复杂度、所有权和失效规则，工程按“源码 → 目标 → 构建 → 产物 → 验证”推进。涉及标准语义时标注版本，并用 `standard-chinese.md` 交叉核对术语和边界。

新建章节工程。使用仓库配置的 Python 3.12：

```powershell
python scripts/cpp/init_project.py `
  --name first-program `
  --dir code/getting-started
```

脚本会创建 `code/getting-started/first-program` 及完整工程文件。随后运行 `python scripts/agent/run.py build getting-started/first-program`，或在 WSL2 Ubuntu 中运行 `bash build-and-run.sh`。解释器规则见 [`handbook/operations/agent-operations.md`](../../../handbook/operations/agent-operations.md)。

修改示例优先运行 `python scripts/agent/run.py verify --changed`；单章使用 `python scripts/agent/run.py build <part>/<chapter>`。全局规则变更会自动回退全量；默认只输出结论，失败后才用 `--verbose`。

## 核心约定与工作流

- 使用 `-std=c++20 -Wall -Wextra`；完整示例带 `int main`。
- 示例与章节对齐：单文件用 `code/<part>/<name>.cpp`，工程章用 `code/<part>/<chapter>/`；`build/` 不入库、不读、不校验。
- 文件名使用 ASCII；注释放在代码上一行，逻辑块之间留空行。
- 先运行 `run.py scope <part>/<chapter>`，再按“引言 → 概念 → 示例 → 验证 → 排错”写作。
- 修改示例运行 `verify --changed`；改主题、全局配置或页面结构时再渲染整本 Book。

入门章节只介绍当前实际使用的编译器、CMake 和运行命令，不展开插件配置、编辑器内部机制或编译数据库。需要介绍 sanitizer 时，应放入独立的调试或未定义行为专题，不把未使用的选项注释到入门 `CMakeLists.txt` 中。
