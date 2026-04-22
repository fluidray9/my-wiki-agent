---
title: "Tree Index"
type: tree-index
kb: "deeepseek-doc"
sources: ['knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md']
generated: 2026-04-22
---

# Tree Index

## DeepSeek-R1 全面介绍
Source: `knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md`

### DeepSeek-R1 全面介绍

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 3, char_start: 20, char_end: 97, keywords: ['发布时间', '2025', '20', '开发方', 'DeepSeek', '深度求索', '中国', '许可证', 'MIT', '可商用'], semantic: "> 发布时间：2025 年 1 月 20 日 > 开发方：DeepSeek（深度求索，中国） > 许可证：MIT（可商用、可蒸馏）", text: "> **发布时间**：2025 年 1 月 20 日 > **开发方**：DeepSeek（深度求索，中国） > **许可证**：MIT（可商用、可蒸馏）"}

### DeepSeek-R1 全面介绍

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 一、是什么

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 11, char_start: 118, char_end: 269, keywords: ['DeepSeek', 'R1', '是一款专注于推理能力的大语言模型', '由中国人工智能公司', '开发', '它以强化学习', 'RL', '为核心训练方法', '让模型通过自我进化习得推理策略', '而非依赖大量人工标注的监督数据'], semantic: "DeepSeek-R1 是一款专注于推理能力的大语言模型，由中国人工智能公司 DeepSeek 开发。它以强化学习（RL）为核心训练方法，让模型通过自我进化习得推理策略，而非依赖大量人工标注的监督数据。其综合性能与 OpenAI o1 相当，但以开源形式发布，引发了全球 AI 社区的广泛关注。", text: "DeepSeek-R1 是一款专注于**推理能力**的大语言模型，由中国人工智能公司 DeepSeek 开发。它以强化学习（RL）为核心训练方法，让模型通过自我进化习得推理策略，而非依赖大量人工标注的监督数据。其综合性能与 OpenAI o1 相当，但以开源形式发布，引发了全球 AI 社区的广泛关注。"}

### 一、是什么

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 二、核心技术

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 17, char_start: 287, char_end: 502, keywords: ['特性', '详情', '总参数量', '671B', '推理时激活参数', '37B', 'MoE', '架构', '按需激活', 'Mixture'], semantic: "| 特性 | 详情 | |------|------| | 总参数量 | 671B | | 推理时激活参数 | 37B（MoE 架构，按需激活） | | 架构 | Mixture of Experts（MoE） | | 训练方法 | Group Relative Policy Optimizatio...", text: "| 特性 | 详情 | |------|------| | 总参数量 | 671B | | 推理时激活参数 | 37B（MoE 架构，按需激活） | | 架构 | Mixture of Experts（MoE） | | 训练方法 | Group Relative Policy Optimization（GRPO），纯强化学习 | | 上下文长度 | 64K tokens（原版）| | 知识截止日期..."}

### 二、核心技术

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 26, char_start: 504, char_end: 567, keywords: ['MoE', '架构的核心思想', '将模型拆分为多个专家子网络', '数学', '代码', '语言等', '每次推理只激活其中一部分', '大幅降低计算成本'], semantic: "MoE 架构的核心思想：将模型拆分为多个专家子网络（数学、代码、语言等），每次推理只激活其中一部分，大幅降低计算成本。", text: "**MoE 架构**的核心思想：将模型拆分为多个专家子网络（数学、代码、语言等），每次推理只激活其中一部分，大幅降低计算成本。"}

### 二、核心技术

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 三、能力与基准表现

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 32, char_start: 588, char_end: 768, keywords: ['数学', 'AIME', '数学竞赛', 'pass', '79', 'MATH', '500', '97', '代码', 'Codeforces'], semantic: "- 数学：AIME 数学竞赛 pass@1 约 79.8%，MATH-500 约 97.3% - 代码：Codeforces Elo 约 2029，超越此前开源最优水平 - 推理：多项复杂推理基准与 OpenAI o1 持平 - 支持显式思维链：输出中包含完整的 <think> 推理过程，透明可检查", text: "- **数学**：AIME 数学竞赛 pass@1 约 **79.8%**，MATH-500 约 **97.3%** - **代码**：Codeforces Elo 约 **2029**，超越此前开源最优水平 - **推理**：多项复杂推理基准与 OpenAI o1 持平 - **支持显式思维链**：输出中包含完整的 `<think>` 推理过程，透明可检查"}

### 三、能力与基准表现

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 四、蒸馏版本（Distill 系列）

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 41, char_start: 798, char_end: 835, keywords: ['DeepSeek', '同步发布了基于', 'R1', '知识蒸馏的轻量版本', '适合本地部署'], semantic: "DeepSeek 同步发布了基于 R1 知识蒸馏的轻量版本，适合本地部署：", text: "DeepSeek 同步发布了基于 R1 知识蒸馏的轻量版本，适合本地部署："}

### 四、蒸馏版本（Distill 系列）

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 43, char_start: 837, char_end: 1074, keywords: ['模型', '基础架构', 'R1', 'Distill', 'Qwen', '5B', 'Qwen2', '7B', '14B', '32B'], semantic: "| 模型 | 基础架构 | |------|---------| | R1-Distill-Qwen-1.5B | Qwen2.5 | | R1-Distill-Qwen-7B | Qwen2.5 | | R1-Distill-Qwen-14B | Qwen2.5 | | R1-Distill-Qw...", text: "| 模型 | 基础架构 | |------|---------| | R1-Distill-Qwen-1.5B | Qwen2.5 | | R1-Distill-Qwen-7B | Qwen2.5 | | R1-Distill-Qwen-14B | Qwen2.5 | | R1-Distill-Qwen-32B | Qwen2.5 | | R1-Distill-Llama-8B | LLaMA-3..."}

