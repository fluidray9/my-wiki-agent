---
name: wiki-tree-query
description: "查询树状索引，定位到 raw 原始文档的精确段落。场景：需要从原始文档检索、精确查找特定段落时"
---

# Wiki Tree Query

查询知识库的树状索引，精确检索原始文档的段落内容。**混合检索**：脚本字符串匹配 + LLM 语义检索 + LLM 综合。

## KB 参数规则

- `--kb KB_NAME`：指定单个知识库
- `--kb KB1 --kb KB2`：指定多个知识库
- **不指定 `--kb`**：搜索所有知识库

## 混合检索流程

```
用户查询 "DeepSeek-V3什么时候发布的"
    ↓
1. 脚本检索（结果1）
   - parse_tree_index() 解析 tree-index.md
   - find_matching_leaves() 字符串匹配评分
   - 返回 top N 结果
    ↓
2. LLM 语义检索（结果2）
   - LLM 阅读 tree-index.md 内容
   - 语义理解，找出相关段落
    ↓
3. LLM 综合
   - 综合结果1和结果2
   - 去重、排序、分析
   - 返回最终结果
    ↓
4. 脚本输出
   - 解析最终结果
   - retrieve_text() 读取原文
   - 格式化输出
```

## 脚本检索（结果1）

**字符串匹配评分**：
- keywords 匹配：权重 3（最高）
- semantic 匹配：权重 2
- text 匹配：权重 1

## LLM 语义检索（结果2）

**LLM 职责**：
1. 阅读 tree-index.md 内容
2. 语义理解用户问题
3. 找出最相关的段落
4. 返回标准化格式

**LLM 语义检索 Prompt**：
```
你是一个检索助手。用户问题: "{query}"

请阅读以下树状索引，找出最相关的段落（返回3个）。

树状索引内容:
{tree_index_content}

返回格式：
结果 1
📚 知识库: xxx
📄 参考文档: xxx
📍 位置: 第 x 行
📑 章节: xxx
```

## LLM 综合

**LLM 职责**：
1. 综合脚本检索结果（结果1）
2. 综合 LLM 语义检索结果（结果2）
3. 去重、排序
4. 返回最终结果

**LLM 综合 Prompt**：
```
你是一个检索助手。用户问题: "{query}"

【LLM语义检索结果】（权重高，优先保留）
{llm_results}

【脚本检索结果】（权重低，作为补充）
{script_results}

综合规则：
1. LLM语义检索结果优先，脚本检索作为补充
2. 去除重复段落（相似内容只保留最相关的）
3. 结果尽量多元（来自不同文档/章节）
4. 最终结果最多5个
5. 按相关性排序

最终结果（每个包含：知识库、文档、位置、内容、理由）:
```

## 脚本函数

```python
# 1. 脚本字符串匹配检索
find_matching_leaves(query, kb_list, max_results)

# 2. LLM 语义检索（Agent 调用）
llm_semantic_search(query, tree_index_content, kb_name)

# 3. LLM 综合（Agent 调用）
llm_synthesize(query, script_results, llm_results)

# 4. 读取原文片段
retrieve_text(file, char_start, char_end)
```

## 命令行用法

```bash
# 查询指定 KB
python scripts/query_tree_index.py "DeepSeek-V3什么时候发布的" --kb deepseek-kb

# 查询多个 KB
python scripts/query_tree_index.py "团队成员" --kb deepseek-kb --kb other-kb

# 语义检索权重 > 脚本检索权重
# 最终结果最多 5 个，尽量多元，相似结果去重

# 搜索所有 KB
python scripts/query_tree_index.py "MoE"

# 指定最大结果数
python scripts/query_tree_index.py "MoE" --kb deepseek-kb --max-results 5
```

## 输出格式

每个结果包含：
```
============================================================
结果 1
============================================================
📚 知识库: deepseek-kb
📄 参考文档: knowledge-base/deepseek-kb/raw/deepseek-v3.md
📍 位置: 第 3 行
📑 章节: DeepSeek-V3 技术解读
------------------------------------------------------------
内容:
DeepSeek-V3 是由幻方量化（High-Flyer）旗下的 DeepSeek AI 开发的开源大语言模型，于 2024 年发布。
============================================================
```
