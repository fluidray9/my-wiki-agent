---
name: wiki-health
description: "结构检查：验证 wiki 的完整性（空文件、index同步、log覆盖）。零 LLM 调用，可每次会话运行。"
---

# Wiki Health

结构检查 skill，调用 `tools/health.py` 执行快速完整性检查。

## 调用

```bash
python tools/health.py              # 输出报告到 stdout
python tools/health.py --save        # 同时保存到 wiki/health-report.md
python tools/health.py --json        # 机器可读 JSON 输出
```

## 检查项

1. **空/残缺文件** — 页面内容少于 100 字符（frontmatter 除外）
2. **Index 同步** — `wiki/index.md` 中的条目 vs 实际文件
3. **Log 覆盖** — source 页面是否在 `wiki/log.md` 有 ingest 记录

## 使用场景

- 每次会话开始时运行
- ingest 后验证结构
- edit 前确认 wiki 健康

## 输出

- 报告格式的 Markdown 或 JSON
- 可选保存到 `wiki/health-report.md`