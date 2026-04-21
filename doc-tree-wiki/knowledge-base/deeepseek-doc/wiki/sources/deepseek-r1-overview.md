---
title: "DeepSeek-R1 全面介绍"
type: source
tags:
  - deepseek
  - reasoning-model
  - reinforcement-learning
  - open-source
sources:
  - raw/deepseek-r1-overview.md
last_updated: 2026-04-21
---

# DeepSeek-R1 全面介绍

> **发布时间**：2025 年 1 月 20 日  
> **开发方**：DeepSeek（深度求索，中国）  
> **许可证**：MIT（可商用、可蒸馏）

## 核心要点

- **发布时间**：2025 年 1 月 20 日
- **开发方**：DeepSeek（深度求索，中国）
- **许可证**：MIT（可商用、可蒸馏）
- **总参数量**：671B
- **推理时激活参数**：37B（MoE 架构）
- **训练方法**：纯强化学习（GRPO）
- **性能**：与 OpenAI o1 相当

## 关键技术

| 特性 | 详情 |
|------|------|
| 总参数量 | 671B |
| 推理时激活参数 | 37B（MoE 架构，按需激活） |
| 架构 | Mixture of Experts（MoE） |
| 训练方法 | GRPO，纯强化学习 |
| 上下文长度 | 64K tokens（原版）|
| 知识截止日期 | 2024 年 7 月 |

## 能力表现

- **数学**：AIME 数学竞赛 pass@1 约 **79.8%**，MATH-500 约 **97.3%**
- **代码**：Codeforces Elo 约 **2029**
- **推理**：多项复杂推理基准与 OpenAI o1 持平
- **支持显式思维链**：输出中包含完整的 `<think>` 推理过程

## 蒸馏版本

| 模型 | 基础架构 |
|------|---------|
| R1-Distill-Qwen-1.5B | Qwen2.5 |
| R1-Distill-Qwen-7B | Qwen2.5 |
| R1-Distill-Qwen-14B | Qwen2.5 |
| R1-Distill-Qwen-32B | Qwen2.5 |
| R1-Distill-Llama-8B | LLaMA-3 |
| R1-Distill-Llama-70B | LLaMA-3 |

## 成本优势

相比 OpenAI o1，R1 的 API 调用成本大约只有其 **15%–50%**。

## 版本演进

| 时间 | 版本 | 主要变化 |
|------|------|---------|
| 2025-01 | R1（原版）| 首发，纯 RL 推理模型 |
| 2025-05 | R1-0528 | 推理质量大幅提升，新增结构化 JSON 输出、函数调用 |

## 局限性

- 不支持图像等多模态输入（纯文本模型）
- 原版上下文窗口为 64K，低于部分竞品
- 中国公司开发，存在数据隐私与合规方面的顾虑
- 部分地区访问官方 API 存在网络限制
