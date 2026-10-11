# .agents/context/ 现行事实与规范

本目录回答「现在是什么、现在就该照做的规范」，是每轮任务的主流程区。按任务打开其中一个文件，不整目录注入。「为什么这样定、否决过什么」在 `../knowledge/`（经 `kb_id` 取用）；「这一步怎么做」在 `../skills/` 的对应技能。文件名与目录名一律纯 ASCII kebab-case。

frontmatter 与检索规范与知识库同一标准（`kb_id` 一律 `cpp-*` 前缀、`##`/`###` 两层分块、Parent 4000 Token 上限），权威定义见 `../knowledge/KNOWLEDGE.md`「文件规范」与「检索不变量」。

## 按任务打开哪个文件

| 任务 | 文件 |
| --- | --- |
| 项目现状、当前分册范围、阅读顺序来源、公开面 | `project.md` |
| 目录结构、章节与示例的对应、站点组成 | `architecture.md` |
| 构建链、clangd、CMake 用法与诊断边界 | `development.md` |
| Google C++ 命名、头文件与偏离白名单 | `conventions/cpp-style.md` |
| 注释（层级、职责、CMake 与 sh 的异同、键值配置） | `conventions/comments.md` |
| 类内与命名空间声明顺序 | `conventions/declaration-order.md` |
| 异常边界与 `what()` 文案 | `conventions/exceptions.md` |
| 列表初始化与窄化转换的取舍 | `conventions/list-initialization.md` |
| clang-tidy 门禁范围与诊断边界 | `conventions/static-analysis.md` |
| 章节骨架、段落、句法、中文质量、语域、密度、qmd 元素、practice 页面分层 | `conventions/writing/`（按文件名取） |
| Mermaid、坐标图、渲染行为与失效模式 | `conventions/rendering/`（按文件名取） |
| C++ 中文术语对照、全书统一术语与替换规则 | `glossary/cpp-terms.md`、`glossary/project-terms.md` |

## 收录新规范

成段材料的落点计划流程见 `../skills/governing-agents/references/intake.md`；新 `kb_id` 的最小闭环（含 `eval_set.py` 补查询）见 `../knowledge/KNOWLEDGE.md`「新增知识的最小闭环」。