### 四、蒸馏版本（Distill 系列）

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 五、成本优势

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 56, char_start: 1092, char_end: 1188, keywords: ['相比', 'OpenAI', 'o1', 'R1', 'API', '调用成本大约只有其', '15', '50', 'Fireworks', 'AI'], semantic: "相比 OpenAI o1，R1 的 API 调用成本大约只有其 15%–50%。以 Fireworks AI 为例，输入/输出均为 $8/百万 tokens，而 o1 的价格远高于此。", text: "相比 OpenAI o1，R1 的 API 调用成本大约只有其 **15%–50%**。以 Fireworks AI 为例，输入/输出均为 $8/百万 tokens，而 o1 的价格远高于此。"}

### 五、成本优势

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 六、开源与影响

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 62, char_start: 1207, char_end: 1322, keywords: ['MIT', '许可证', '允许商用', '二次开发', '蒸馏部署', '完整技术报告开放', '训练流程', '架构细节全部公开', '训练成本极低', '挑战了'], semantic: "- MIT 许可证：允许商用、二次开发、蒸馏部署 - 完整技术报告开放：训练流程、架构细节全部公开 - 训练成本极低，挑战了"顶级 AI 必须耗费巨额算力"的行业共识 - 引发市场对英伟达等 GPU 厂商的重新估值", text: "- **MIT 许可证**：允许商用、二次开发、蒸馏部署 - **完整技术报告开放**：训练流程、架构细节全部公开 - 训练成本极低，挑战了"顶级 AI 必须耗费巨额算力"的行业共识 - 引发市场对英伟达等 GPU 厂商的重新估值"}

### 六、开源与影响

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 七、版本演进

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 71, char_start: 1340, char_end: 1488, keywords: ['时间', '版本', '主要变化', '2025', '01', 'R1', '原版', '首发', 'RL', '推理模型'], semantic: "| 时间 | 版本 | 主要变化 | |------|------|---------| | 2025-01 | R1（原版）| 首发，纯 RL 推理模型 | | 2025-05 | R1-0528 | 推理质量大幅提升，新增结构化 JSON 输出、函数调用，无需手动插入 <think> |", text: "| 时间 | 版本 | 主要变化 | |------|------|---------| | 2025-01 | R1（原版）| 首发，纯 RL 推理模型 | | 2025-05 | R1-0528 | 推理质量大幅提升，新增结构化 JSON 输出、函数调用，无需手动插入 `<think>` |"}

### 七、版本演进

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 八、局限性

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 80, char_start: 1505, char_end: 1608, keywords: ['不支持图像等多模态输入', '纯文本模型', '原版上下文窗口为', '64K', '低于部分竞品', '中国公司开发', '存在数据隐私与合规方面的顾虑', '尤其在医疗', '金融等敏感领域', '部分地区访问官方'], semantic: "- 不支持图像等多模态输入（纯文本模型） - 原版上下文窗口为 64K，低于部分竞品 - 中国公司开发，存在数据隐私与合规方面的顾虑（尤其在医疗、金融等敏感领域） - 部分地区访问官方 API 存在网络限制", text: "- 不支持图像等多模态输入（纯文本模型） - 原版上下文窗口为 64K，低于部分竞品 - 中国公司开发，存在数据隐私与合规方面的顾虑（尤其在医疗、金融等敏感领域） - 部分地区访问官方 API 存在网络限制"}

### 八、局限性

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 通过官方 API（兼容 OpenAI SDK）

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 99, char_start: 1866, char_end: 1916, keywords: ['也可通过', 'OpenRouter', 'Fireworks', 'AI', 'Together', '等第三方平台调用'], semantic: "也可通过 OpenRouter、Fireworks AI、Together AI 等第三方平台调用。", text: "也可通过 OpenRouter、Fireworks AI、Together AI 等第三方平台调用。"}

### 通过官方 API（兼容 OpenAI SDK）

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 7, char_start: 103, char_end: 106, keywords: [], semantic: "---", text: "---"}

### 十、总结

- {file: "knowledge-base/deeepseek-doc/raw/deeepseek-r1-overview.md", line: 105, char_start: 1932, char_end: 2039, keywords: ['DeepSeek', 'R1', '2025', '年初最具影响力的开源', 'AI', '事件之一', '它证明了用强化学习而非海量监督数据也能训练出顶尖推理模型', '同时以极低成本和', 'MIT', '开源协议向全球开放'], semantic: "DeepSeek-R1 是 2025 年初最具影响力的开源 AI 事件之一。它证明了用强化学习而非海量监督数据也能训练出顶尖推理模型，同时以极低成本和 MIT 开源协议向全球开放，深刻改变了大模型竞争格局。", text: "DeepSeek-R1 是 2025 年初最具影响力的开源 AI 事件之一。它证明了**用强化学习而非海量监督数据**也能训练出顶尖推理模型，同时以极低成本和 MIT 开源协议向全球开放，深刻改变了大模型竞争格局。"}
