# C++ Notes 项目写作边界

本项目面向刚开始学习 C++ 的中文读者，运行环境以 Linux 为准，Windows 读者通过 WSL2 获得同样环境。项目自称使用“这份笔记”，不使用“本书”。正文优先使用 C++20 语义，示例必须能编译、运行并与正文输出一致。

## 章节与示例

- 每章只解决一个读者任务。章节组织遵循 `writing-style-core.md`，C++ 教学递进遵循 `cpp-chapter-writing.md`。
- 章节文件位于 `content/<part>/`，对应示例位于 `code/<part>/`，单文件或同名工程均可。
- 任务状态和专项必读以 `.agents/skills/cpp-content/references/tasks/<part>.md` 为准，不在正文复制路线状态。

## 全书排版约定

行内代码、文档元素和代码块格式统一以 `references/quarto/authoring.md` 与 `references/quarto/terminal-validation.md` 为准，本文件不维护第二套规则。

## 可验证性

- C++ 示例按项目约定使用 `-std=c++20 -Wall -Wextra` 校验，完整示例包含 `int main`。
- 不读取或引用 `code/**/build/**`、`_book/**` 和缓存目录。这些是本地生成物。
- 修改中文正文、skill 或主题 CSS 后检查 UTF-8 无 BOM、LF。影响主题或 `_quarto.yml` 时执行整本渲染。
