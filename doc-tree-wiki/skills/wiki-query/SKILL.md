---
name: wiki-query
description: "从知识库 wiki 中检索信息并综合回答，支持保存为 synthesis。场景：需要从 wiki 查找信息、回答问题、综合多个页面的内容时"
---

# Wiki Query

从知识库的 wiki 检索信息并综合回答。**Agent 手动执行，脚本只负责查找页面**。

## KB 参数规则

- `--kb KB_NAME`：指定单个知识库
- `--kb KB1 --kb KB2`：指定多个知识库
- **不指定 `--kb`**：搜索所有知识库

## 工作流程

1. **Agent 读取** `knowledge-base/{kb}/wiki/index.md` 了解 wiki 结构
2. **Agent 查找相关页面** — 根据问题关键词搜索 wiki 目录
3. **Agent 读取相关页面** — 使用 Read 工具获取页面内容
4. **Agent 综合回答** — 基于 wiki 内容生成答案，使用 `[[wikilinks]]` 引用来源
5. **Agent 可选保存** — 调用 `save_synthesis()` 保存为 synthesis 页面

## 脚本函数

```python
# 查找相关页面（返回路径列表，含 KB 信息）
query(question="transformer architecture", kb_list=["deepseek-kb"])
# 返回: [{"kb": "deepseek-kb", "pages": [{"path": "...", "relative": "..."}, ...]}]
```

## 命令行用法

```bash
# 查询指定 KB
python scripts/query.py "transformer architecture" --kb deepseek-kb

# 查询多个 KB
python scripts/query.py "DeepSeek 模型" --kb deepseek-kb --kb other-kb

# 搜索所有 KB
python scripts/query.py "MoE"

# 保存结果
python scripts/query.py "..." --save synthesis/my-analysis.md
```

## Agent 职责

- 读取 wiki/index.md 了解结构
- 分析问题，确定需要查询的页面
- 读取相关页面内容
- 综合回答，使用 `[[WikiLink]]` 引用来源页面
- 决定是否保存为 synthesis

## 输出

- 综合回答（Agent 生成）
- 引用来源（`[[PageName]]` wikilinks）
