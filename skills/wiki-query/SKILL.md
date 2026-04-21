---
name: wiki-query
description: "从 wiki 中检索信息并综合回答，支持保存为 synthesis。场景：需要从 wiki 查找信息、回答问题、综合多个页面的内容时"
---

# Wiki Query

查询 wiki skill，调用 `scripts/query.py`。

## 调用

```bash
python scripts/query.py "问题内容"
```

## 工作流程

1. **脚本** `find_relevant_pages()` 读取 index 并匹配相关页面
2. **脚本** 返回页面路径列表给 Claude
3. **Claude** 读取页面内容并综合回答
4. **Claude** 可调用 `save_synthesis()` 保存为 synthesis 页面

## 脚本职责

- 读取 `wiki/index.md`
- 关键词匹配找相关页面（`find_relevant_pages()`）
- Graph 扩展（如 `graph/graph.json` 存在，利用邻居扩展）
- 返回页面路径列表

## Claude 职责

- 读取相关页面内容
- 综合回答问题，使用 `[[wikilink]]` 引用来源
- 决定是否保存为 synthesis
- 调用 `save_synthesis(save_path, content, question)` 保存

## 输出

- 综合回答（Claude 生成）
- 引用来源列表
