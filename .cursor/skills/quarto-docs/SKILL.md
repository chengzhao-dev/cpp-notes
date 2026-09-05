---
name: quarto-docs
description: 编写结构清晰、可验证、适合 HTML 阅读的 Quarto 中文技术文档。涉及 QMD、README、章节润色和渲染时使用。
---

# Skill: quarto-docs

负责页面结构、中文表达和多文件协作；C++ 语义交给 `cpp-content`，主题细节交给 `quarto-theme`。按目录索引只读所需 reference。

## 任务路由

正文读 `authoring.md`、`writing-style-core.md`；句子衔接读 `sentence-flow.md`，润色按需读 `avoid-words.md`；图表、表格、Callout 读 `authoring-elements.md`；终端命令读 `terminal-validation.md`；结构、输出和排错读 `basics.md`、`html-output.md`、`pitfalls.md`。多文件任务先建立页面角色，再统一路线、术语和链接。不读主题 CSS，不整包加载 references。

## 常见错误（Do / Don’t）

| ✗ | ✓ |
|---|---|
| YAML `title:` + 同文本 `# H1` | 只用 `title:`，小节从 `##` |
| 代码块 `{.cpp}` | 普通围栏 `cpp` |
| 终端用 `PS>` | 演示块统一 `$` |
| 普通章写 `description:` | 仅 index/part 封面 |
| 在 `##`/`###` 前写 `---` 水平线 | H2 靠默认下边框分隔，小节前不写 `---` |
| `::: {.callout-best-practice}` 等自定义类 | 仅用内置 5 类与全局中文类型标题；自定义类会被静默丢弃（`pitfalls.md` #12） |
| 卡片堆叠 API、命令和长句 | 只保留主题、范围和学习结果 |
| 用反引号包住普通概念或卡片标题 | 只标记需要精确识别的技术对象 |

## 脚本与校验

章节骨架使用 `../cpp-content/templates/cpp-topic.qmd`；批量校验走 `run.py check`。中文 `.qmd`、Skill 和主题 CSS 使用 UTF-8 无 BOM、LF；修改后先运行 `check_encoding.py`。

## 章节主线

正文按“目标 → 前置条件 → 问题场景 → 心智模型 → 最小示例 → 实际操作 → 验证 → 常见错误 → 回顾”推进。前置条件与命令分开写，并列条件用无序列表，有先后关系的动作用有序列表。标题必须代表独立任务、概念、示例、验证或排错流程；短内容不单独创建 `###`。标题后的第一句直接兑现承诺，每段只引入一个新对象。

多文件修改先建立角色关系，再统一标题、术语、命令、链接和详略。环境、工具、命令和高级配置混杂，或命令没有目的和成功判据，都是反面案例。

真实工程章节在第一次展示源码前展示目录树。先用命令获取真实目录，再从根目录按实际层级生成 `text` 代码块；只展示当前任务需要的源码、构建文件和关键产物，不凭想象补文件，不展示缓存和 CMake 杂项。代码块前说明目的，代码块后说明结果和下一步。面向新手直接使用 Windows、WSL2 上的 Ubuntu 等具体名称；插件和编辑器内部机制不写入入门主线，必要时只链接官方文档。正文只承诺实际提供的查看、编译、运行和验证内容。
