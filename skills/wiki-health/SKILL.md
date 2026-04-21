---
name: wiki-health
description: "检查 wiki 结构完整性，验证空文件、index 同步和 log 覆盖情况。场景：每次会话开始时、ingest 后、edit 前需要确认 wiki 健康状态时"
---

# Wiki Health

检查 wiki 结构完整性。**Agent 调用脚本执行检查**，纯结构性检查，无 LLM 调用。

## 命令行用法

```bash
python scripts/health.py              # 输出报告到 stdout
python scripts/health.py --save        # 同时保存到 wiki/health-report.md
python scripts/health.py --json        # 机器可读 JSON 输出
```

## 检查项

| 检查项 | 说明 |
|--------|------|
| 空/残缺文件 | 页面内容少于 100 字符（frontmatter 除外） |
| Index 同步 | `wiki/index.md` 条目 vs 实际文件 |
| Log 覆盖 | source 页面是否有 `wiki/log.md` ingest 记录 |

## 脚本输出示例

```markdown
# Wiki Health Report — 2026-04-21

Scanned 9 wiki pages.

## Empty / Stub Files (0 found)
All pages have content beyond frontmatter. ✅

## Index Sync (0 issues)
index.md is in sync with disk. ✅

## Log Coverage (0 source pages without log entry)
All source pages have corresponding log entries. ✅
```

## Agent 职责

- 运行健康检查脚本
- 根据报告决定是否需要修复
- 优先于 lint 运行（结构问题不解决，lint 无意义）