---
title: "DeepSeek-R1"
type: entity
tags:
  - model
  - reasoning
  - LLM
sources:
  - sources/deepseek-r1-overview.md
last_updated: 2026-04-21
---

# DeepSeek-R1

DeepSeek-R1 是一款专注于**推理能力**的大语言模型，由中国人工智能公司 DeepSeek 开发。它以强化学习（RL）为核心训练方法，让模型通过自我进化习得推理策略，而非依赖大量人工标注的监督数据。

## 核心参数

| 特性 | 详情 |
|------|------|
| 总参数量 | 671B |
| 推理时激活参数 | 37B（MoE 架构） |
| 上下文长度 | 64K tokens（原版）|
| 知识截止日期 | 2024 年 7 月 |
| 发布时间 | 2025 年 1 月 20 日 |
| 许可证 | MIT |

## 性能表现

- **数学**：AIME 数学竞赛 pass@1 约 **79.8%**，MATH-500 约 **97.3%**
- **代码**：Codeforces Elo 约 **2029**
- **综合推理**：与 OpenAI o1 持平

## 版本演进

| 时间 | 版本 | 主要变化 |
|------|------|---------|
| 2025-01 | R1（原版）| 首发，纯 RL 推理模型 |
| 2025-05 | R1-0528 | 推理质量大幅提升，新增结构化 JSON 输出、函数调用 |

## 相关概念

- [DeepSeek](entities/DeepSeek.md)
- [MoE](concepts/MoE.md)
- [GRPO](concepts/GRPO.md)
- [Knowledge Distillation](concepts/Knowledge-Distillation.md)
