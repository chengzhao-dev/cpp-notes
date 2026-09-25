# .agents/knowledge/ 知识库

本目录是领域依据的唯一出处：回答「为什么这样配置、为什么这样设计、为什么会失败」。目录名与对应 Skill 一致。
「skill 与 knowledge 怎么分工」的权威定义在 `.agents/skills/catalog.md`「skill 与 knowledge 的分工」，本文件只引用不复制。

## 目录结构

```text
.agents/knowledge/
├── cpp-content/                  # 按 language、memory、toolchain 等性质归档
├── quarto-docs/                  # 按 writing、rendering、output 等性质归档
├── quarto-theme/                 # 主题令牌、布局几何与响应式行为
├── github-ops/                   # Git、CI、Pages 与发布
└── agent-ops/                    # Agent 运行、重构与维护
```

按性质创建子目录，不创建空目录。文件名与目录名一律纯 ASCII。

## 文件规范（强制）

frontmatter 字段：

| 字段 | 必填 | 作用 |
|---|---|---|
| `kb_id` | 是 | 全局唯一。现行约定 `cpp-<area>-<topic>-v<N>`（如 `cpp-quarto-chapter-pattern-v1`），历史 id 保持不改名，改名等于新建知识 |
| `title` | 是 | 文档级标题，也是 Parent 无 `###` 时的标题路径根 |
| `domain` | 是 | 检索预过滤维度，取值与 Skill 目录名一致 |
| `subdomain` | 建议 | 同一 Skill 内的主题筛选 |
| `tags` | 建议 | 行内列表，参与概念图谱连线，也是冲突检测的概念来源之一 |
| `level_range` | 建议 | 面向读者的难度区间 |
| `dependencies` | 建议 | 前置知识的 `kb_id` 列表，图谱按它建边 |
| `supersedes` | 版本替换时必填 | 被替代的 `kb_id`，命中后旧版分数乘 0.35 |
| `created` / `updated` | 是 / 是 | 日期字符串，`updated` 差异是冲突判定依据 |
| `chunk_strategy` | 是 | 目前只有 `semantic_heading` |
| `estimated_tokens` | 建议 | 人工估计值，实际预算以索引测得为准 |

正文结构：

1. 全文只有一个 `# H1`，与 `title` 一致。
2. `##` 是 **Parent Chunk** 边界（返回给 LLM 的大块），`###` 是 **Child Chunk** 边界（精准匹配的小块）。
3. 每个 `###` 下必须有正文：只有标题没有内容的壳块会被分块器丢弃。
4. 不复述 skill 侧的写作约定。需要指向别处时写「见标识 `<kb_id>` 的知识文件」。
5. 表格不超过 30 行，禁止段落中间的 HTML 锚点跳转。

## 检索不变量

1. 不产出无正文的标题壳 Child。不产出与 Parent 逐字节相同的 Child。
2. 每个 Child 都带 `[标题路径] ` 前缀，保证独立可判读。
3. 检索器交给 LLM 的是 Stage 5 回溯后的 Parent，评测口径必须与之一致。
4. 中文分词取二元组，ASCII 标识符整体保留并拆下划线，**语言关键字永不作为停用词**。
5. 冲突候选按全库文档级概念集合（`tags` ∪ 反引号内的严格标识符）的 Jaccard 判定，并跳过已被 `supersedes` 关联的一对。

## Token 预算与增长

知识文件不设整文件大小上限，避免把内聚主题机械拆散。实际约束放在检索单元：默认单次检索最多使用 4000 Token，上下文硬上限为 6000 Token，任一 live Parent Chunk 不得超过 4000 Token。

新增或扩容前先更新已有知识。同一主题需要更多细节时，按 `##` 的独立概念边界扩容；一个父块超过 4000 Token 时，先压缩重复表述，再按可独立检索的概念拆分。每次新增 `kb_id` 都要在 `eval_set.py` 补查询，让召回率与注入预算接受自动评测。

## 索引与验证

```powershell
& .agents/skills/agent-ops/scripts/run.ps1 kb-index            # 增量（按 content_hash 跳过未变文件）
& .agents/skills/agent-ops/scripts/run.ps1 kb-index --rebuild  # 改分词或结构后全量重建
& .agents/skills/agent-ops/scripts/run.ps1 kb-check            # 格式违规、重复、孤立、断链、P95 延迟
& .agents/skills/agent-ops/scripts/run.ps1 kb-eval             # Top-5 召回率与注入 Token 预算
& .agents/skills/agent-ops/scripts/run.ps1 kb-search "<查询>" --domain quarto-docs --explain
```

产物写在 `temp/knowledge-index/`（已 gitignore，缺失时自动重建）。管道代码在 `.agents/skills/python-tools/scripts/`：
`kb_common.py` 公共工具、`chunker.py` 语义分块、`indexer.py` FTS5 与图谱索引、
`retriever.py` 检索与 Parent 回溯、`evaluator.py` 与 `eval_set.py` 评测、`check_health.py` 体检、
`test_conflict_detection.py` 锁住「重合度 → 检索降权」链路（已接入 `check --profile knowledge`）。

## 新增知识的最小闭环

1. 建文件或更新唯一权威 → `kb-index` → `kb-check`（重复与 Parent 超限必须为 0）。
2. 在 `.agents/skills/python-tools/scripts/eval_set.py` 补该文件的查询条目，让召回率可验证而不是自我声明。
3. 精简对应的 skill reference，只留怎么做和一行 `kb-search` 入口；详细取舍依据留在 knowledge。
4. 更新 `.agents/skills/catalog.md` 短路由，最后按改动域运行 `run.py check --profile ...`。
