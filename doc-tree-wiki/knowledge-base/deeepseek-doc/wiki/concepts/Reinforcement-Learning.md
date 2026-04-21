---
title: "Reinforcement Learning"
type: concept
tags:
  - machine-learning
  - training-method
sources:
  - sources/deepseek-r1-overview.md
last_updated: 2026-04-21
---

# Reinforcement Learning (强化学习)

强化学习是机器学习的一个重要分支，模型通过与环境交互，以试错方式学习最优策略。DeepSeek-R1 采用纯强化学习（GRPO）作为核心训练方法，证明了无需大量监督数据也能训练出顶尖推理模型。

## 核心概念

- **Agent（智能体）**：模型本身
- **Environment（环境）**：模型所处的任务环境
- **Policy（策略）**：模型做出决策的方式
- **Reward（奖励）**：衡量动作好坏的目标

## 在 LLM 训练中的应用

- **传统方法**：使用大量人工标注的监督数据进行 SFT（Supervised Fine-Tuning）
- **RL 方法**：如 GRPO，通过奖励信号让模型自我学习推理策略

## 相关链接

- [DeepSeek-R1](entities/DeepSeek-R1.md)
- [GRPO](concepts/GRPO.md)
