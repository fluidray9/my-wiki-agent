---
name: wiki-lint
description: "语义检查：检查 wiki 内容质量（孤立页面、断链、矛盾、数据空白）。需要 LLM 调用，建议每 10-15 次 ingest 后运行。"
---

# Wiki Lint

语义检查 skill，调用 `tools/lint.py`。

## 调用

```bash
python tools/lint.py              # 输出报告到 stdout
python tools/lint.py --save        # 保存报告到 wiki/lint-report.md
```

## 检查项

1. **孤立页面** — 没有其他页面链接到它
2. **断链** — `[[wikilinks]]` 指向不存在的页面
3. **矛盾** — 页面间的冲突声明
4. **过时的摘要** — 被新源超越的摘要
5. **缺失 entity** — 在 3+ 页面提及但没有自身页面的实体
6. **数据空白** — wiki 无法回答的重要问题

## Graph 感知检查（需要 graph.json）

- Hub 残缺 — 高连接度节点内容过少
- 脆弱桥接 — 社区间单边连接
- 孤立社区 — 零外部连接的节点群

## 输出

- Markdown 格式的 lint 报告
- 可选保存到 `wiki/lint-report.md`