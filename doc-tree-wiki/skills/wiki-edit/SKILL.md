---
name: wiki-edit
description: "修改 wiki 页面内容，验证 wikilinks 有效性，同步更新 index 和 log。场景：需要编辑、更新、删除或重命名 wiki 页面时"
---

# Wiki Edit

修改 wiki 页面 skill，无独立 Python 脚本，直接由 Agent 执行。

## KB 参数规则

- `--kb KB_NAME`：指定知识库
- **不指定 `--kb`**：从文件路径推断 KB 名

## 工作流程

1. **定位页面** — 找到要修改的 wiki 页面路径（`knowledge-base/{kb}/wiki/`）
2. **读取内容** — 读取当前页面内容和 frontmatter
3. **编辑** — 根据用户需求修改内容
   - 保持 frontmatter 完整
   - 使用 `[[wikilinks]]` 链接相关页面
   - 遵循页面模板格式
4. **验证** — 调用 `wiki-health` 检查：
   - 所有 `[[wikilinks]]` 有效
   - 页面未变成空/残缺
5. **同步 index** — 如页面标题/位置变化，更新 `knowledge-base/{kb}/wiki/index.md`
6. **记录 log** — 添加 `## [YYYY-MM-DD] edit | <title>` 到 `knowledge-base/{kb}/wiki/log.md`
7. **更新图谱** — 调用 `wiki-graph` 重新构建图谱（如有重大变化）

## 编辑类型

- 更新现有页面内容
- 重命名页面（同步更新所有引用）
- 合并两个页面
- 删除页面（从 index 移除）

## 输出

- 修改后的页面内容
- index/log 更新确认