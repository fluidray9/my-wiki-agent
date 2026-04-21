#!/usr/bin/env python3
"""
Query the tree index to find matching passages from raw documents.

Usage:
    python scripts/query_tree_index.py "query text" --kb my-kb      # Query specific KB
    python scripts/query_tree_index.py "query text" --kb kb1 --kb kb2  # Query multiple KBs
    python scripts/query_tree_index.py "query text"                 # Query all KBs
"""

import argparse
import re
import sys
from pathlib import Path
import json


REPO_ROOT = Path(__file__).parent.parent.parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"
# Support both knowledge-base/ and direct tree-index/ layouts
TREE_INDEX_ROOT = REPO_ROOT / "tree-index"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def list_knowledge_bases() -> list[dict]:
    """List all knowledge bases by scanning knowledge-base/ directory."""
    kb_list = []
    if not KB_DIR.exists():
        return kb_list
    for kb_path in KB_DIR.iterdir():
        if kb_path.is_dir():
            kb_meta_file = kb_path / "kb-meta.json"
            kb_name = kb_path.name
            if kb_meta_file.exists():
                try:
                    meta = json.loads(read_file(kb_meta_file))
                    kb_list.append({
                        "name": kb_name,
                        "description": meta.get("description", ""),
                        "path": kb_path
                    })
                except:
                    kb_list.append({
                        "name": kb_name,
                        "description": "",
                        "path": kb_path
                    })
            else:
                kb_list.append({
                    "name": kb_name,
                    "description": "",
                    "path": kb_path
                })
    return kb_list


def parse_tree_index(kb_name: str) -> list[dict]:
    """Parse tree-index/final-tree-index.md for a specific KB.

    Returns:
        [{"file": "knowledge-base/xxx/raw/xxx.md", "line": 10, "char_start": 150, "char_end": 500,
          "keywords": [...], "semantic": "...", "text": "...", "section": "章节名", "kb": "kb_name"}, ...]
    """
    tree_index_file = KB_DIR / kb_name / "tree-index" / "final-tree-index.md"
    if not tree_index_file.exists():
        # Try intermediate tree-index.md if final doesn't exist
        tree_index_file = KB_DIR / kb_name / "tree-index" / "tree-index.md"
    # Also support direct tree-index/ layout
    if not tree_index_file.exists():
        tree_index_file = TREE_INDEX_ROOT / "tree-index.md"

    if not tree_index_file.exists():
        print(f"Warning: Tree index not found for KB: {kb_name} at {tree_index_file}")
        return []

    content = read_file(tree_index_file)
    leaf_nodes = []

    # Track current section
    current_section = ""

    # Parse headers to track sections
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    for match in header_pattern.finditer(content):
        level = len(match.group(1))
        title = match.group(2).strip()
        if level == 3:  # H3 is section level (###)
            current_section = title

    # Parse leaf nodes: lines starting with "- {"
    # Format: - {file: "...", line: 3, char_start: 20, char_end: 127, keywords: [...], semantic: "...", text: "..."}
    leaf_pattern = re.compile(
        r'-\s*\{file:\s*"([^"]+)"\s*,\s*line:\s*(\d+)\s*,\s*char_start:\s*(\d+)\s*,\s*char_end:\s*(\d+)\s*,\s*keywords:\s*(\[[^\]]*\])\s*,\s*semantic:\s*"([^"]*)"\s*,\s*text:\s*"([^"]+)"\}'
    )
    for match in leaf_pattern.finditer(content):
        file_path = match.group(1)
        line_num = int(match.group(2))
        char_start = int(match.group(3))
        char_end = int(match.group(4))
        keywords_str = match.group(5)
        semantic = match.group(6)
        text = match.group(7)

        # Parse keywords list
        import ast
        try:
            keywords = ast.literal_eval(keywords_str)
        except:
            keywords = []

        leaf_nodes.append({
            "file": file_path,
            "line": line_num,
            "char_start": char_start,
            "char_end": char_end,
            "keywords": keywords,
            "semantic": semantic,
            "text": text,
            "section": current_section,
            "kb": kb_name
        })

    return leaf_nodes


