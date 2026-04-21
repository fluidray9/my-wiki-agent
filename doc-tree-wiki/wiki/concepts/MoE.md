---
title: "MoE"
type: concept
tags: [architecture, neural-network]
sources: [deepseek-v3]
last_updated: 2026-04-21
---

# MoE（混合专家模型）

混合专家模型（Mixture of Experts）是一种神经网络架构，通过稀疏激活的方式提高模型容量和效率。

## 工作原理
- 模型包含多个"专家"网络
- 每个输入只激活部分专家
- 通过路由机制选择激活哪些专家

## DeepSeek-V3 的 MoE
- 总参数：671B
- 激活参数：37B
- 显著降低了计算成本

## Connections
- [[DeepSeekAI]] — 使用 MoE 架构
- [[大语言模型]] — MoE 用于 LLM
- [[模型蒸馏]] — 相关技术