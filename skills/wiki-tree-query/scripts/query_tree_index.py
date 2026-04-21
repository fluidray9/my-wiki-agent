#!/usr/bin/env python3
"""
Query the tree index to find matching passages from raw documents.

Usage:
    python scripts/query_tree_index.py "query text"
"""

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent.parent
RAW_DIR = REPO_ROOT / "raw"
TREE_INDEX_FILE = REPO_ROOT / "tree-index" / "final-tree-index.md"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_tree_index() -> list[dict]:
    """Parse tree-index/tree-index.md and extract leaf nodes.

    Returns:
        [{"file": "raw/xxx.md", "line": 10, "char_start": 150, "char_end": 500,
          "keywords": [...], "semantic": "...", "text": "...", "section": "章节名"}, ...]
    """
    if not TREE_INDEX_FILE.exists():
        print(f"Error: Tree index not found at {TREE_INDEX_FILE}")
        print("Run wiki-tree-index first to generate the index.")
        sys.exit(1)

    content = read_file(TREE_INDEX_FILE)
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
    # New format: - {file: "...", line: 3, char_start: 20, char_end: 127, keywords: [...], semantic: "...", text: "..."}
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
            "section": current_section
        })

    return leaf_nodes


def find_matching_leaves(query: str, max_results: int = 10) -> list[dict]:
    """Find leaf nodes matching the query (keyword + semantic search).

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of matching leaf nodes with file, position, text, keywords, semantic
    """
    leaf_nodes = parse_tree_index()
    query_lower = query.lower()

    # Score each leaf by relevance (keyword + semantic matching)
    scored = []
    for node in leaf_nodes:
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


def semantic_search(query: str, max_results: int = 10) -> list[dict]:
    """Semantic search - search based on meaning, not just keywords.

    This function relies on Agent to do the semantic understanding.
    Script provides: keywords matching, semantic field matching.

    Args:
        query: Natural language query (e.g., "deepseek-v3什么时候出来的")
        max_results: Maximum number of results

    Returns:
        List of matching leaf nodes with relevance scores
    """
    # Use find_matching_leaves which now considers keywords and semantic
    return find_matching_leaves(query, max_results)


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


def query(query_text: str, max_results: int = 10) -> list[dict]:
    """Query the tree index and return matching results.

    Returns:
        [{"section": "...", "file": "...", "text": "...", "retrieved_text": "..."}, ...]
    """
    print(f"Querying tree index for: {query_text}")

    matches = find_matching_leaves(query_text, max_results)
    print(f"Found {len(matches)} matching passages")

    results = []
    for i, match in enumerate(matches, 1):
        print(f"\n--- Result {i} ---")
        print(f"Section: {match['section']}")
        print(f"File: {match['file']} (line {match['line']})")
        print(f"Index text: {match['text'][:100]}...")

        # Retrieve actual text from raw file
        actual_text = retrieve_text(match["file"], match["char_start"], match["char_end"])
        print(f"Retrieved: {actual_text[:200]}...")

        results.append({
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
    parser.add_argument("--max-results", type=int, default=10, help="Maximum number of results")
    args = parser.parse_args()

    results = query(args.query, args.max_results)

    if not results:
        print("\nNo results found. Try a different query or rebuild the index.")
