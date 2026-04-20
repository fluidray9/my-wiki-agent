---
name: wiki-heal
description: "自动发现并修复缺失的 entity 页面，调用 LLM 根据现有上下文生成定义。场景：lint 检查发现缺失 entity、需要自动生成 entity 页面时"
---

# Wiki Heal

图自愈 skill，调用 `tools/heal.py`。

## 调用

```bash
python tools/heal.py
```

## 工作流程

1. 调用 `tools/lint.py` 的 `find_missing_entities()` 获取缺失 entity 列表
2. 对每个缺失 entity：
   - 搜索所有引用该 entity 的页面
   - 提取上下文片段
   - 调用 LLM 生成 entity 定义页面
3. 保存到 `wiki/entities/<EntityName>.md`

## 输出

- 新生成的 entity 页面
- 控制台日志显示进度

## 依赖

- 需要 litellm 调用 LLM
- 需要 wiki 有一定的页面积累