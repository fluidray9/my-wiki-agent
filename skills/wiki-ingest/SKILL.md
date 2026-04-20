---
name: wiki-ingest
description: "摄入源文档到 wiki，生成 source/entity/concept 页面并更新 index。场景：需要将 Markdown、PDF、arXiv 等文档转换为 wiki 页面时"
---

# Wiki Ingest

摄入源文档 skill，调用 `scripts/ingest.py`。

## 调用

```bash
# 单个文件
python scripts/ingest.py raw/papers/my-paper.md

# 批量目录
python scripts/ingest.py raw/papers/

# 验证模式（不摄入，只检查）
python scripts/ingest.py --validate-only
```

## 工作流程

1. 读取源文档内容
2. 构建当前 wiki 上下文（index + overview + 最近 5 个 source）
3. 调用 LLM 生成：
   - `wiki/sources/<slug>.md` — source 页面
   - `wiki/entities/<Name>.md` — entity 页面（人物/公司/项目）
   - `wiki/concepts/<Name>.md` — concept 页面（概念/框架）
   - 更新 `wiki/overview.md`
   - 标记矛盾
4. 更新 `wiki/index.md`
5. 记录到 `wiki/log.md`
6. 验证：检查断链、index 覆盖

## 输出

- 创建的页面列表
- 矛盾警告（如有）
- 验证结果