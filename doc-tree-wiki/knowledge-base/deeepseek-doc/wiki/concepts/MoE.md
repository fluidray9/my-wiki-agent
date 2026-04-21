---
title: "MoE (Mixture of Experts)"
type: concept
tags:
  - architecture
  - MoE
  - deep-learning
sources:
  - sources/deepseek-r1-overview.md
last_updated: 2026-04-21
---

# MoE (Mixture of Experts)

MoE（Mixture of Experts，混合专家）是一种神经网络架构设计，将模型拆分为多个专家子网络（数学、代码、语言等），每次推理只激活其中一部分，从而大幅降低计算成本。

## 核心思想

- 将模型拆分为多个"专家"子网络
- 每个子网络擅长处理不同类型的任务
- 每次推理只激活相关的少数专家
- 大幅降低计算成本的同时保持模型容量

## 在 DeepSeek-R1 中的应用

| 特性 | 详情 |
|------|------|
| 总参数量 | 671B |
| 推理时激活参数 | 37B |
| 架构类型 | MoE |

## 优势

- **计算效率**：推理时只激活 37B 参数，而非全部 671B
- **模型容量**：保持大规模参数带来的能力
- **专业化**：不同专家可专注于不同领域

## 相关链接

- [DeepSeek-R1](entities/DeepSeek-R1.md)
- [DeepSeek](entities/DeepSeek.md)
