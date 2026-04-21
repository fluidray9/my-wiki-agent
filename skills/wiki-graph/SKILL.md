---
name: wiki-graph
description: "构建知识图谱，解析 wikilinks + Louvain 社区检测 + vis.js 可视化。场景：需要更新图谱、查看页面关系、生成交互式可视化时"
---

# Wiki Graph

构建知识图谱。**Agent 手动推断隐含关系，脚本处理确定性构建**。

## 命令行用法

```bash
python scripts/build_graph.py              # 确定性构建（EXTRACTED 边）
python scripts/build_graph.py --open        # 构建后打开 graph.html
python scripts/build_graph.py --report      # 生成健康报告
python scripts/build_graph.py --save        # 保存报告到 graph/graph-report.md
```

## 工作流程

**Pass 1: 确定性构建（脚本）**
1. **脚本** `extract_wikilinks()` — 解析所有页面的 [[wikilinks]]
2. **脚本** `build_extracted_edges()` — 构建 EXTRACTED 类型的边（置信度 1.0）
3. **脚本** `detect_communities()` — Louvain 社区检测
4. **脚本** `render_html()` — 生成 vis.js 可视化

**Pass 2: 隐含关系推断（Agent）**
5. **Agent** 读取页面内容，推断隐含关系
6. **Agent** 将 INFERRED 边追加到 graph.json

## 脚本函数

```python
# 追加隐含关系边（Agent 调用）
add_inferred_edges([{"from": "PageA", "to": "PageB", "type": "INFERRED", "confidence": 0.8, "reason": "..."}])
```

## 图谱结构

| 类型 | 说明 |
|------|------|
| EXTRACTED | 直接从 wikilink 提取，置信度 1.0 |
| INFERRED | Agent 推断的隐含关系 |
| AMBIGUOUS | 关系不明确 |

## Agent 职责

- 读取 wiki 页面内容
- 推断隐含关系（如 "A 和 B 都提到了 X，所以可能相关"）
- 调用 `add_inferred_edges()` 追加到图谱

## 输出

- `graph/graph.json` — 节点和边数据
- `graph/graph.html` — 可交互 vis.js 可视化