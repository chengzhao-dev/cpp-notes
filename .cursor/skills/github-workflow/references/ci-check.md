# CI 持续集成与检查规范

官方依据：[GitHub Actions workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)、[GITHUB_TOKEN 权限](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication) 与 [Pages deployment](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 核心工作流清单

1. **render-check.yml**（Pull Request 门禁）：
   - 依赖环境：Ubuntu 最新版、Quarto 运行环境、Python 3.12。
   - 执行阶段：
     - quarto render：检查文档语法、YAML 配置与跨文件引用。
     - python3 handbook/scripts/build/defer-mermaid.py：验证渲染后处理脚本。
     - python3 .cursor/skills/cpp-content/scripts/verify_examples.py：硬性门禁，保证书中所有 C++ 代码均可通过编译。
2. **pages.yml**（Main 分支发布）：
   - 具备单并发控制（concurrency: pages），避免多任务并发覆盖。
   - 生成完整静态网站产物，推送到 gh-pages 分支。

## 调试与排错

- 当 CI 失败时，先在本地通过 .cursor/tools/run.py check 与 .cursor/tools/run.py verify 进行复现，禁止盲目推 commit 试错。
- 每个 workflow 显式声明最小 `permissions`；新增步骤只申请实际需要的权限，并为部署步骤单独说明写权限来源。
