---
title: Knowledge Distillation
type: concept
tags: [知识蒸馏, 训练方法, 轻量模型]
sources: [raw/deeepseek-doc/deepseek-r1-overview.md]
last_updated: 2026-04-22
---

# Knowledge Distillation（知识蒸馏）

**知识蒸馏**是将大型模型（教师模型）的知识迁移到小型模型（学生模型）的技术。DeepSeek 同步发布了基于 R1 知识蒸馏的轻量版本，适合本地部署。

## DeepSeek 蒸馏系列

| 模型 | 基础架构 |
|------|---------|
| R1-Distill-Qwen-1.5B | Qwen2.5 |
| R1-Distill-Qwen-7B | Qwen2.5 |
| R1-Distill-Qwen-14B | Qwen2.5 |
| R1-Distill-Qwen-32B | Qwen2.5 |
| R1-Distill-Llama-8B | LLaMA-3 |
| R1-Distill-Llama-70B | LLaMA-3 |

## 优势

- 保持大模型核心能力
- 大幅降低计算资源需求
- 适合本地部署和边缘设备

## 相关模型

- [[DeepSeek-R1]] — 教师模型
