# GitHub CI

CI 只覆盖文档：Quarto 渲染与文档后处理脚本。C++ 示例编译只在本地按需验证，不进 CI。

| workflow | 触发 | 内容 |
| --- | --- | --- |
| `render-check.yml` | PR / 手动 | `quarto render` + `defer_mermaid.py` 后处理 |
| `pages.yml` | push main / 手动 | 渲染并发布 `_book/` 到 gh-pages |

提交作者与 committer 只用 `chengzhao-dev`；提交信息不添加 `Co-authored-by` 等额外作者 trailer（见 `shipping-github`）。
