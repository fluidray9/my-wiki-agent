---
name: wiki-fix
description: "检查 wiki 内容质量问题并自动修复（发现孤立页面、断链、缺失 entity 并修复）。场景：需要检查 wiki 语义完整性、修复缺失 entity 页面时"
---

# Wiki Fix

检查 + 修复 wiki 内容质量。**Agent 手动执行语义检查，脚本提供确定性检查函数**。

## 命令行用法

```bash
# Lint 检查（确定性检查）
python scripts/lint.py
python scripts/lint.py --save        # 保存报告到 wiki/lint-report.md

# Heal 修复（生成缺失 entity）
python scripts/heal.py
```

## Lint 检查项（Agent 执行）

**确定性检查（脚本）：**
| 检查项 | 函数 |
|--------|------|
| 孤立页面 | `find_orphans()` |
| 断链 | `find_broken_links()` |
| 缺失 entity | `find_missing_entities()` |
| Hub 残缺 | `check_hub_stubs()` |
| 脆弱桥接 | `check_fragile_bridges()` |
| 孤立社区 | `check_isolated_communities()` |

**语义检查（Agent 手动）：**
- 矛盾检测 — 对比不同页面的 claims
- 过时检测 — 检查是否有更新的 source
- 数据空白 — 发现 wiki 无法回答的问题

## Heal 工作流程

1. **脚本** `find_missing_entities()` 获取缺失 entity 列表
2. **脚本** `search_sources(entity_name)` 获取引用上下文
3. **Agent** 根据上下文生成 entity 页面内容
4. **Agent** 写入文件

## Agent 职责

- 运行 lint 脚本获取确定性检查结果
- 手动检查语义（矛盾、过时、数据空白）
- 对 heal 发现的问题，生成缺失 entity 页面内容
- 写入 entity 页面文件

## 输出

- lint 报告（确定性 + Agent 语义分析）
- heal 修复列表（如有）