# DeepSeek-V3 技术解读

DeepSeek-V3 是由幻方量化（High-Flyer）旗下的 DeepSeek AI 开发的开源大语言模型，于 2024 年发布。该模型在多项基准测试中表现优异，超越了 Llama 3.1 405B 等竞品。

## 核心技术

- **MoE 架构**：DeepSeek-V3 采用混合专家（Mixture of Experts）架构，总参数 671B，激活参数 37B
- **多头潜在注意力（MLA）**：创新注意力机制，显著降低推理成本
- **FP8 混合精度训练**：支持 FP8 精度训练，大幅提升训练效率

## 关键创新

1. **无辅助损失负载均衡**：通过自适应策略实现专家负载均衡，避免传统辅助损失带来的性能损失
2. **双周排练（DualPipe）**：创新的并行策略，减少流水线气泡
3. **跨节点专家并行**：支持大规模分布式训练

## 团队成员

- **梁文峰（Lei Wang）**：DeepSeek 创始人兼 CEO，幻方量化创始人
- **曾艳庆（Yanqing Zeng）**：DeepSeek 核心研究员
- **谢慈航（Cihang Xie）**：DeepSeek 核心研究员

## 相关概念

- 混合专家模型（MoE）
- 大语言模型（LLM）
- 模型蒸馏
- 模型量化

## 相关公司/组织

- DeepSeek AI
- 幻方量化（High-Flyer）
- 沐曦集成科技（MetaX）