def find_matching_leaves(query: str, kb_list: list[str], max_results: int = 10) -> list[dict]:
    """Find leaf nodes matching the query across specified KBs.

    Args:
        query: Search query string
        kb_list: List of KB names to search
        max_results: Maximum number of results to return

    Returns:
        List of matching leaf nodes with file, position, text, keywords, semantic, kb
    """
    all_nodes = []
    for kb_name in kb_list:
        nodes = parse_tree_index(kb_name)
        all_nodes.extend(nodes)

    if not all_nodes:
        return []

    query_lower = query.lower()

    # Score each leaf by relevance (keyword + semantic matching)
    scored = []
    for node in all_nodes:
        text_lower = node["text"].lower()
        semantic_lower = node["semantic"].lower()
        keywords_lower = [k.lower() for k in node.get("keywords", [])]

        query_words = query_lower.split()

        # Keyword match score
        keyword_score = sum(1 for word in query_words if any(word in kw for kw in keywords_lower))

        # Semantic match score
        semantic_score = sum(1 for word in query_words if word in semantic_lower)

        # Text match score
        text_score = sum(1 for word in query_words if word in text_lower)

        total_score = keyword_score * 3 + semantic_score * 2 + text_score * 1

        if total_score > 0:
            scored.append((total_score, node))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Return top results
    return [node for _, node in scored[:max_results]]


def retrieve_text(file_path: str, char_start: int, char_end: int) -> str:
    """Retrieve text from a raw document at the specified position.

    Args:
        file_path: Path to the raw file (relative to REPO_ROOT)
        char_start: Starting character position
        char_end: Ending character position

    Returns:
        The text content at the specified position
    """
    full_path = REPO_ROOT / file_path
    if not full_path.exists():
        return f"[File not found: {file_path}]"

    content = read_file(full_path)
    if char_start < 0 or char_end > len(content):
        return f"[Invalid position: {char_start}-{char_end}]"

    return content[char_start:char_end]


def get_tree_index_content(kb_name: str) -> str:
    """Get raw tree-index content for LLM to analyze."""
    tree_index_file = KB_DIR / kb_name / "tree-index" / "tree-index.md"
    if not tree_index_file.exists():
        return f"[Tree index not found for KB: {kb_name}]"
    return read_file(tree_index_file)


def format_script_results(matches: list[dict]) -> str:
    """Format script matching results for LLM synthesis."""
    if not matches:
        return "（无）"

    lines = []
    for i, m in enumerate(matches, 1):
        lines.append(f"结果 {i}")
        lines.append(f"📚 知识库: {m['kb']}")
        lines.append(f"📄 参考文档: {m['file']}")
        lines.append(f"📍 位置: 第 {m['line']} 行")
        lines.append(f"📑 章节: {m['section']}")
        lines.append(f"📝 原文: {m['text'][:100]}...")
        lines.append("")
    return "\n".join(lines)


def query(query_text: str, kb_list: list[str] = None, max_results: int = 10) -> list[dict]:
    """Query the tree index and return matching results.

    Args:
        query_text: Query string
        kb_list: List of KB names to search. None means all KBs.
        max_results: Maximum number of results

    Returns:
        [{"kb": "...", "section": "...", "file": "...", "text": "...", "retrieved_text": "..."}, ...]
    """
    # If no KB specified, search all
    if not kb_list:
        all_kbs = list_knowledge_bases()
        kb_list = [kb["name"] for kb in all_kbs]
        print(f"Searching all KBs: {kb_list}")
    else:
        print(f"Searching KBs: {kb_list}")

    print(f"Querying tree index for: {query_text}")

    matches = find_matching_leaves(query_text, kb_list, max_results)
    print(f"Found {len(matches)} matching passages")

    results = []
    for i, match in enumerate(matches, 1):
        # Retrieve actual text from raw file
        actual_text = retrieve_text(match["file"], match["char_start"], match["char_end"])

        print(f"\n{'='*60}")
        print(f"结果 {i}")
        print(f"{'='*60}")
        print(f"📚 知识库: {match['kb']}")
        print(f"📄 参考文档: {match['file']}")
        print(f"📍 位置: 第 {match['line']} 行")
        print(f"📑 章节: {match['section']}")
        print(f"{'-'*60}")
        print(f"内容:\n{actual_text}")
        print(f"{'='*60}")
        print()

        results.append({
            "kb": match["kb"],
            "section": match["section"],
            "file": match["file"],
            "line": match["line"],
            "index_text": match["text"],
            "retrieved_text": actual_text
        })

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the tree index")
    parser.add_argument("query", help="Query text to search for")
    parser.add_argument("--kb", action="append", help="Knowledge base name (can be specified multiple times). If not provided, searches all KBs.")
    parser.add_argument("--max-results", type=int, default=5, help="每个KB最多返回结果数")
    args = parser.parse_args()

    kb_list = args.kb if args.kb else None
    results = query(args.query, kb_list, args.max_results)

    if not results:
        print("\nNo results found. Try a different query or rebuild the index.")
