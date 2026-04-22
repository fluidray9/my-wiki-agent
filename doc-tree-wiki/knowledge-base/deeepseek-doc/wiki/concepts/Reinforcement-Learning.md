---
title: Reinforcement Learning
type: concept
tags: [强化学习, AI训练, 推理]
sources: [raw/deeepseek-doc/deepseek-r1-overview.md]
last_updated: 2026-04-22
---

# Reinforcement Learning（强化学习）

**强化学习（RL）** 是 DeepSeek-R1 的核心训练方法，让模型通过与环境交互、自我试错来学习最优策略，而非依赖大量人工标注的监督数据。

## GRPO

DeepSeek-R1 使用 **GRPO**（Group Relative Policy Optimization）作为具体训练方法。

## 在 DeepSeek-R1 中的应用

- 纯强化学习训练，无需监督微调
- 模型通过自我进化习得推理策略
- 综合性能与 OpenAI o1 持平

## 相关模型

- [[DeepSeek-R1]] — 使用强化学习训练
