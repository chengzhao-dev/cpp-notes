# AGENTS.md

**C++ 笔记**是面向新手的 Linux C++ Quarto Book。

## 项目结构

| 路径 | 职责 |
| --- | --- |
| `content/` | Quarto 章节正文，按 part 分目录 |
| `code/` | 与章节对应的 C++ 示例和工程，`build/` 是产物 |
| `.cursor/skills/quarto-theme/assets/theme/` | 页面主题、样式和字体资源 |
| `.cursor/` | skills、统一工具和项目 MCP 服务 |
| `knowledge/` | 精简领域知识库（回答「为什么」）；`temp/knowledge-index/` 是其索引产物，不入库 |

章节目录对齐：`content/<part>/`、`code/<part>/`、任务单 `.cursor/skills/cpp-content/references/tasks/<part>/`。

## 常用命令

| 命令 | 用途 |
| --- | --- |
| `python .cursor/skills/agent-ops/scripts/run.py scope <目标>` | 输出最小读取作用域 |
| `python .cursor/skills/agent-ops/scripts/run.py check` | 批量运行编码、文档、主题和产物检查 |
| `python .cursor/skills/agent-ops/scripts/run.py render` | 渲染 Book 并自动检查 |
| `python .cursor/skills/agent-ops/scripts/run.py verify --changed` | 增量校验 C++ 示例 |
| `python .cursor/skills/agent-ops/scripts/run.py build <part>/<chapter>` | 在 WSL 构建单章示例 |
| `python .cursor/skills/agent-ops/scripts/run.py status` | 输出精简 Git 状态 |
| `python .cursor/skills/agent-ops/scripts/run.py kb-index [--rebuild]` | 增量或全量重建知识库索引 |
| `python .cursor/skills/agent-ops/scripts/run.py kb-search "<查询>" [参数]` | 按预算检索知识库，参数透传 retriever（`--toc` `--parent` `--explain` `--domain`） |
| `python .cursor/skills/agent-ops/scripts/run.py kb-check` | 知识库结构体检与检索延迟 |
| `python .cursor/skills/agent-ops/scripts/run.py kb-eval` | 标注集召回率与注入 Token 验收 |
| `python .cursor/skills/agent-ops/scripts/run.py kb-scale [--sizes 1000,10000]` | 三层索引规模基准，输出全库 P95 拐点与域内分片对照 |

## 工作约束

1. 每次任务先运行 `run.py scope`，只读 UNIT、READ 和必要 reference；不要整包读取 references。
2. 永不读取或索引 `_book/**`、`code/**/build/**`、`.quarto/**`、`.cache/**`、`.tmp/**`；产物检查交给脚本。
3. 只有检查失败或出现新症状才进入诊断逃生舱；查明后把稳定经验沉淀为一次断言。
4. 预计读取超过 8 个文件或需要全仓检索时才派侦察代理；编辑必须回主线程完成。
5. 默认输出 terse 结论，失败才使用 `--verbose`；不回显密钥、凭据、`.env` 或无关个人信息。
6. 中文文件使用 UTF-8 无 BOM、LF；修改 `.qmd`、skill 或主题 CSS 后先运行编码检查。
7. 修改 `.cursor/skills/quarto-theme/assets/theme/**` 或 `_quarto.yml` 会触发整本渲染；先确认代价，再运行 `run.py render`。
8. 稳定前缀按字符计预算：`AGENTS.md` 仅按 `project_doc_max_bytes = 65536` 做字节护栏，`.cursor/skills/` 的 L1/L2 由 `check_skill_size.py` 按字符为主、字节为次级护栏强制。
9. goal 模式长任务：上下文压缩由宿主完成；每轮只推进一个可验证子目标并把进度落盘到 `git status` 可见的文件，不依赖对话记忆交接；压缩后或收到上下文告警时先重读 `run.py scope` 与 `git status` 确认边界；每轮结束前用一次 `run.py check` 收口。
10. 工具调用遵循固定路径优先、PATH 回退、缺失即止：Python 使用 `CPP_MEMO_PYTHON` 与 `.cursor/skills/python-tools/assets/config/runtime.json`，其他工具使用对应的 `CPP_MEMO_<TOOL>`；所有候选均不可用时立即中止当前命令，不伪造结果。

## 初始化兼容

Codex 初始化或其他工具重新生成规则时，必须合并本文件，不得覆盖项目结构、命令、安全约束和读取边界；`AGENTS.md` 是唯一项目级总入口，宿主专用文件只能引用它。
