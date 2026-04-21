---
name: wiki-graph
description: "构建知识图谱，解析 wikilinks + Louvain 社区检测 + vis.js 可视化。场景：需要更新图谱、查看页面关系、生成交互式可视化时"
---

# Wiki Graph

知识图谱构建 skill，调用 `scripts/build_graph.py`。

## 调用

```bash
python scripts/build_graph.py              # 确定性构建（EXTRACTED 边）
python scripts/build_graph.py --open        # 构建后打开 graph.html
python scripts/build_graph.py --report      # 生成健康报告
python scripts/build_graph.py --save        # 保存报告到 graph/graph-report.md
```

## 工作流程

1. **脚本** `extract_wikilinks()` — 解析所有页面的 [[wikilinks]]
2. **脚本** `build_extracted_edges()` — 构建 EXTRACTED 类型的边（置信度 1.0）
3. **脚本** `detect_communities()` — Louvain 社区检测（使用 networkx）
4. **脚本** `render_html()` — 生成 vis.js 可视化

5. **Claude** 读取页面内容，推断隐含关系
6. **Claude** 调用 `add_inferred_edges()` 将 INFERRED 边追加到 graph.json

## 脚本职责

- wikilink 解析（`extract_wikilinks()`）
- 构建 EXTRACTED 边（`build_extracted_edges()`）
- Louvain 社区检测（`detect_communities()`）
- HTML 可视化生成（`render_html()`）
- graph.json 读写（`add_inferred_edges()`）

## Claude 职责

- 读取页面内容
- 推断 INFERRED 类型的隐含关系边
- 调用 `add_inferred_edges([{"from": "...", "to": "...", "type": "INFERRED", ...}])` 追加到图谱

## 输出

- `graph/graph.json` — 节点和边数据
- `graph/graph.html` — 可交互的 vis.js 可视化
