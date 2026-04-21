---
name: wiki-refresh
description: "检测 wiki source 页面是否落后于原始文档，通过哈希对比刷新过时内容。场景：源文档被修改后、需要同步更新 wiki source 页面时"
---

# Wiki Refresh

检测并刷新过时的 wiki source 页面。**Agent 调用脚本检查，脚本对比哈希判断是否需要刷新**。

## KB 参数规则

- `--kb KB_NAME`：指定知识库
- **不指定 `--kb`**：检查所有知识库

## 命令行用法

```bash
# 刷新指定 KB
python scripts/refresh.py --kb deepseek-kb                     # 只刷新变化的 source
python scripts/refresh.py --kb deepseek-kb --force             # 强制刷新所有 source
python scripts/refresh.py --kb deepseek-kb --page sources/X    # 刷新指定页面
python scripts/refresh.py --kb deepseek-kb --dry-run            # 只列出需要刷新的页面

# 刷新所有 KB
python scripts/refresh.py
```

## 工作流程

1. **脚本** 读取 `wiki/sources/*.md` 的 frontmatter 中的 `source_file` 字段
2. **脚本** 计算 raw 文档的 SHA256 哈希
3. **脚本** 与缓存哈希对比（`graph/.refresh_cache.json`）
4. **Agent** 对比不一致的文档重新 ingest

## Agent 职责

- 运行 refresh 脚本查看哪些 source 需要刷新
- 读取原始文档和现有 wiki source 页面
- 更新 wiki source 页面内容
- 写入更新后的文件

## 输出

- 控制台显示刷新进度
- 刷新后更新缓存