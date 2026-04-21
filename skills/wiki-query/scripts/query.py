#!/usr/bin/env python3
"""
Query the LLM Wiki.

Usage:
    python tools/query.py "What are the main themes across all sources?"
    python tools/query.py "How does ConceptA relate to ConceptB?" --save
    python tools/query.py "Summarize everything about EntityName" --save synthesis/my-analysis.md

Flags:
    --save              Save the answer back into the wiki (prompts for filename)
    --save <path>       Save to a specific wiki path
"""

import sys
import re
import json
import argparse
from pathlib import Path
from datetime import date

import os

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"
SCHEMA_FILE = REPO_ROOT / "CLAUDE.md"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  saved: {path.relative_to(REPO_ROOT)}")


def find_relevant_pages(question: str, index_content: str) -> list[Path]:
    """Extract linked pages from index that seem relevant to the question.
    Uses character-level matching for CJK compatibility."""
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', index_content)
    question_lower = question.lower()
    relevant = []

    for title, href in md_links:
        title_lower = title.lower()
        # For CJK: check if any 2+ char substring of the title appears in question
        has_cjk = any('\u4e00' <= ch <= '\u9fff' for ch in title)
        if has_cjk:
            # Sliding window: check if any 2-char CJK bigram from title exists in question
            matched = any(
                title_lower[j:j+2] in question_lower
                for j in range(len(title_lower) - 1)
                if any('\u4e00' <= c <= '\u9fff' for c in title_lower[j:j+2])
            )
        else:
            # Latin: original word-based match (lowered threshold to >2)
            matched = any(word in question_lower for word in title_lower.split() if len(word) > 2)

        if matched:
            p = WIKI_DIR / href
            if p.exists() and p not in relevant:
                relevant.append(p)

    # Also try graph-based expansion: find neighbors of matched pages
    graph_json = REPO_ROOT / "graph" / "graph.json"
    if graph_json.exists() and relevant:
        try:
            graph_data = json.loads(graph_json.read_text())
            page_ids = {p.relative_to(WIKI_DIR).as_posix().replace('.md', '') for p in relevant}
            neighbors = set()
            for edge in graph_data.get('edges', []):
                if edge.get('confidence', 0) >= 0.7:
                    if edge['from'] in page_ids:
                        neighbors.add(edge['to'])
                    elif edge['to'] in page_ids:
                        neighbors.add(edge['from'])
            for nid in neighbors:
                np = WIKI_DIR / f"{nid}.md"
                if np.exists() and np not in relevant:
                    relevant.append(np)
        except (json.JSONDecodeError, KeyError):
            pass

    # Always include overview
    overview = WIKI_DIR / "overview.md"
    if overview.exists() and overview not in relevant:
        relevant.insert(0, overview)
    return relevant[:15]  # cap to avoid context overflow


def append_log(entry: str):
    existing = read_file(LOG_FILE)
    LOG_FILE.write_text(entry.strip() + "\n\n" + existing, encoding="utf-8")


def query(question: str) -> list[dict]:
    """Find relevant pages for a question. Returns list of dicts with path info.

    Claude should read these pages and synthesize the answer.
    """
    today = date.today().isoformat()

    # Step 1: Read index
    index_content = read_file(INDEX_FILE)
    if not index_content:
        print("Wiki is empty. Ingest some sources first with: python scripts/ingest.py <source>")
        return []

    # Step 2: Find relevant pages
    relevant_pages = find_relevant_pages(question, index_content)

    if not relevant_pages:
        print("  No relevant pages found.")
        return []

    # Print found pages for Claude
    print(f"  Found {len(relevant_pages)} relevant pages:")
    for p in relevant_pages:
        print(f"    - {p.relative_to(REPO_ROOT)}")

    return [{"path": str(p), "relative": str(p.relative_to(REPO_ROOT))} for p in relevant_pages]


def save_synthesis(save_path: str, content: str, question: str) -> None:
    """Save a synthesis page. Called by Claude after synthesizing the answer."""
    today = date.today().isoformat()
    full_save_path = WIKI_DIR / save_path
    frontmatter = f"""---
title: "{question[:80]}"
type: synthesis
tags: []
sources: []
last_updated: {today}
---

"""
    write_file(full_save_path, frontmatter + content)

    # Update index
    index_content = read_file(INDEX_FILE)
    entry = f"- [{question[:60]}]({save_path}) — synthesis"
    if "## Syntheses" in index_content:
        index_content = index_content.replace("## Syntheses\n", f"## Syntheses\n{entry}\n")
        INDEX_FILE.write_text(index_content, encoding="utf-8")
    print(f"  indexed: {save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the LLM Wiki")
    parser.add_argument("question", help="Question to ask the wiki")
    parser.add_argument("--save", nargs="?", const="", default=None,
                        help="Save answer to wiki (optionally specify path)")
    args = parser.parse_args()
    pages = query(args.question)
    if pages:
        print("\nClaude should read these pages and synthesize the answer.")
