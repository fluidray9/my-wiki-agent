---
name: wiki-tree-index
description: "从 raw 原始文档生成树状索引，按章节+段落组织。场景：需要生成或重建树状索引时"
---

# Wiki Tree Index

生成树状索引，从知识库的原始文档构建按章节+段落组织的索引。

## KB 参数规则

- `--kb KB_NAME`：指定知识库名称
- **不指定 `--kb`**：从 raw 路径推断 KB 名

## 工作流程

1. **脚本** `extract_document_structure()` 解析指定 KB 的 `knowledge-base/{kb}/raw/*.md`
2. **脚本** 返回结构化数据（标题层级、段落位置）
3. **Agent** 使用索引进行**语义检索**（如 "deepseek-v3什么时候出来的" → 找到发布时间相关内容）
4. **脚本** 写入 `knowledge-base/{kb}/tree-index/tree-index.md`

## 树状索引格式

每个叶子节点包含丰富的检索信息：

```yaml
---
title: "Tree Index"
type: tree-index
kb: "deepseek-kb"
sources: [knowledge-base/deepseek-kb/raw/doc1.md, knowledge-base/deepseek-kb/raw/doc2.md]
generated: 2026-04-21
---

## 第一章
### 1.1 章节名
- {file: "knowledge-base/deepseek-kb/raw/doc1.md", line: 10, char_start: 150, char_end: 500,
   keywords: ["DeepSeek", "V3", "发布", "2024"],
   semantic: "介绍 DeepSeek-V3 发布时间...",
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
extract_document_structure(file_path, kb_name)

# 生成树状索引内容
generate_tree_index_content(docs_structure, kb_name)
```

## 命令行用法

```bash
# 指定 KB 生成
python scripts/build_tree_index.py --kb deepseek-kb

# 从路径推断 KB
python scripts/build_tree_index.py knowledge-base/deepseek-kb/raw/doc.md

# 只显示解析结果
python scripts/build_tree_index.py --kb deepseek-kb --dry-run
```

## 语义检索支持

树状索引支持 Agent 进行语义检索：
- **关键字检索**：`query_tree_index.py "MoE" --kb deepseek-kb` → 精确匹配
- **语义检索**：Agent 理解用户意图（如 "deepseek-v3什么时候出来的" → 找"发布时间"）→ 从 tree-index 找到候选段落 → retrieve_text() 读取原文 → 综合回答

## 输出

- `knowledge-base/{kb}/tree-index/tree-index.md` — 树状索引文件
- `knowledge-base/{kb}/tree-index/final-tree-index.md` — LLM 按主题重组后的最终索引
