---
title: GRPO
type: concept
tags: [训练方法, 强化学习, 推理]
sources: [raw/deeepseek-doc/deepseek-r1-overview.md]
last_updated: 2026-04-22
---

# GRPO（Group Relative Policy Optimization）

**GRPO** 是 DeepSeek-R1 使用的训练方法，全称 Group Relative Policy Optimization，属于纯强化学习方法，让模型通过自我进化习得推理策略，而非依赖大量人工标注的监督数据。

## 核心思想

- 无需大量人工标注的监督数据
- 通过相对比较（group relative）优化策略
- 模型自我进化习得推理能力

## 相关模型

- [[DeepSeek-R1]] — 使用 GRPO 训练

## 相关概念

- [[Reinforcement-Learning]] — 强化学习
- [[Knowledge-Distillation]] — 知识蒸馏
