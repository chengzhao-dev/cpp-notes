# cpp-notes

[![quarto build & deploy](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml/badge.svg)](https://github.com/chengzhao-dev/cpp-notes/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](LICENSE)

基于 [Quarto Book](https://quarto.org/docs/books/) 的 C++ 编程备忘文档：**在线阅读 <https://chengzhao-dev.github.io/cpp-notes/>**。

## 环境

- 默认环境：**Windows 上的 WSL2** 开发环境，详见 `content/environment/`。
- 示例源码统一放在 `code/` 目录。

## 本地渲染

```bash
quarto render      # 渲染整本 Book，输出到 _book/
quarto preview     # 本地实时预览
git push           # 推送即自动部署（Actions 渲染 → Pages 发布）
```

> 改 `theme/scss/`（主题 `*.scss`）、`theme/css/`（组件 `*.css`）或 `theme/includes/fonts.html`（全局）会整本重渲染，较慢；`quarto preview` 在 Windows 上偶发卡死，清理方式见 `AGENTS.md`。

## 结构

```
├── _quarto.yml               # Book 配置
├── index.qmd                 # 首页入口
├── content/                  # 备忘录章节（.qmd）
├── code/                     # C++ 示例源码（code/<主题>/<小写下划线>.cpp）
├── theme/                    # 主题：scss/（明暗主题变量）、css/（按域拆分组件规则）、includes/（fonts/footer）
├── scripts/                  # 仓库级构建/CI 脚本（defer-mermaid.py、python.json 本机解释器）
└── .opencode/                # opencode 配置与 skills（agent 工具在各 skill 的 scripts/，均为 Python）
```

## 发布

- 推送到 `main` 后由 `.github/workflows/pages.yml` 自动 `quarto render`，产物经官方 `upload-pages-artifact` + `deploy-pages` actions 发布到 GitHub Pages（Pages 来源须为 **GitHub Actions**，见仓库 Settings → Pages）。
- Pull Request 由 `.github/workflows/render-check.yml` 做渲染检查，防断渲染进主干。

## 内容规划

按 part 逐步扩写：`environment` 环境与工具链 → `core` 语言核心 → `memory` 对象与内存（RAII/智能指针/移动语义）→ `stl` 容器与算法 → `templates` 模板 → `concurrency` 并发 → `toolchain` CMake 与工程实践 → 速查表。
