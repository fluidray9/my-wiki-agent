---
title: MoE
type: concept
tags: [架构, MoE, 模型结构]
sources: [raw/deeepseek-doc/deepseek-r1-overview.md]
last_updated: 2026-04-22
---

# MoE（Mixture of Experts）

**MoE（Mixture of Experts）** 是一种模型架构，将模型拆分为多个专家子网络（数学、代码、语言等），每次推理只激活其中一部分，从而大幅降低计算成本。

## 在 DeepSeek-R1 中的应用

| 参数 | 值 |
|------|-----|
| 总参数量 | 671B |
| 推理时激活参数 | 37B |

## 核心思想

专家网络各自专注于不同类型的任务或知识领域，gating 机制根据输入动态选择激活哪些专家，避免每次都动用全部参数。

## 相关模型

- [[DeepSeek-R1]] — 使用 MoE 架构
