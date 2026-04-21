---
title: "Tree Index"
type: tree-index
kb: "deepseek-kb"
sources: ['knowledge-base/deepseek-kb/raw/deepseek-v3-extra.md', 'knowledge-base/deepseek-kb/raw/deepseek-v3.md']
generated: 2026-04-21
---

# Tree Index

## DeepSeek-V3 补充信息
Source: `knowledge-base/deepseek-kb/raw/deepseek-v3-extra.md`

### DeepSeek-V3 补充信息

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3-extra.md", line: 3, char_start: 20, char_end: 95, keywords: ['关于', 'DeepSeek', 'V3', '的发布时间存在不同说法', '最新资料显示', '实际上于', '2025', '发布', '而非', '2024'], semantic: "关于 DeepSeek-V3 的发布时间存在不同说法。最新资料显示 DeepSeek-V3 实际上于 2025 年 发布，而非 2024 年。", text: "关于 DeepSeek-V3 的发布时间存在不同说法。最新资料显示 DeepSeek-V3 实际上于 **2025 年** 发布，而非 2024 年。"}

### 团队补充

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3-extra.md", line: 7, char_start: 106, char_end: 180, keywords: ['估计', '据内部消息', 'DeepSeek', 'V3', '的研发团队规模约', '100', '资金', '获得了幻方量化的持续资金支持'], semantic: "- 估计：据内部消息，DeepSeek-V3 的研发团队规模约 100 人 - 资金：DeepSeek 获得了幻方量化的持续资金支持", text: "- **估计**：据内部消息，DeepSeek-V3 的研发团队规模约 100 人 - **资金**：DeepSeek 获得了幻方量化的持续资金支持"}

### 技术补充

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3-extra.md", line: 12, char_start: 191, char_end: 289, keywords: ['推理优化', 'DeepSeek', 'V3', '在推理时采用了', 'Continuous', 'Batching', '技术', '显著提升了吞吐量', '开源策略', '采用'], semantic: "- 推理优化：DeepSeek-V3 在推理时采用了 Continuous Batching 技术，显著提升了吞吐量 - 开源策略：DeepSeek 采用 MIT 许可证，完全开源", text: "- **推理优化**：DeepSeek-V3 在推理时采用了 Continuous Batching 技术，显著提升了吞吐量 - **开源策略**：DeepSeek 采用 MIT 许可证，完全开源"}

## DeepSeek-V3 技术解读
Source: `knowledge-base/deepseek-kb/raw/deepseek-v3.md`

### DeepSeek-V3 技术解读

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3.md", line: 3, char_start: 20, char_end: 127, keywords: ['DeepSeek', 'V3', '是由幻方量化', 'High', 'Flyer', '旗下的', 'AI', '开发的开源大语言模型', '2024', '年发布'], semantic: "DeepSeek-V3 是由幻方量化（High-Flyer）旗下的 DeepSeek AI 开发的开源大语言模型，于 2024 年发布。该模型在多项基准测试中表现优异，超越了 Llama 3.1 405B 等竞品。", text: "DeepSeek-V3 是由幻方量化（High-Flyer）旗下的 DeepSeek AI 开发的开源大语言模型，于 2024 年发布。该模型在多项基准测试中表现优异，超越了 Llama 3.1 405B 等竞品。"}

### 核心技术

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3.md", line: 7, char_start: 138, char_end: 283, keywords: ['MoE', '架构', 'DeepSeek', 'V3', '采用混合专家', 'Mixture', 'Experts', '总参数', '671B', '激活参数'], semantic: "- MoE 架构：DeepSeek-V3 采用混合专家（Mixture of Experts）架构，总参数 671B，激活参数 37B - 多头潜在注意力（MLA）：创新注意力机制，显著降低推理成本 - FP8 混合精度训练：支持 FP8 精度训练，大幅提升训练效率", text: "- **MoE 架构**：DeepSeek-V3 采用混合专家（Mixture of Experts）架构，总参数 671B，激活参数 37B - **多头潜在注意力（MLA）**：创新注意力机制，显著降低推理成本 - **FP8 混合精度训练**：支持 FP8 精度训练，大幅提升训练效率"}

### 关键创新

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3.md", line: 13, char_start: 294, char_end: 406, keywords: ['无辅助损失负载均衡', '通过自适应策略实现专家负载均衡', '避免传统辅助损失带来的性能损失', '双周排练', 'DualPipe', '创新的并行策略', '减少流水线气泡', '跨节点专家并行', '支持大规模分布式训练'], semantic: "1. 无辅助损失负载均衡：通过自适应策略实现专家负载均衡，避免传统辅助损失带来的性能损失 2. 双周排练（DualPipe）：创新的并行策略，减少流水线气泡 3. 跨节点专家并行：支持大规模分布式训练", text: "1. **无辅助损失负载均衡**：通过自适应策略实现专家负载均衡，避免传统辅助损失带来的性能损失 2. **双周排练（DualPipe）**：创新的并行策略，减少流水线气泡 3. **跨节点专家并行**：支持大规模分布式训练"}

### 团队成员

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3.md", line: 19, char_start: 417, char_end: 538, keywords: ['梁文峰', 'Lei', 'Wang', 'DeepSeek', '创始人兼', 'CEO', '幻方量化创始人', '曾艳庆', 'Yanqing', 'Zeng'], semantic: "- 梁文峰（Lei Wang）：DeepSeek 创始人兼 CEO，幻方量化创始人 - 曾艳庆（Yanqing Zeng）：DeepSeek 核心研究员 - 谢慈航（Cihang Xie）：DeepSeek 核心研究员", text: "- **梁文峰（Lei Wang）**：DeepSeek 创始人兼 CEO，幻方量化创始人 - **曾艳庆（Yanqing Zeng）**：DeepSeek 核心研究员 - **谢慈航（Cihang Xie）**：DeepSeek 核心研究员"}

### 相关概念

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3.md", line: 25, char_start: 549, char_end: 589, keywords: ['混合专家模型', 'MoE', '大语言模型', 'LLM', '模型蒸馏', '模型量化'], semantic: "- 混合专家模型（MoE） - 大语言模型（LLM） - 模型蒸馏 - 模型量化", text: "- 混合专家模型（MoE） - 大语言模型（LLM） - 模型蒸馏 - 模型量化"}

### 相关公司/组织

- {file: "knowledge-base/deepseek-kb/raw/deepseek-v3.md", line: 32, char_start: 603, char_end: 651, keywords: ['DeepSeek', 'AI', '幻方量化', 'High', 'Flyer', '沐曦集成科技', 'MetaX'], semantic: "- DeepSeek AI - 幻方量化（High-Flyer） - 沐曦集成科技（MetaX）", text: "- DeepSeek AI - 幻方量化（High-Flyer） - 沐曦集成科技（MetaX）"}
