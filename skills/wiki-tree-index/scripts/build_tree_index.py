#!/usr/bin/env python3
"""
Build tree index from raw documents.

Usage:
    python scripts/build_tree_index.py              # Generate tree index
    python scripts/build_tree_index.py --dry-run     # Show parsed structure only
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import date


REPO_ROOT = Path(__file__).parent.parent.parent.parent
RAW_DIR = REPO_ROOT / "raw"
TREE_INDEX_DIR = REPO_ROOT / "tree-index"
TREE_INDEX_FILE = TREE_INDEX_DIR / "tree-index.md"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_document_structure(file_path: Path) -> dict:
    """Parse a document, extract headers and paragraphs with positions.

    Returns:
        {
            "file": "raw/xxx.md",
            "title": "Document Title",
            "headers": [(level, title, char_start, char_end), ...],
            "paragraphs": [(char_start, char_end, text), ...]
        }
    """
    content = read_file(file_path)
    if not content:
        return None

    result = {
        "file": str(file_path.relative_to(REPO_ROOT)),
        "title": file_path.stem,
        "headers": [],
        "paragraphs": []
    }

    # Extract title from first H1 or filename
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        result["title"] = title_match.group(1).strip()

    # Extract headers (H1-H6) with positions
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    for match in header_pattern.finditer(content):
        level = len(match.group(1))
        title = match.group(2).strip()
        char_start = match.start()
        char_end = match.end()
        result["headers"].append((level, title, char_start, char_end))

    # Extract paragraphs (non-empty lines that are not headers or code blocks)
    # But INCLUDE list items (- **item**) as they contain important content
    in_code_block = False
    lines = content.split('\n')
    current_para = []
    para_start = 0
    para_start_line = 0

    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        stripped = line.strip()
        # Include lines that are not headers or code blocks (even if they start with -)
        if stripped and not stripped.startswith('#') and not stripped.startswith('```'):
            if not current_para:
                # Find char position of this line
                para_start = content.find(line)
                para_start_line = i
            current_para.append(stripped)
        else:
            if current_para:
                text = ' '.join(current_para)
                char_end = para_start + len(text)
                result["paragraphs"].append((para_start, char_end, text))
                current_para = []
    if current_para:
        text = ' '.join(current_para)
        char_end = para_start + len(text)
        result["paragraphs"].append((para_start, char_end, text))

    return result


def get_all_raw_files() -> list[Path]:
    """Get all .md files from raw directory."""
    if not RAW_DIR.exists():
        print(f"Error: raw/ directory not found at {RAW_DIR}")
        sys.exit(1)
    files = sorted(RAW_DIR.rglob("*.md"))
    if not files:
        print(f"Error: No .md files found in {RAW_DIR}")
        sys.exit(1)
    return files


def build_tree_index():
    """Build tree index from all raw documents."""
    files = get_all_raw_files()
    print(f"Found {len(files)} raw documents")

    docs_structure = []
    for f in files:
        doc = extract_document_structure(f)
        if doc:
            docs_structure.append(doc)
            print(f"  Parsed: {doc['file']} ({len(doc['headers'])} headers, {len(doc['paragraphs'])} paragraphs)")

    if not docs_structure:
        print("No documents to index")
        return

    # Output structure for LLM to generate tree index
    print("\n" + "=" * 60)
    print("Document structures extracted. LLM should generate tree index.")
    print("=" * 60)

    for doc in docs_structure:
        print(f"\n### {doc['title']} ({doc['file']})")
        print(f"Headers: {len(doc['headers'])}")
        print(f"Paragraphs: {len(doc['paragraphs'])}")

        # Show header structure
        print("\nHeaders:")
        for level, title, start, end in doc['headers']:
            indent = "  " * (level - 1)
            print(f"  {indent}[H{level}] {title}")

        # Show first few paragraphs as sample
        print("\nSample paragraphs:")
        for i, (start, end, text) in enumerate(doc['paragraphs'][:3]):
            preview = text[:80] + "..." if len(text) > 80 else text
            print(f"  [{i}] chars {start}-{end}: {preview}")

    print("\n" + "=" * 60)
    print("Run with --dry-run to see this output without generating index.")
    print("LLM should use this structure to generate tree-index/tree-index.md")
    print("=" * 60)


def extract_keywords(text: str) -> list[str]:
    """Extract important keywords from text."""
    import re
    # Remove markdown formatting
    clean = re.sub(r'\*\*|\*|`|#', '', text)
    # Split and filter Chinese characters and words
    words = re.findall(r'[\w一-龥]+', clean)
    # Filter short words and common terms (Chinese stop words)
    stop_words = {'的', '是', '在', '了', '和', '与', '或', '一个', '以及', '该', '这', '那',
                  'to', 'of', 'the', 'and', 'is', 'in', 'a', 'an', 'for', 'with', 'by',
                  'on', 'at', 'from', 'as', 'it', 'this', 'that', 'are', 'was', 'be'}
    keywords = [w for w in words if len(w) >= 2 and w.lower() not in stop_words]
    # Return unique keywords, limit to 10
    seen = set()
    unique = []
    for k in keywords:
        if k not in seen and len(unique) < 10:
            seen.add(k)
            unique.append(k)
    return unique


def generate_semantic_summary(text: str) -> str:
    """Generate a semantic summary of the text content."""
    import re
    # Clean text
    clean = re.sub(r'\*\*|\*|`|#', '', text)
    # Truncate to reasonable length for semantic search
    if len(clean) > 150:
        return clean[:150] + "..."
    return clean


def generate_tree_index_content(docs_structure: list[dict]) -> str:
    """Generate tree index markdown content with keywords and semantic info."""
    today = date.today().isoformat()
    sources = [doc["file"] for doc in docs_structure]

    lines = [
        "---",
        f"title: \"Tree Index\"",
        "type: tree-index",
        f"sources: {sources}",
        f"generated: {today}",
        "---",
        "",
        "# Tree Index",
        ""
    ]

    for doc in docs_structure:
        lines.append(f"## {doc['title']}")
        lines.append(f"Source: `{doc['file']}`")
        lines.append("")

        # Group paragraphs under headers
        current_header_idx = 0
        for para_start, para_end, text in doc["paragraphs"]:
            # Find which header this paragraph belongs to
            while current_header_idx < len(doc["headers"]) - 1:
                if para_start < doc["headers"][current_header_idx + 1][2]:
                    break
                current_header_idx += 1

            if current_header_idx < len(doc["headers"]):
                level, header_title, _, _ = doc["headers"][current_header_idx]
                lines.append(f"### {header_title}")
                lines.append("")

            # Calculate line number from char position
            content_sample = doc.get("_content", "")
            if not content_sample and para_end > 0:
                file_path = REPO_ROOT / doc["file"]
                if file_path.exists():
                    content_sample = read_file(file_path)
                    doc["_content"] = content_sample

            if content_sample:
                line_num = content_sample[:para_start].count('\n') + 1
            else:
                line_num = 1

            # Extract keywords and semantic summary
            keywords = extract_keywords(text)
            semantic = generate_semantic_summary(text)
            text_preview = text[:200] + "..." if len(text) > 200 else text

            # Leaf node format with keywords and semantic info
            lines.append(f"- {{file: \"{doc['file']}\", line: {line_num}, char_start: {para_start}, char_end: {para_end}, keywords: {keywords}, semantic: \"{semantic}\", text: \"{text_preview}\"}}")
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build tree index from raw documents")
    parser.add_argument("--dry-run", action="store_true", help="Show parsed structure without generating index")
    args = parser.parse_args()

    files = get_all_raw_files()
    docs_structure = [extract_document_structure(f) for f in files]
    docs_structure = [d for d in docs_structure if d]

    if args.dry_run:
        build_tree_index()
    else:
        # Generate tree index directly (no LLM needed)
        TREE_INDEX_DIR.mkdir(exist_ok=True)
        content = generate_tree_index_content(docs_structure)
        TREE_INDEX_FILE.write_text(content, encoding="utf-8")
        print(f"Generated: {TREE_INDEX_FILE}")
        print(f"Sources: {[doc['file'] for doc in docs_structure]}")
