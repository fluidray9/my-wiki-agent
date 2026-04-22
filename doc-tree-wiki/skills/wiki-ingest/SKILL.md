---
name: wiki-ingest
description: "摄入源文档到知识库 wiki，生成 source/entity/concept 页面并更新 index。场景：需要将 Markdown、PDF、arXiv 等文档转换为 wiki 页面时"
---

# Wiki Ingest

摄入源文档到知识库的 LLM Wiki。**Agent 手动执行所有步骤**，脚本只负责文件读写。

## KB 参数规则

- `--kb KB_NAME`：指定知识库名称
- **不指定 `--kb`**：从文件路径推断 KB 名（如 `raw/deepseek-kb/doc.md` → KB = `deepseek-kb`）

## 工作流程

1. **Agent 读取源文档** — 使用 Read 工具读取 `knowledge-base/{kb}/raw/*.md`
2. **Agent 读取 wiki 上下文** — 读取 `knowledge-base/{kb}/wiki/index.md` 和 `wiki/overview.md`
3. **Agent 生成页面内容** — 根据文档生成 source/entity/concept 页面的 markdown
4. **Agent 调用脚本函数写入** — 调用 `ctx.save_source_page()`, `ctx.save_entity_page()`, `ctx.save_concept_page()`
5. **Agent 更新索引** — 更新 `knowledge-base/{kb}/wiki/index.md`, `wiki/overview.md`, `wiki/log.md`

## 脚本函数（Claude 调用）

```python
# 写入源页面
ctx.save_source_page(slug="my-source", content="...")

# 写入实体页面 (path 如 "entities/EntityName.md")
ctx.save_entity_page(path="entities/PersonName.md", content="...")

# 写入概念页面 (path 如 "concepts/ConceptName.md")
ctx.save_concept_page(path="concepts/ConceptName.md", content="...")

# 验证 ingest 结果
ctx.validate_ingest(changed_pages=["sources/my-source.md", "entities/PersonName.md"])
```

## 命令行用法

```bash
# 指定 KB ingest
python scripts/ingest.py raw/my-article.md --kb deepseek-kb

# 从路径推断 KB
python scripts/ingest.py knowledge-base/deepseek-kb/raw/doc.md

# 批量 ingest
python scripts/ingest.py raw/deepseek-kb/*.md --kb deepseek-kb

# 验证现有 wiki（断链、未索引检查）
python scripts/ingest.py --validate-only --kb deepseek-kb
```

## Claude 职责（Agent-Delegation 架构）

- 读取源文档内容
- **检测图片引用**：markdown 中 `![](path/to/image.png)` 等引用
- **解析图片内容**：读取图片文件，用 LLM 理解图片内容（图像描述/OCR）
- 检测矛盾（如与现有 wiki 内容冲突）
- 生成页面 markdown（包含完整 frontmatter: title, type, tags, sources, last_updated）
- 在 wiki 页面中包含图片内容描述
- 在 tree-index 中标注图片来源
- 调用 `save_*_page()` 写入文件
- 更新 index.md 添加条目
- 追加到 log.md: `## [YYYY-MM-DD] ingest | <Title>`
- **调用 wiki-graph 构建/更新图谱**

## 图片处理流程

1. 读取 markdown 文件时，检测图片引用：
   ```markdown
   ![alt text](img/screenshot.png)
   ```
2. 解析图片路径（相对于 markdown 文件位置）
3. 读取图片文件内容
4. 用 LLM 解析图片内容（如：图像描述、OCR 文字等）
5. 在生成的 wiki 页面中包含图片内容描述
6. 在 tree-index 中，图片节点标记为 `keywords: ["图片", ...]`

## source_file frontmatter

- 指向 markdown 文件本身（如 `raw/raw2/raw2.md`）
- 图片是 markdown 引用的内容，不是独立源文档

## 输出摘要

完成后报告：
- 创建的页面列表
- 检测到的矛盾（如有）
- 验证结果（断链检查、index 覆盖）
- 图谱更新结果（节点数、边数）
