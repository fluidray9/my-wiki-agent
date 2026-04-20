---
name: wiki-health
description: "检查 wiki 结构完整性，验证空文件、index 同步和 log 覆盖情况。场景：每次会话开始时、ingest 后、edit 前需要确认 wiki 健康状态时"
---

# Wiki Health

结构检查 skill，调用 `scripts/health.py` 执行快速完整性检查。

## 调用

```bash
python scripts/health.py              # 输出报告到 stdout
python scripts/health.py --save        # 同时保存到 wiki/health-report.md
python scripts/health.py --json        # 机器可读 JSON 输出
```

## 检查项

1. **空/残缺文件** — 页面内容少于 100 字符（frontmatter 除外）
2. **Index 同步** — `wiki/index.md` 中的条目 vs 实际文件
3. **Log 覆盖** — source 页面是否在 `wiki/log.md` 有 ingest 记录

## 输出

- 报告格式的 Markdown 或 JSON
- 可选保存到 `wiki/health-report.md`