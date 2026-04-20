---
name: wiki-maintenance
description: "执行 wiki 全面体检，依次调用 health/lint/heal/refresh 检查并修复问题。场景：需要对 wiki 进行定期维护、检查结构完整性和内容质量时"
---

# Wiki Maintenance

维护调度 skill，无独立 Python 脚本，依次调用子 skill。

## 工作流程

1. **wiki-health** — 结构检查
   - 空文件/残缺文件
   - index 同步
   - log 覆盖
2. **wiki-fix（lint）** — 语义检查（如 health 通过）
   - 孤立页面
   - 断链
   - 矛盾
   - 缺失 entity
   - 数据空白
3. **wiki-fix（heal）** — 自动修复（如发现缺失 entity）
4. **wiki-refresh** — 检查过时 source（可选）
5. **汇总报告** — 整理所有检查结果

## 顺序说明

- health 必须在 fix 之前（lint 检查语义，结构有问题则跳过）
- heal 在 lint 之后（lint 发现缺失 entity，heal 修复）
- refresh 可选（手动触发，不自动跑）

## 输出

- health 报告
- lint 报告
- heal 修复列表（如有）
- refresh 结果（如执行）
- 最终维护汇总