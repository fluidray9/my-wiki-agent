---
name: wiki-ingest
description: "摄入源文档到 wiki，生成 source/entity/concept 页面并更新 index。场景：需要将 Markdown、PDF、arXiv 等文档转换为 wiki 页面时"
---

# Wiki Ingest

摄入源文档到 LLM Wiki。**Agent 手动执行所有步骤**，脚本只负责文件读写。

## 工作流程

1. **Agent 读取源文档** — 使用 Read 工具读取 `raw/*.md`
2. **Agent 读取 wiki 上下文** — 读取 `wiki/index.md` 和 `wiki/overview.md`
3. **Agent 生成页面内容** — 根据文档生成 source/entity/concept 页面的 markdown
4. **Agent 调用脚本函数写入** — 调用 `save_source_page()`, `save_entity_page()`, `save_concept_page()`
5. **Agent 更新索引** — 更新 `wiki/index.md`, `wiki/overview.md`, `wiki/log.md`

## 脚本函数（Claude 调用）

```python
# 写入源页面
save_source_page(slug="my-source", content="...")

# 写入实体页面 (path 如 "entities/EntityName.md")
save_entity_page(path="entities/PersonName.md", content="...")

# 写入概念页面 (path 如 "concepts/ConceptName.md")
save_concept_page(path="concepts/ConceptName.md", content="...")

# 验证 ingest 结果
validate_ingest(changed_pages=["sources/my-source.md", "entities/PersonName.md"])
```

## 命令行用法

```bash
# 验证现有 wiki（断链、未索引检查）
python scripts/ingest.py --validate-only

# ingest 单个文件（会打印提示，但实际操作由 Agent 完成）
python scripts/ingest.py raw/my-article.md
```

## Claude 职责（Agent-Delegation 架构）

- 读取源文档内容
- 检测矛盾（如与现有 wiki 内容冲突）
- 生成页面 markdown（包含完整 frontmatter: title, type, tags, sources, last_updated）
- 调用 `save_*_page()` 写入文件
- 更新 index.md 添加条目
- 追加到 log.md: `## [YYYY-MM-DD] ingest | <Title>`

## 输出摘要

完成后报告：
- 创建的页面列表
- 检测到的矛盾（如有）
- 验证结果（断链检查、index 覆盖）
