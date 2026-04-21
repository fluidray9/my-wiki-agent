---
name: wiki-file-convert
description: "将 PDF、arXiv 或其他格式文件转换为 Markdown，支持批量目录转换。场景：需要将 PDF、Word、arXiv 等文件转换为 Markdown 以便摄入 wiki 时"
---

# Wiki File Convert

将 PDF、arXiv 等文件转换为 Markdown。**脚本执行转换，Agent 负责转换后的 ingest**。

## 命令行用法

```bash
# arXiv 论文
python scripts/pdf2md.py 2401.12345
python scripts/pdf2md.py https://arxiv.org/abs/2401.12345

# 本地 PDF
python scripts/pdf2md.py paper.pdf
python scripts/pdf2md.py paper.pdf --backend marker    # 复杂布局
python scripts/pdf2md.py paper.pdf --backend pymupdf4llm  # 快速

# 指定输出路径
python scripts/pdf2md.py paper.pdf -o raw/papers/my-paper.md

# 目录批量转换
python scripts/file_to_md.py --input_dir raw/articles/
python scripts/file_to_md.py --input_dir raw/articles/ --delete_source
```

## 支持的后端

| 后端 | 适用场景 | 安装 |
|------|---------|------|
| arxiv2md | arXiv 论文 | `pip install arxiv2markdown` |
| marker | 复杂多栏布局 PDF | `pip install marker-pdf` |
| pymupdf4llm | 快速转换原生文本 PDF | `pip install pymupdf4llm` |
| markitdown | 通用文件（Word/Excel 等） | `pip install markitdown` |

## Agent 职责

- 运行转换脚本生成 .md 文件到 `raw/` 目录
- 使用 `wiki-ingest` 技能将转换后的文件 ingest 到 wiki

## 输出

- `.md` 文件到 `raw/` 目录
- 控制台显示转换结果