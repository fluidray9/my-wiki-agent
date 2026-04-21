---
title: "Knowledge Distillation"
type: concept
tags:
  - model-compression
  - training
sources:
  - sources/deepseek-r1-overview.md
last_updated: 2026-04-21
---

# Knowledge Distillation (知识蒸馏)

知识蒸馏是将大型模型（Teacher Model）的知识迁移到小型模型（Student Model）的技术。DeepSeek 同步发布了基于 R1 知识蒸馏的轻量版本，适合本地部署。

## 蒸馏原理

- 大模型（Teacher）生成"软标签"或"推理过程"
- 小模型（Student）学习模仿大模型的行为
- 保留大模型大部分能力的同时大幅降低参数量

## DeepSeek-R1 蒸馏版本

| 模型 | 基础架构 | 特点 |
|------|---------|------|
| R1-Distill-Qwen-1.5B | Qwen2.5 | 最小蒸馏版本 |
| R1-Distill-Qwen-7B | Qwen2.5 | 轻量部署 |
| R1-Distill-Qwen-14B | Qwen2.5 | 中等规模 |
| R1-Distill-Qwen-32B | Qwen2.5 | 高性能蒸馏 |
| R1-Distill-Llama-8B | LLaMA-3 | Llama 系列蒸馏 |
| R1-Distill-Llama-70B | LLaMA-3 | 最大蒸馏版本 |

## 部署优势

- 可通过 Ollama 本地运行
- 降低推理成本
- 适合资源受限环境

## 相关链接

- [DeepSeek-R1](entities/DeepSeek-R1.md)
