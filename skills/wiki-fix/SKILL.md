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

## 功能

### lint.py — 检查

1. **孤立页面** — 没有其他页面链接到它
2. **断链** — `[[wikilinks]]` 指向不存在的页面
3. **矛盾** — 页面间的冲突声明
4. **过时的摘要** — 被新源超越的摘要
5. **缺失 entity** — 在 3+ 页面提及但没有自身页面的实体
6. **数据空白** — wiki 无法回答的重要问题

### heal.py — 修复

自动为缺失的 entity 生成定义页面：
1. 找到所有缺失 entity
2. 搜索引用该 entity 的页面
3. 提取上下文
4. 调用 LLM 生成 entity 页面
5. 保存到 `wiki/entities/<EntityName>.md`

## 工作流

通常 `wiki-maintenance` 会依次调用：
1. `python scripts/lint.py` — 检查问题
2. `python scripts/heal.py` — 修复缺失 entity