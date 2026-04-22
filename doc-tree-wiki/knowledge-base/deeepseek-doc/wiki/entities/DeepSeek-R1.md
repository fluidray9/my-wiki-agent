---
title: DeepSeek-R1
type: entity
tags: [模型, 推理, 开源, MoE]
sources: [raw/deeepseek-doc/deepseek-r1-overview.md]
last_updated: 2026-04-22
---

# DeepSeek-R1

**DeepSeek-R1** 是一款专注于**推理能力**的大语言模型，由 DeepSeek 开发。2025 年 1 月 20 日发布，以 MIT 许可证开源，综合性能与 OpenAI o1 相当。

## 核心参数

| 特性 | 详情 |
|------|------|
| 总参数量 | 671B |
| 推理时激活参数 | 37B（MoE 架构） |
| 架构 | Mixture of Experts（MoE） |
| 训练方法 | GRPO（纯强化学习） |
| 上下文长度 | 64K tokens |
| 知识截止日期 | 2024 年 7 月 |

## 能力表现

- **数学**：AIME pass@1 约 79.8%，MATH-500 约 97.3%
- **代码**：Codeforces Elo 约 2029
- **推理**：与 OpenAI o1 持平
- **显式思维链**：输出包含完整推理过程

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

API 调用成本约为 OpenAI o1 的 **15%–50%**。

## 局限性

- 不支持多模态输入（纯文本模型）
- 上下文窗口 64K
- 数据隐私与合规顾虑（敏感领域）
- 部分地区访问受限

## 相关实体

- [[DeepSeek]] — 开发公司

## 相关概念

- [[MoE]] — 架构基础
- [[GRPO]] — 训练方法
- [[Knowledge-Distillation]] — 蒸馏技术
- [[Reinforcement-Learning]] — 强化学习
