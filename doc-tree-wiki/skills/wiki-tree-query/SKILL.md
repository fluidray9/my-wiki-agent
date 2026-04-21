---
name: wiki-tree-query
description: "查询树状索引，定位到 raw 原始文档的精确段落。场景：需要从原始文档检索、精确查找特定段落时"
---

# Wiki Tree Query

查询知识库的树状索引，精确检索原始文档的段落内容。

## KB 参数规则

- `--kb KB_NAME`：指定单个知识库
- `--kb KB1 --kb KB2`：指定多个知识库
- **不指定 `--kb`**：搜索所有知识库

## 工作流程

1. **Agent 分析查询** — 理解用户问题的语义（如 "deepseek-v3什么时候出来的" → 需要找发布时间）
2. **脚本** `find_matching_leaves()` 根据语义意图匹配候选段落
3. **Agent** 读取 raw 原文片段，综合答案返回给用户

## 语义检索支持

**Agent 语义转换**：
用户问题 "deepseek-v3什么时候出来的" → Agent 转换为 "发布" 或 "2024" 或 "时间"

**混合检索评分**：
- keywords 匹配：权重 3（最高）
- semantic 匹配：权重 2
- text 匹配：权重 1

**示例**：
| 用户问题 | Agent 转换 | 找到的结果 |
|---------|-----------|-----------|
| "deepseek-v3什么时候出来的" | → "发布" 或 "2024" | ✅ 找到发布时间 |
| "有哪些人参与了" | → "团队" 或 "成员" | ✅ 找到团队成员 |
| "用了什么技术" | → "技术" 或 "架构" | ✅ 找到技术信息 |

## 脚本函数

```python
# 查找匹配的叶子节点
find_matching_leaves(query="发布时间", kb_list=["deepseek-kb"])

# 语义搜索（LLM/Agent 驱动）
semantic_search(query="deepseek-v3什么时候出来的", kb_list=["deepseek-kb"])

# 读取原文片段
retrieve_text(file="knowledge-base/deepseek-kb/raw/doc1.md", char_start=150, char_end=500)
```

## 命令行用法

```bash
# 查询指定 KB
python scripts/query_tree_index.py "MoE" --kb deepseek-kb

# 查询多个 KB
python scripts/query_tree_index.py "团队成员" --kb deepseek-kb --kb other-kb

# 搜索所有 KB（不指定 --kb）
python scripts/query_tree_index.py "DeepSeek"

# 指定最大结果数
python scripts/query_tree_index.py "MoE" --kb deepseek-kb --max-results 5
```

## 输出

- 匹配的叶子节点列表（含 KB 名称、位置信息）
- LLM 从 raw 读取原文片段返回给用户
