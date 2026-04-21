# LLM Wiki — 共享规范

所有 skill 必须遵循这些规范。

## 目录结构

每个知识库（KB）有独立的目录结构：

```
doc-tree-wiki/
├── knowledge-base/               # 所有知识库
│   ├── deepseek-kb/            # 知识库 A
│   │   ├── kb-meta.json          # KB 元数据
│   │   ├── raw/                  # 源文档（不可修改）
│   │   ├── wiki/                 # Agent 维护的 wiki 层
│   │   │   ├── index.md          # 所有页面目录
│   │   │   ├── log.md            # 操作记录（append-only）
│   │   │   ├── overview.md       # 跨源的综合概述
│   │   │   ├── sources/          # 每个源文档一个总结页
│   │   │   ├── entities/         # 人物/公司/项目页面
│   │   │   ├── concepts/         # 概念/框架/理论页面
│   │   │   └── syntheses/        # 查询答案存档
│   │   ├── tree-index/           # 树状索引
│   │   └── graph/                # 自动生成的知识图谱
│   └── other-kb/               # 知识库 B
│       └── ...
└── skills/                     # 技能（保持不变）
```

> 旧结构（直接使用 `raw/`、`wiki/`）已废弃，请使用知识库结构。

## 页面格式

每个 wiki 页面使用 YAML frontmatter：

```yaml
---
title: "Page Title"
type: source | entity | concept | synthesis
tags: []
sources: []       # list of source slugs that inform this page
last_updated: YYYY-MM-DD
---
```

## 页面类型

| 类型 | 描述 | 存放位置 |
|------|------|---------|
| source | 源文档摘要页 | wiki/sources/ |
| entity | 人物/公司/项目 | wiki/entities/ |
| concept | 概念/框架/理论 | wiki/concepts/ |
| synthesis | 查询答案存档 | wiki/syntheses/ |

## 命名约定

| 类型 | 命名规则 | 示例 |
|------|---------|------|
| source | kebab-case | `attention-is-all-you-need.md` |
| entity | TitleCase | `OpenAI.md`, `SamAltman.md` |
| concept | TitleCase | `ReinforcementLearning.md` |
| synthesis | kebab-case | `transformer-analysis.md` |

## Wikilink 语法

使用 `[[PageName]]` 链接到其他 wiki 页面：

```markdown
- [[EntityName]] — 关系说明
- [[ConceptName]] — 连接说明
```

注意：
- 大小写敏感，必须与目标页面标题匹配
- 链接不存在的页面会被标记为断链

## Source Page 模板

```markdown
---
title: "Source Title"
type: source
tags: []
date: YYYY-MM-DD
source_file: raw/...
---

## Summary
2–4 sentence summary.

## Key Claims
- Claim 1
- Claim 2

## Key Quotes
> "Quote here" — context

## Connections
- [[EntityName]] — how they relate
- [[ConceptName]] — how it connects

## Contradictions
- Contradicts [[OtherPage]] on: ...
```

### Domain-Specific Templates

If the source falls into a specific domain (e.g., personal diary, meeting notes), use a specialized template:

#### Diary / Journal Template
```markdown
---
title: "YYYY-MM-DD Diary"
type: source
tags: [diary]
date: YYYY-MM-DD
---
## Event Summary
...
## Key Decisions
...
## Energy & Mood
...
## Connections
...
## Shifts & Contradictions
...
```

#### Meeting Notes Template
```markdown
---
title: "Meeting Title"
type: source
tags: [meeting]
date: YYYY-MM-DD
---
## Goal
...
## Key Discussions
...
## Decisions Made
...
## Action Items
...
```

## Entity Page 模板

```markdown
---
title: "EntityName"
type: entity
tags: []
sources: []
last_updated: YYYY-MM-DD
---

## Definition
实体的定义和概述。

## Key Attributes
- 属性 1
- 属性 2

## Connections
- [[SourcePage]] — 来源说明
```

## Concept Page 模板

```markdown
---
title: "ConceptName"
type: concept
tags: []
sources: []
last_updated: YYYY-MM-DD
---

## Definition
概念的定义和核心思想。

## Key Points
- 要点 1
- 要点 2

## Related Concepts
- [[RelatedConcept1]]
- [[RelatedConcept2]]

## Sources
- [[SourcePage]] — 来源说明
```

## Index 格式

