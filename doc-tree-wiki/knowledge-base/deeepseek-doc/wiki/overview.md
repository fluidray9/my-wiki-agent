---
title: "Overview - DeepSeek-R1 Knowledge Base"
type: synthesis
last_updated: 2026-04-21
---

# DeepSeek-R1 Knowledge Base

DeepSeek-R1 是 2025 年初最具影响力的开源 AI 事件之一。它证明了**用强化学习而非海量监督数据**也能训练出顶尖推理模型。

## 核心信息

- **开发者**：DeepSeek（深度求索，中国）
- **发布时间**：2025 年 1 月 20 日
- **许可证**：MIT（可商用、可蒸馏）
- **性能**：与 OpenAI o1 相当的推理能力

## 技术亮点

1. **MoE 架构**：671B 总参数，推理时只激活 37B
2. **GRPO 训练**：纯强化学习方法，无需大量监督数据
3. **蒸馏系列**：提供 1.5B-70B 的轻量版本
4. **成本优势**：API 成本约为 OpenAI o1 的 15%-50%

## 能力表现

| 领域 | 表现 |
|------|------|
| 数学 | AIME 79.8%, MATH-500 97.3% |
| 代码 | Codeforces Elo 2029 |
| 综合推理 | 与 OpenAI o1 持平 |

## 局限性

- 不支持多模态输入
- 64K 上下文窗口
- 数据隐私顾虑（尤其敏感领域）
- 部分地区网络访问限制

## 来源

本知识库基于 [deepseek-r1-overview](sources/deepseek-r1-overview.md) 构建。
