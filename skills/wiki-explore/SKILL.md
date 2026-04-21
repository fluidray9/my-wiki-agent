---
name: wiki-explore
description: "打开知识图谱可视化，展示 wiki 结构关系和统计信息。场景：需要查看 wiki 的整体结构、节点关系、图谱可视化时"
---

# Wiki Explore

探索 wiki 知识图谱。**Agent 调用 wiki-graph 构建图谱，然后打开可视化**。

## 工作流程

1. **检查图谱是否存在**
   - 如 `graph/graph.html` 存在 → 直接打开
   - 如不存在 → 调用 `wiki-graph` 构建

2. **Agent 打开** `graph/graph.html` — 在浏览器中显示

3. **Agent 展示统计** — 节点数、边数、边数/节点比

4. **Agent 引导交互** — 告诉用户如何：
   - 点击节点查看页面内容
   - 筛选边类型（Extracted/Inferred）
   - 调整置信度阈值
   - 搜索特定节点

## 图谱结构

| 元素 | 说明 |
|------|------|
| 节点颜色 | source(绿)、entity(蓝)、concept(橙)、synthesis(紫) |
| 边类型 | EXTRACTED(灰实线)、INFERRED(橙虚线)、AMBIGUOUS(灰虚线) |
| 节点大小 | 按连接度缩放 |

## Agent 职责

- 检查图谱是否存在，不存在则调用 wiki-graph 构建
- 打开 graph.html 可视化
- 展示图谱统计信息
- 引导用户交互

## 输出

- 打开 graph.html
- 显示图谱统计
- 引导下一步操作