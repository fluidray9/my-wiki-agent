---
name: wiki-query
description: "从 wiki 中检索信息并综合回答，支持保存为 synthesis。场景：需要从 wiki 查找信息、回答问题、综合多个页面的内容时"
---

# Wiki Query

查询 wiki skill，调用 `scripts/query.py`。

## 调用

```bash
python scripts/query.py "问题内容"
python scripts/query.py "问题内容" --save           # 保存到 synthesis
python scripts/query.py "问题内容" --save synthesis/my-analysis.md  # 保存到指定路径
```

## 工作流程

1. 读取 `wiki/index.md` 找相关页面
2. 用关键词匹配或 LLM 选择相关页面（最多 15 个）
3. 读取相关页面内容
4. 调用 LLM 综合回答，使用 `[[wikilink]]` 引用来源
5. 询问是否保存为 synthesis 页面

## Graph 扩展（可选）

如 `graph/graph.json` 存在，可利用邻居扩展找到更多相关页面

## 输出

- 综合回答（Markdown 格式）
- 末尾的 ## Sources 列出引用页面
- 可选保存到 `wiki/syntheses/<slug>.md`