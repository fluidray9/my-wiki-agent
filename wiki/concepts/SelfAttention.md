---
title: "Self-Attention"
type: concept
tags: [mechanism, neural-network]
sources: [transformer-architecture]
last_updated: 2026-04-21
---

# Self-Attention

Self-Attention is a mechanism that allows each position in a sequence to attend to all positions in the same sequence. It is the core component of the Transformer architecture.

## How It Works
- Computes attention weights between all pairs of positions
- Allows modeling long-range dependencies
- Enables parallel computation (unlike RNNs)

## Key Properties
- **Multi-head attention**: Multiple attention heads can capture different relationships
- **Scaled dot-product**: Attention scores are scaled to prevent gradient instability

## Connections
- [[TransformerArchitecture]] — the architecture that uses self-attention
- [[BERT]] — uses self-attention
- [[GPT]] — uses self-attention