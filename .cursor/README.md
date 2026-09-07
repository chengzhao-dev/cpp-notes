# cpp-notes Agent 配置

格式参考：[OpenAI Codex Skills](https://developers.openai.com/codex/skills/)；协议参考：[MCP Specification](https://modelcontextprotocol.io/specification/latest)。这些来源定义格式与协议，不保证宿主自动发现本目录。

`.cursor/` 是本仓库面向 Agent 的配置目录，包含可按需读取的 skills 和一个项目级 MCP 服务。

六项原则的完整文本位于根目录 `CODEX-PERSONAL-INSTRUCTIONS.md`，供粘贴进 Codex 个性化设置使用。它是宿主设置内容，不属于 skills 的阅读项：任务路由、`_CATALOG.md` 和任务单必读清单都不登记它。

Codex 项目指令链按 `project_doc_max_bytes` 截断；本项目采用 `65536` 字节护栏。OpenAI 未定义固定的 `AGENTS.md` 行数或 token 上限。

Codex 对每个 skill 的初始列表预算为上下文窗口的 2%，未知时按 8000 字符封顶；`.cursor/tools/check_skill_size.py` 据此按字符核算 name 与 description 的总量。

## 当前兼容性结论

不同宿主不会自动扫描同一个目录名。当前 Codex 会话不会把项目内的 `.cursor/skills/` 自动注册为内置 skill，但可以显式读取其中的 `SKILL.md` 并按规则执行。因此：

1. 进入任务后，先读取 `.cursor/skills/<skill>/SKILL.md`。
2. 按 `SKILL.md` 中的路由，只读取需要的 `references/`。
3. 不把 `.cursor/skills/` 当作宿主已经自动加载的系统指令。

Codex 初始化或其他宿主重新生成规则时，必须合并根目录 `AGENTS.md`，不得覆盖项目结构、读取边界、常用命令和安全约束；宿主专用文件只作薄适配层。

`.cursor/skills/` 使用通用的 `SKILL.md` front matter：每个 skill 是一个目录，包含一个 `SKILL.md`，可选包含 `references/`、`scripts/` 和 `templates/`。它是仓库内的唯一 skills 副本。

`manifest.json` 是本项目的说明元数据，不是 Codex、Cursor 或其他宿主自动读取的配置格式。要让某个宿主使用 skills 或 MCP，仍需在该宿主自己的项目或用户配置中显式登记。

## MCP

MCP 实现位于 `.cursor/mcp/`，使用 Python 标准库和 stdio JSON-RPC，不需要额外依赖。它提供受路径白名单保护的项目资源、文件读取/编辑、检索、校验、渲染、构建和 Git 只读工具。

```powershell
python .cursor/mcp/server.py
```

MCP 客户端应把上面的命令作为 stdio server 启动命令；具体初始化消息、工具列表和宿主配置示例见 `.cursor/mcp/README.md`。
