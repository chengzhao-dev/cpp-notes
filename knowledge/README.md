# knowledge/ 知识库

本目录是**领域知识的唯一出处**：回答「为什么这样配、为什么这样设计、失效的成因是什么」。
skill 侧 `.cursor/skills/*/references/` 只承载写作流程、格式约定和硬约束，需要依据时写一行检索入口，不复制本目录正文。

## 目录结构

```text
knowledge/
├── domains/                      # main 分支的稳定知识
│   ├── cpp_core/                 # 核心语言
│   │   └── 01_memory_pointers/
│   └── tooling/                  # 工具链与工程
│       ├── 01_build_toolchain/
│       ├── 02_quarto_rendering/
│       ├── 03_publishing/
│       ├── 04_repository_hygiene/
│       ├── 05_html_output/
│       └── 06_agent_runtime/
└── branches/                     # 非 main 分支的知识
    ├── cpp26-preview/
    └── legacy-cpp98/
```

子目录前缀数字只用于稳定排序，不参与检索打分。文件名与目录名一律纯 ASCII。

## 文件规范（强制）

frontmatter 字段：

| 字段 | 必填 | 作用 |
|---|---|---|
| `kb_id` | 是 | 全局唯一，格式 `<domain>-<subdomain>-<主题>-v<N>`；改名等于新建知识 |
| `title` | 是 | 文档级标题，也是 Parent 无 `###` 时的标题路径根 |
| `domain` | 是 | 检索预过滤维度，取值与 `domains/` 下一层目录名一致 |
| `subdomain` | 建议 | 与 `domains/<domain>/` 下的子目录名对应 |
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
4. 不复述 skill 侧的写作约定；需要指向别处时写「见标识 `<kb_id>` 的知识文件」。
5. 表格不超过 30 行，禁止段落中间的 HTML 锚点跳转。

## 检索不变量

1. 不产出无正文的标题壳 Child；不产出与 Parent 逐字节相同的 Child。
2. 每个 Child 都带 `[标题路径] ` 前缀，保证独立可判读。
3. 检索器交给 LLM 的是 Stage 5 回溯后的 Parent，评测口径必须与之一致。
4. 中文分词取二元组，ASCII 标识符整体保留并拆下划线，**语言关键字永不作为停用词**。
5. 冲突候选只在**同一分支**内按文档级概念集合（`tags` ∪ 反引号内的严格标识符）的 Jaccard 判定，并跳过已被 `supersedes` 关联的一对；跨分支的差异是分支分歧，不是冲突。

## 索引与验证

```powershell
python .cursor/tools/run.py kb-index            # 增量（按 content_hash 跳过未变文件）
python .cursor/tools/run.py kb-index --rebuild  # 改分词或结构后全量重建
python .cursor/tools/run.py kb-check            # 格式违规、重复、孤立、断链、P95 延迟
python .cursor/tools/run.py kb-eval             # Top-5 召回率、延迟与注入 Token 预算
python .cursor/tools/run.py kb-search "<查询>" --domain tooling --explain
```

产物写在 `index_data/`（已 gitignore，缺失时自动重建）。管道代码在 `scripts/`：
`kb_util.py` 公共工具、`chunker.py` 语义分块、`indexer.py` 双层索引与图谱、
`retriever.py` 五阶段检索、`evaluate.py` 与 `eval_set.py` 评测、`health_check.py` 体检、
`test_conflict_detection.py` 锁住「重合度 → 检索降权」链路（已接入 `run.py check`）。

## 新增知识的最小闭环

1. 建文件 → `kb-index` → `kb-check`（重复必须为 0）。
2. 在 `scripts/eval_set.py` 补该文件的查询条目，让召回率可验证而不是自我声明。
3. 精简对应的 skill reference，只留怎么做加一行 `kb-search` 入口。
4. 更新 `.cursor/skills/_CATALOG.md` 路由，最后跑 `run.py check`。
