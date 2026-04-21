---
name: wiki-maintenance
description: "执行 wiki 全面体检，依次调用 health/lint/heal/refresh 检查并修复问题。场景：需要对 wiki 进行定期维护、检查结构完整性和内容质量时"
---

# Wiki Maintenance

wiki 全面维护调度。**Agent 依次调用子 skill 执行检查和修复**。

## 工作流程

1. **wiki-health** — 结构检查（先跑，确保基础没问题）
   - 空文件/残缺文件
   - index 同步
   - log 覆盖

2. **wiki-fix（lint）** — 语义检查（如 health 通过）
   - 孤立页面
   - 断链
   - 矛盾检测（Agent 手动）
   - 缺失 entity
   - 数据空白（Agent 手动）

3. **wiki-fix（heal）** — 自动修复（如 lint 发现缺失 entity）
   - Agent 根据脚本提供的上下文生成缺失 entity

4. **wiki-refresh** — 检查过时 source（可选）

5. **汇总报告** — Agent 整理所有检查结果

## 执行顺序

```
wiki-health → wiki-fix (lint) → wiki-fix (heal) → wiki-refresh (可选)
```

- health 必须在 fix 之前（结构有问题则 lint 无意义）
- heal 在 lint 之后（lint 发现问题，heal 修复）
- refresh 可选（手动触发）

## Agent 职责

- 依次调用各子 skill
- 收集各 skill 的输出结果
- 综合分析并生成维护报告

## 输出

- health 报告
- lint 报告
- heal 修复列表（如有）
- refresh 结果（如执行）
- 最终维护汇总