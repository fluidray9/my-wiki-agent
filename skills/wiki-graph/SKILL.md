---
name: wiki-graph
description: "构建知识图谱：解析 wikilinks + LLM 推断 + Louvain 社区检测 + vis.js 可视化"
---

# Wiki Graph

知识图谱构建 skill，调用 `tools/build_graph.py`。

## 调用

```bash
python tools/build_graph.py              # 完整构建
python tools/build_graph.py --no-infer    # 跳过 LLM 推断（更快）
python tools/build_graph.py --open        # 构建后打开 graph.html
python tools/build_graph.py --clean       # 清除缓存，强制重新推断
python tools/build_graph.py --report      # 生成健康报告
python tools/build_graph.py --save        # 保存报告到 graph/graph-report.md
```

## 两阶段构建

**Pass 1 — 确定性解析：**
- 扫描所有 wiki 页面中的 `[[wikilinks]]`
- 生成 EXTRACTED 边（置信度 1.0）

**Pass 2 — LLM 推断：**
- 对每个页面调用 LLM 推断隐含关系
- 生成 INFERRED 边（置信度 ≥ 0.7）或 AMBIGUOUS 边（< 0.7）
- 支持断点续传（.cache.json）

## 输出

- `graph/graph.json` — 节点和边数据
- `graph/graph.html` — 可交互的 vis.js 可视化