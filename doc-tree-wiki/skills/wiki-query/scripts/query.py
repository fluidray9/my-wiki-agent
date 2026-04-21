#!/usr/bin/env python3
"""
Query the LLM Wiki.

Usage:
    python tools/query.py "What are the main themes?" --kb my-kb
    python tools/query.py "How does ConceptA relate to ConceptB?" --kb kb1 --kb kb2
    python tools/query.py "Summarize everything about EntityName"
    python tools/query.py "..." --save synthesis/my-analysis.md

Flags:
    --kb KB_NAME       Knowledge base name (can be specified multiple times)
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

REPO_ROOT = Path(__file__).parent.parent.parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"
SCHEMA_FILE = REPO_ROOT / "wiki-shared" / "shared-instructions.md"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  saved: {path.relative_to(REPO_ROOT)}")


def list_knowledge_bases() -> list[dict]:
    """List all knowledge bases."""
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


def find_relevant_pages(question: str, wiki_dir: Path, index_content: str) -> list[Path]:
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
            p = wiki_dir / href
            if p.exists() and p not in relevant:
                relevant.append(p)

    # Also try graph-based expansion: find neighbors of matched pages
    graph_json = wiki_dir.parent / "graph" / "graph.json"
    if graph_json.exists() and relevant:
        try:
            graph_data = json.loads(read_file(graph_json))
            page_ids = {p.relative_to(wiki_dir).as_posix().replace('.md', '') for p in relevant}
            neighbors = set()
            for edge in graph_data.get('edges', []):
                if edge.get('confidence', 0) >= 0.7:
                    if edge['from'] in page_ids:
                        neighbors.add(edge['to'])
                    elif edge['to'] in page_ids:
                        neighbors.add(edge['from'])
            for nid in neighbors:
                np = wiki_dir / f"{nid}.md"
                if np.exists() and np not in relevant:
                    relevant.append(np)
        except (json.JSONDecodeError, KeyError):
            pass

    # Always include overview
    overview = wiki_dir / "overview.md"
    if overview.exists() and overview not in relevant:
        relevant.insert(0, overview)
    return relevant[:15]  # cap to avoid context overflow


def query(question: str, kb_list: list[str] = None) -> list[dict]:
    """Find relevant pages for a question across specified KBs.
    Returns list of dicts with path info and KB name.

    Claude should read these pages and synthesize the answer.
    """
    today = date.today().isoformat()

    # If no KB specified, search all
    if not kb_list:
        all_kbs = list_knowledge_bases()
        kb_list = [kb["name"] for kb in all_kbs]
        print(f"Searching all KBs: {kb_list}")
    else:
        print(f"Searching KBs: {kb_list}")

    all_results = []

    for kb_name in kb_list:
        wiki_dir = KB_DIR / kb_name / "wiki"
        index_file = wiki_dir / "index.md"
        log_file = wiki_dir / "log.md"

        # Step 1: Read index
        index_content = read_file(index_file)
        if not index_content:
            print(f"  KB '{kb_name}': wiki is empty.")
            continue

        # Step 2: Find relevant pages
        relevant_pages = find_relevant_pages(question, wiki_dir, index_content)

        if not relevant_pages:
            print(f"  KB '{kb_name}': no relevant pages found.")
            continue

        # Print found pages for Claude
        print(f"\n{'='*60}")
        print(f"📚 知识库: {kb_name}")
        print(f"{'='*60}")
        print(f"找到 {len(relevant_pages)} 个相关页面:")
        for i, p in enumerate(relevant_pages, 1):
            # Try to read source_file from frontmatter
            content = read_file(p)
            source_file = "N/A"
            match = re.search(r'^source_file:\s*(.+)$', content, re.MULTILINE)
            if match:
                source_file = match.group(1).strip()
            rel_path = p.relative_to(wiki_dir)
            print(f"  {i}. {rel_path}")
            print(f"     来源: {source_file}")

        all_results.append({
            "kb": kb_name,
            "pages": [{"path": str(p), "relative": str(p.relative_to(REPO_ROOT))} for p in relevant_pages]
        })

    if not all_results:
        print("No relevant pages found in any KB. Ingest some sources first.")

    return all_results


def save_synthesis(kb_name: str, save_path: str, content: str, question: str) -> None:
    """Save a synthesis page to specified KB. Called by Claude after synthesizing the answer."""
    wiki_dir = KB_DIR / kb_name / "wiki"
    today = date.today().isoformat()
    full_save_path = wiki_dir / save_path
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
    index_file = wiki_dir / "index.md"
    index_content = read_file(index_file)
    entry = f"- [{question[:60]}]({save_path}) — synthesis"
    if "## Syntheses" in index_content:
        index_content = index_content.replace("## Syntheses\n", f"## Syntheses\n{entry}\n")
        index_file.write_text(index_content, encoding="utf-8")
    print(f"  indexed: {save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the LLM Wiki")
    parser.add_argument("question", help="Question to ask the wiki")
    parser.add_argument("--kb", action="append", help="Knowledge base name (can be specified multiple times)")
    parser.add_argument("--save", nargs="?", const="", default=None,
                        help="Save answer to wiki (optionally specify path)")
    args = parser.parse_args()

    kb_list = args.kb if args.kb else None
    results = query(args.question, kb_list)

    if results:
        print("\nClaude should read these pages and synthesize the answer.")
