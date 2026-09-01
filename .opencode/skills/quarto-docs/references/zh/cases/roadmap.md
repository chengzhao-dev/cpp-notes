# 路线图示例 / 案例（writing-style.md 配套）

本文件是 `writing-style.md`「路线图（引导句 + mermaid）的中心结构」的 before/after 案例库。规则见 `../writing-style.md`。

示例（WSL2 环境章「本章目标」后的路线图）：

```markdown
本章的路线是先装好 WSL2 与 Ubuntu，再在它里面装好并验证 C++ 构建工具链，下图就是这条路线。

```{mermaid}
flowchart TD
  A[装好并启用 WSL2] --> B[用 Ubuntu 作为开发环境]
  B --> C{软件源网速慢吗？}
  C -- 不慢，用官方源 --> D[安装并验证 C++ 构建工具链]
  C -- 慢，换国内镜像 --> D
```
```

要点：引导句统摄两步 → 图按「装环境 → 装工具」递进、节点对齐目标列表 → 分支对称（换源不展开），细节在 `### 软件源` 深挖。
