# LLM Wiki — 共享规范

所有 skill 必须遵循这些规范。

## 目录结构

```
raw/          # 源文档（不可修改）
wiki/         # Agent 维护的 wiki 层
  index.md    # 所有页面目录
  log.md      # 操作记录（append-only）
  overview.md # 跨源的综合概述
  sources/    # 每个源文档一个总结页
  entities/   # 人物/公司/项目页面
  concepts/   # 概念/框架/理论页面
  syntheses/  # 查询答案存档
graph/        # 自动生成的知识图谱
tools/        # Python 工具脚本
```

## 页面格式

每个 wiki 页面使用 YAML frontmatter：

```yaml
---
title: "页面标题"
type: source | entity | concept | synthesis
tags: []
sources: []       # 源 slug 列表
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
2–4 句摘要。

## Key Claims
- 主张 1
- 主张 2

## Key Quotes
> "引用内容" — 上下文

## Connections
- [[EntityName]] — 关系
- [[ConceptName]] — 连接

## Contradictions
- 与 [[OtherPage]] 矛盾：...
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
- [Source Title](sources/slug.md) — 一句话描述

## Entities
- [Entity Name](entities/EntityName.md) — 一句话描述

## Concepts
- [Concept Name](concepts/ConceptName.md) — 一句话描述

## Syntheses
- [Analysis Title](syntheses/slug.md) — 回答的问题
```

## Log 格式

每个操作记录：
```
## [YYYY-MM-DD] <operation> | <title>
```

操作类型：ingest, query, health, lint, graph, edit

## 验证清单

创建/修改页面后检查：
- [ ] frontmatter 完整（title, type, last_updated）
- [ ] 所有 [[wikilinks]] 指向已存在的页面
- [ ] 新页面已添加到 index.md
- [ ] 操作已记录到 log.md