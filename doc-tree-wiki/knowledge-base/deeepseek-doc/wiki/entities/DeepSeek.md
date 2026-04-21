---
title: "DeepSeek"
type: entity
tags:
  - company
  - AI
  - LLM
sources:
  - sources/deepseek-r1-overview.md
last_updated: 2026-04-21
---

# DeepSeek

DeepSeek（深度求索）是一家中国人工智能公司，专注于开发大语言模型和推理能力。2025年1月发布的 DeepSeek-R1 模型以强化学习为核心训练方法，性能与 OpenAI o1 相当，但以开源 MIT 许可证发布，引发全球 AI 社区广泛关注。

## 核心产品

- **DeepSeek-R1**：专注于推理能力的大语言模型，671B 参数，MoE 架构
- **蒸馏系列**：基于 R1 知识蒸馏的轻量版本（1.5B-70B）

## 关键成就

- 用纯强化学习训练出顶尖推理模型，挑战了"顶级 AI 必须耗费巨额算力"的行业共识
- 以极低成本（约为 OpenAI o1 的 15%-50%）提供 API 服务
- MIT 许可证允许商用、二次开发和蒸馏部署

## 技术特点

- 采用 Group Relative Policy Optimization（GRPO）训练方法
- MoE（Mixture of Experts）架构，推理时只激活 37B 参数
- 支持显式思维链输出

## 相关链接

- [DeepSeek-R1](entities/DeepSeek-R1.md)
- [MoE](concepts/MoE.md)
