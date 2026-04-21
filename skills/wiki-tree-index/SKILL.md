---
name: wiki-tree-index
description: "从 raw 原始文档生成树状索引，按章节+段落组织。场景：需要生成或重建树状索引时"
---

# Wiki Tree Index

生成树状索引，从原始文档 `raw/` 构建按章节+段落组织的索引。

## 工作流程

1. **脚本** `extract_document_structure()` 解析所有 `raw/*.md`
2. **脚本** 返回结构化数据（标题层级、段落位置）
3. **Agent** 使用索引进行**语义检索**（如 "deepseek-v3什么时候出来的" → 找到发布时间相关内容）
4. **脚本** 写入 `tree-index/tree-index.md`

## 树状索引格式

每个叶子节点包含丰富的检索信息：

```yaml
---
title: "Tree Index"
type: tree-index
sources: [raw/doc1.md, raw/doc2.md]
generated: 2026-04-21
---

## 第一章
### 1.1 章节名
- {file: "raw/doc1.md", line: 10, char_start: 150, char_end: 500,
   keywords: ["DeepSeek", "V3", "发布", "2024"],   # 关键词（用于精确匹配）
   semantic: "介绍 DeepSeek-V3 发布时间...",          # 语义摘要（用于语义检索）
   text: "原始段落内容..."}
```

**字段说明**：
| 字段 | 说明 | 用途 |
|------|------|------|
| file | 文件路径 | 定位原始文档 |
| line | 行号 | 定位原始文档 |
| char_start/end | 字符位置 | 精确定位段落 |
| keywords | 关键词列表 | 关键字检索（权重3） |
| semantic | 语义摘要 | 语义检索（权重2） |
| text | 原始文本 | 显示/引用（权重1） |

## 脚本函数

```python
# 解析文档结构（供 Agent 生成树状索引）
extract_document_structure(file_path)  # 返回 [(level, title, char_start, char_end, paragraphs), ...]

# 生成树状索引内容
generate_tree_index_content(docs_structure)  # 返回 markdown 字符串
```

## 命令行用法

```bash
python scripts/build_tree_index.py              # 生成树状索引
python scripts/build_tree_index.py --dry-run     # 只显示解析结果，不生成索引
```

## 语义检索支持

树状索引支持 Agent 进行语义检索：
- **关键字检索**：`query_tree_index.py "MoE"` → 精确匹配
- **语义检索**：Agent 理解用户意图（如 "deepseek-v3什么时候出来的" → 找"发布时间"）→ 从 tree-index 找到候选段落 → retrieve_text() 读取原文 → 综合回答

## 输出

- `tree-index/tree-index.md` — 树状索引文件
