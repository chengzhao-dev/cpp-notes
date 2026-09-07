# AGENTS.md

**C++ 笔记**是面向新手的 Linux C++ Quarto Book。

## 六原则摘要

编码前思考；简洁优先；精准修改；目标驱动执行；默认使用简体中文；安全优先且绝不泄露密钥、凭据或敏感信息。

完整表述见根目录 `CODEX-PERSONAL-INSTRUCTIONS.md`，该文件用于粘贴进 Codex 个性化设置的「Codex 说明」，在那里它就是最高优先级。项目仓库只保留下面的结构、命令与读取边界。

## 项目结构

| 路径 | 职责 |
| --- | --- |
| `content/` | Quarto 章节正文，按 part 分目录 |
| `code/` | 与章节对应的 C++ 示例和工程，`build/` 是产物 |
| `theme/` | 页面主题、样式和字体资源 |
| `handbook/` | 项目结构、任务、运维和 Agent 规范 |
| `.cursor/` | skills、统一工具和项目 MCP 服务 |

章节目录对齐：`content/<part>/`、`code/<part>/`、`handbook/tasks/content/<part>/`。

## 常用命令

| 命令 | 用途 |
| --- | --- |
| `python .cursor/tools/run.py scope <目标>` | 输出最小读取作用域 |
| `python .cursor/tools/run.py check` | 批量运行编码、文档、主题和产物检查 |
| `python .cursor/tools/run.py render` | 渲染 Book 并自动检查 |
| `python .cursor/tools/run.py verify --changed` | 增量校验 C++ 示例 |
| `python .cursor/tools/run.py build <part>/<chapter>` | 在 WSL 构建单章示例 |
| `python .cursor/tools/run.py status` | 输出精简 Git 状态 |

## 工作约束

1. 每次任务先运行 `run.py scope`，只读 UNIT、READ 和必要 reference；不要整包读取 references。
2. 永不读取或索引 `_book/**`、`code/**/build/**`、`.quarto/**`、`.cache/**`、`.tmp/**`；产物检查交给脚本。
3. 只有检查失败或出现新症状才进入诊断逃生舱；查明后把稳定经验沉淀为一次断言。
4. 预计读取超过 8 个文件或需要全仓检索时才派侦察代理；编辑必须回主线程完成。
5. 默认输出 terse 结论，失败才使用 `--verbose`；不回显密钥、凭据、`.env` 或无关个人信息。
6. 中文文件使用 UTF-8 无 BOM、LF；修改 `.qmd`、skill 或主题 CSS 后先运行编码检查。
7. 修改 `theme/**` 或 `_quarto.yml` 会触发整本渲染；先确认代价，再运行 `run.py render`。
8. 稳定前缀按字符计预算：`AGENTS.md` 仅按 `project_doc_max_bytes = 65536` 做字节护栏，`.cursor/skills/` 的 L1/L2 由 `check_skill_size.py` 按字符为主、字节为次级护栏强制。
9. 根目录 `CODEX-PERSONAL-INSTRUCTIONS.md` 只服务宿主个性化设置：禁止把它写入任务单必读、scope 的 READ、`_CATALOG.md` 路由或任何 skill 的阅读项。
10. goal 模式长任务：上下文明显吃紧（约 70%–80%）时先压缩再继续，压缩后重读 `run.py scope` 输出确认边界；plan 与 build 模式不做此约束。细则见 `handbook/operations/agent-operations.md`。
11. 工具调用遵循固定路径优先、PATH 回退、缺失即止：Python 使用 `CPP_MEMO_PYTHON` 与 `.config/python/runtime.json`，其他工具使用对应的 `CPP_MEMO_<TOOL>`；所有候选均不可用时立即中止当前命令，不伪造结果。

## 初始化兼容

Codex 初始化或其他工具重新生成规则时，必须合并本文件，不得覆盖项目结构、命令、安全约束和读取边界；`AGENTS.md` 是唯一项目级总入口，宿主专用文件只能引用它。
