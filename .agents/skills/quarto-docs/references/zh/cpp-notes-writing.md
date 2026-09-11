# C++ Notes 项目写作边界

本项目面向刚开始学习 C++ 的中文读者，运行环境以 Linux 为准，Windows 读者通过 WSL2 获得同样环境。正文优先使用 C++20 语义，示例必须能编译、运行并与正文输出一致。

## 章节与示例

- 每章只解决一个读者任务，按“问题场景 → 心智模型 → 规则 → 最小示例 → 行为解释 → 限制与验证”推进。
- 章节文件位于 `content/<part>/`；对应示例位于 `code/<part>/`，单文件或同名工程均可。
- 任务状态和专项必读以 `.agents/skills/cpp-content/references/tasks/<part>.md` 为准，不在正文复制路线状态。

## 可验证性

- 命令块标明 `bash`、`powershell` 或 `cmake`；输出单独放在 `text` 块，并只写实测结果。
- C++ 示例按项目约定使用 `-std=c++20 -Wall -Wextra` 校验；完整示例包含 `int main`。
- 不读取或引用 `code/**/build/**`、`_book/**` 和缓存目录；这些是本地生成物。
- 修改中文正文、skill 或主题 CSS 后检查 UTF-8 无 BOM、LF；影响主题或 `_quarto.yml` 时执行整本渲染。
