---
name: quarto-docs
description: 编写结构清晰、可验证、适合 HTML 阅读的 Quarto 中文技术文档。涉及 QMD、README、章节润色和渲染时使用。
---

# Skill: quarto-docs

负责页面结构、中文表达和多文件协作；C++ 语义交给 `cpp-content`，主题细节交给 `quarto-theme`。按目录索引只读所需 reference。

## 总原则

中文技术文档任务先遵循 `references/zh/writing-principles.md`；受众导向与可验证性是冲突时的最终裁决标准。章节组织读 `writing-style-core.md`，C++ 章节读 `cpp-chapter-writing.md`。句式、措辞、环境和项目案例通过知识库检索获取。

## 任务路由
正文读 `authoring.md`、`writing-style-core.md`；中文总原则和专项规则按上节路由读取；图表、表格和提示框读 `authoring-elements.md`；终端命令读 `terminal-validation.md`；结构、输出和排错读 `basics.md`、`html-output.md`、`pitfalls.md`。需要项目细则时用 `kb-search --domain quarto-docs`。不读主题 CSS，不整包加载 references。

## 常见错误（Do / Don’t）

| ✗ | ✓ |
|---|---|
| YAML `title:` + 同文本 `# H1` | 只用 `title:`，小节从 `##` |
| 代码块 `{.cpp}` | 普通围栏 `cpp` |
| 终端用 `PS>` | 演示块统一 `$` |
| 普通章写 `description:` | 仅 index/part 封面 |
| 在 `##`/`###` 前写 `---` 水平线 | H2 靠默认下边框分隔，小节前不写 `---` |
| 裸写 `{{< include /code/.../file >}}` | 整体包进带语言名的围栏（`cpp`/`bash`/`cmake`），否则 `#` 注释变标题（`pitfalls.md` #13） |
| `##`/`###` 手动加 `一、`、`1.1` 序号 | 标题只写任务名，`number-sections: false` 下序号会与目录和引用错位 |
| 用反引号包住仓库文件路径 | 写成可跳转链接：GitHub blob 或 `page.qmd#锚点` |
| `::: {.callout-best-practice}` 等自定义类 | 仅用内置 5 类与全局中文类型标题；自定义类会被静默丢弃（`pitfalls.md` #12） |
| 卡片堆叠 API、命令和长句 | 只保留主题、范围和学习结果 |
| 用反引号包住普通概念或卡片标题 | 只标记需要精确识别的技术对象 |

## 脚本与校验

章节骨架使用 `../cpp-content/templates/cpp-topic.qmd`；批量校验走 `run.py check`。中文 `.qmd`、Skill 和主题 CSS 使用 UTF-8 无 BOM、LF；修改后先运行 `check_encoding.py`。

## 协作原则

多文件修改先确定页面角色，再统一标题、术语、命令、链接和详略。正文只承诺实际提供且能验证的内容；具体环境、工程和命令案例留在知识库。
