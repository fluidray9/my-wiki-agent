---
name: wiki-ingest
description: "摄入源文档到 wiki，生成 source/entity/concept 页面并更新 index。场景：需要将 Markdown、PDF、arXiv 等文档转换为 wiki 页面时"
---

# Wiki Ingest

摄入源文档 skill，调用 `scripts/ingest.py`。

## 调用

```bash
python scripts/ingest.py raw/papers/my-paper.md
python scripts/ingest.py --validate-only
```

## 工作流程

1. **Claude** 读取源文档内容
2. **Claude** 根据文档生成 source/entity/concept 页面的 markdown 内容
3. **脚本** 接收 Claude 调用 `save_source_page()`, `save_entity_page()`, `save_concept_page()` 写入文件
4. **脚本** 更新 `wiki/index.md` 和 `wiki/log.md`

## 脚本职责

- 文件读写（`save_source_page()`, `save_entity_page()`, `save_concept_page()`）
- `update_index()` — 更新 index.md
- `append_log()` — 追加到 log.md
- `validate_ingest()` — 验证断链和 index 覆盖

## Claude 职责

- 读取源文档内容
- 生成页面 markdown 内容（包含完整 frontmatter）
- 调用 `save_source_page(slug, content)` 写入 source 页面
- 调用 `save_entity_page(path, content)` 写入 entity 页面
- 调用 `save_concept_page(path, content)` 写入 concept 页面

## 输出

- 创建的页面列表
- 验证结果（断链检查、index 覆盖）