```markdown
# Wiki Index

## Overview
- [Overview](overview.md) — living synthesis

## Sources
- [Source Title](sources/slug.md) — one-line summary

## Entities
- [Entity Name](entities/EntityName.md) — one-line description

## Concepts
- [Concept Name](concepts/ConceptName.md) — one-line description

## Syntheses
- [Analysis Title](syntheses/slug.md) — what question it answers
```

## Log 格式

每个操作记录：
```
## [YYYY-MM-DD] <operation> | <title>
```

操作类型：ingest, query, health, lint, graph, edit

---

## Ingest 工作流

触发条件：用户说 "ingest <file>" 或 `/wiki-ingest`

步骤（按顺序）：
1. Read the source document fully using the Read tool
2. Read `wiki/index.md` and `wiki/overview.md` for current wiki context
3. Write `wiki/sources/<slug>.md` — use the source page format
4. Update `wiki/index.md` — add entry under Sources section
5. Update `wiki/overview.md` — revise synthesis if warranted
6. Update/create entity pages for key people, companies, projects mentioned
7. Update/create concept pages for key ideas and frameworks discussed
8. Flag any contradictions with existing wiki content
9. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | <Title>`
10. **Post-ingest validation** — check for broken `[[wikilinks]]`, verify all new pages are in `index.md`, print a change summary

## Query 工作流

触发条件：用户说 "query: <question>" 或 `/wiki-query`

步骤：
1. Read `wiki/index.md` to identify relevant pages
2. Read those pages with the Read tool
3. Synthesize an answer with inline citations as `[[PageName]]` wikilinks
4. Ask the user if they want the answer filed as `wiki/syntheses/<slug>.md`

## Lint 工作流

触发条件：用户说 "lint the wiki" 或 `/wiki-lint`

Use Grep and Read tools to check for:
- **Orphan pages** — wiki pages with no inbound `[[links]]` from other pages
- **Broken links** — `[[WikiLinks]]` pointing to pages that don't exist
- **Contradictions** — claims that conflict across pages
- **Stale summaries** — pages not updated after newer sources
- **Missing entity pages** — entities mentioned in 3+ pages but lacking their own page
- **Data gaps** — questions the wiki can't answer; suggest new sources

Output a lint report and ask if the user wants it saved to `wiki/lint-report.md`.

## Health 工作流

触发条件：用户说 "health" 或 `/wiki-health`

Run: `python tools/health.py` (or `python tools/health.py --json` for machine-readable output)

Fast structural integrity checks — **zero LLM calls**, safe to run every session:
- **Empty / stub files** — pages with no content beyond frontmatter
- **Index sync** — `wiki/index.md` entries vs actual files on disk
- **Log coverage** — source pages missing a corresponding `ingest` entry in `wiki/log.md`

Output a health report. Use `--save` to write to `wiki/health-report.md`.

### Health vs Lint Boundary

| Dimension | `health` | `lint` |
|---|---|---|
| **Scope** | Structural integrity | Content quality |
| **LLM calls** | Zero | Yes (semantic analysis) |
| **Cost** | Free | Tokens |
| **Frequency** | Every session, before other work | Every 10-15 ingests |
| **Checks** | Empty files, index sync, log sync | Orphans, broken links, contradictions, gaps |
| **Tool** | `tools/health.py` | `tools/lint.py` |
| **Run order** | First (pre-flight) | After health passes |

> Run `health` first — linting an empty file wastes tokens.

## Graph 工作流

触发条件：用户说 "build the knowledge graph" 或 `/wiki-graph`

When the user asks to build the graph, run `tools/build_graph.py` which:
- Pass 1: Parses all `[[wikilinks]]` → deterministic `EXTRACTED` edges
- Pass 2: Infers implicit relationships → `INFERRED` edges with confidence scores
- Runs Louvain community detection
- Outputs `graph/graph.json` + `graph/graph.html`

If the user doesn't have Python/dependencies set up, instead generate the graph data manually:
1. Use Grep to find all `[[wikilinks]]` across wiki pages
2. Build a node/edge list
3. Write `graph/graph.json` directly
4. Write `graph/graph.html` using the vis.js template

## 验证清单

创建/修改页面后检查：
- [ ] frontmatter 完整（title, type, last_updated）
- [ ] 所有 [[wikilinks]] 指向已存在的页面
- [ ] 新页面已添加到 index.md
- [ ] 操作已记录到 log.md
