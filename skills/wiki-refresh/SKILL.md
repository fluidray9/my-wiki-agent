---
name: wiki-refresh
description: "刷新过时页面：检测 source 页面是否落后于原始文档"
---

# Wiki Refresh

刷新过时页面 skill，调用 `tools/refresh.py`。

## 调用

```bash
python tools/refresh.py                     # 只刷新变化的 source
python tools/refresh.py --force             # 强制刷新所有 source
python tools/refresh.py --page sources/X    # 刷新指定页面
python tools/refresh.py --dry-run            # 只列出需要刷新的页面
```

## 工作流程

1. 读取 `wiki/sources/*.md` 的 frontmatter 中的 `source_file` 字段
2. 计算 raw 文档的 SHA256 哈希
3. 与缓存的哈希对比（缓存在 `graph/.refresh_cache.json`）
4. 对比不一致的文档重新调用 ingest

## 输出

- 控制台显示刷新进度
- 刷新后更新缓存

## 使用场景

- raw/ 中的原始文档被修改
- 需要同步更新 wiki