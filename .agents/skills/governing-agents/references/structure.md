# Agent 工作区结构规范

本规范适用于 `.agents/` 及其下的 `skills/`、`knowledge/`、`memory/`、`incidents/`，以及技能内部资源目录。配套命名规范见同技能下的 `naming.md`；两者冲突时，命名以 `naming.md` 为准，结构以本文件为准。

## 1. 四区职责

| 区 | 回答的问题 | 何时读 |
| --- | --- | --- |
| `skills/` | 怎么做（流程、清单、硬约束） | 命中任务时读对应 `SKILL.md` |
| `knowledge/` | 是什么 / 为什么（稳定事实、取舍） | 需要依据时，经 `kb-search` 或 `kb_id` |
| `memory/` | 过去哪里容易出错 | 每个任务开始时读 `MEMORY.md` 索引 |
| `incidents/` | 这次失败有没有先例 | **仅排查失败时**读 `INDEX.md`，平时视为不存在 |

一个知识点只允许一个出处：同一规则不要在多个区完整复制；引用用路径或 `kb_id` 指回唯一出处。

## 2. 目标结构

```text
.agents/
├── README.md                     # 一级入口，允许
├── skills/
│   ├── governing-agents/         # 三级：具体技能
│   │   ├── SKILL.md
│   │   ├── references/           # naming.md、structure.md、catalog.md
│   │   └── scripts/
│   └── <skill>/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── knowledge/
│   ├── KNOWLEDGE.md              # 领域路由
│   └── <domain>/<subdomain>/<topic>.md
├── memory/
│   ├── MEMORY.md
│   └── domains/<domain>/{index.md,<topic>.md}
├── incidents/
│   ├── INDEX.md
│   └── <domain>/<topic>.md
└── mcp/
    ├── README.md
    └── server.py
```

## 2.1 按性质封装

一个文件夹只封装一种「性质」（领域、职责、技能、生命周期、格式）。同目录出现两种以上性质时，继续拆子文件夹。

## 2.2 叶子目录规则（强制）

- **非叶子目录**（还有子文件夹的目录）只放：固定入口文件（`SKILL.md`、`KNOWLEDGE.md`、`MEMORY.md`、`INDEX.md`、`README.md`、`index.md`）、子文件夹、必要的轻量索引。
- **叶子目录**（其下没有子文件夹）直接放该性质的最终文件。
- 具体内容文件尽量放在从仓库根算起的三级或更深目录。

判定方法：目录里同时有 `x.md` 和子文件夹 `y/`，且 `x.md` 不是入口索引 → 把 `x.md` 移入性质相符的叶子（新建或已有的 `y/` 内）。

## 3. 技能内部

- `SKILL.md` 是唯一入口；详细规则放 `references/`，脚本放 `scripts/`，资源放 `assets/`。
- `references/` 内按性质建子目录（如 `cpp/`、`zh/`、`tasks/`）；子目录本身成为叶子时才直接放文件。
- 脚本数量增多时按职责分子目录；统一入口 `run.ps1`/`run.py` 保留在 `scripts/` 顶层。

## 4. memory 与 incidents

- `memory/`：三层索引，`MEMORY.md` 只做领域路由；每个领域一个 `index.md`（关键词 → 主题表）+ 若干原子主题文件。
- `incidents/`：单一 `INDEX.md`（症状关键词 → 案例指针）；案例文件放 `<domain>/`。不进任何常规路由、catalog 或检索索引。
- 复盘案例正文顺序：frontmatter → `# 标题` → 日期与关键词 → `## 症状` → `## 根因` → `## 修复方案` →（可选）`## 验证方法`。

## 5. 本仓特例

- 知识库索引产物只写根目录 `temp/knowledge-index/`，不入 `.agents/`。
- `.agents/skills/designing-theme/assets/theme/**` 是 Quarto 消费的主题资源，其内部组织以渲染链路为准，不受 2.2 约束。
- `mcp/server.py` 是宿主登记的固定入口路径，保持不动。
