---
title: "GRPO (Group Relative Policy Optimization)"
type: concept
tags:
  - training
  - reinforcement-learning
  - optimization
sources:
  - sources/deepseek-r1-overview.md
last_updated: 2026-04-21
---

# GRPO (Group Relative Policy Optimization)

GRPO 是 DeepSeek-R1 使用的核心训练方法，全称为 Group Relative Policy Optimization。它是一种纯强化学习方法，让模型通过自我进化习得推理策略，而非依赖大量人工标注的监督数据。

## 核心思想

- **无需监督数据**：传统 LLM 依赖大量人工标注的 training data，GRPO 完全通过强化学习训练
- **自我进化**：模型通过试错学习推理策略
- **相对比较**：使用组内相对比较来优化策略

## 与传统方法对比

| 方面 | 传统 SFT | GRPO |
|------|---------|------|
| 数据需求 | 大量人工标注 | 无需标注 |
| 训练方式 | 监督学习 | 强化学习 |
| 推理能力 | 一般 | 强 |
| 成本 | 高 | 较低 |

## 相关链接

- [DeepSeek-R1](entities/DeepSeek-R1.md)
- [Reinforcement Learning](concepts/Reinforcement-Learning.md)
