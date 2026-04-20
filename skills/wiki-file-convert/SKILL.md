---
name: wiki-file-convert
description: "将 PDF、arXiv 或其他格式文件转换为 Markdown，支持批量目录转换。场景：需要将 PDF、Word、arXiv 等文件转换为 Markdown 以便摄入 wiki 时"
---

# Wiki File Convert

文件转换 skill，调用 `scripts/pdf2md.py` 或 `scripts/file_to_md.py`。

## 调用

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

# 目录批量转换（使用 file_to_md.py）
python scripts/file_to_md.py --input_dir raw/articles/
python scripts/file_to_md.py --input_dir raw/articles/ --delete_source  # 转换后删除原文件
```

## 支持的后端

| 后端 | 适用场景 | 安装 |
|------|---------|------|
| arxiv2md | arXiv 论文（使用结构化源，非 PDF） | `pip install arxiv2markdown` |
| marker | 复杂多栏布局的 PDF | `pip install marker-pdf` |
| pymupdf4llm | 快速转换原生文本 PDF | `pip install pymupdf4llm` |
| markitdown | 通用文件（Word/Excel 等） | `pip install markitdown` |

## 输出

- `.md` 文件到 `raw/` 目录
- 控制台显示转换结果