---
name: wiki-fix
description: "检查 wiki 内容质量问题并自动修复（发现孤立页面、断链、缺失 entity 并修复）。场景：需要检查 wiki 语义完整性、修复缺失 entity 页面时"
---

# Wiki Fix

检查 + 修复 skill，包含 `lint.py` 和 `heal.py`。

## 调用

```bash
# 检查（lint）
python scripts/lint.py
python scripts/lint.py --save        # 保存报告

# 修复（heal）
python scripts/heal.py
```

## Lint 工作流程

**脚本** 运行确定性检查：
1. `find_orphans()` — 检查孤立页面
2. `find_broken_links()` — 检查断链
3. `find_missing_entities()` — 检查缺失 entity（出现≥3次但无页面）
4. `check_hub_stubs()` — Hub 残缺检查（需先运行 build_graph）
5. `check_fragile_bridges()` — 脆弱桥接检查（需先运行 build_graph）
6. `check_isolated_communities()` — 孤立社区检查（需先运行 build_graph）

**Claude** 完成语义检查：
- 矛盾检测 — 对比不同页面的 claims
- 过时检测 — 检查是否有更新的 source
- 数据空白 — 发现 wiki 无法回答的问题

## Heal 工作流程

1. **脚本** `find_missing_entities()` 获取缺失 entity 列表
2. **脚本** `search_sources(entity_name)` 获取引用上下文
3. **Claude** 根据上下文生成 entity 页面内容
4. **Claude** 调用 `save_entity_page(name, content)` 写入文件

## 脚本职责

- 确定性检查函数（find_orphans, find_broken_links, find_missing_entities 等）
- 搜索引用上下文（search_sources）
- 文件写入（save_entity_page）

## Claude 职责

- 语义分析（矛盾、过时、数据空白）
- 生成 entity 页面内容
- 调用 `save_entity_page(name, content)` 写入文件

## 输出

- lint 报告（确定性检查结果 + Claude 语义分析）
- heal 修复列表（如有）
