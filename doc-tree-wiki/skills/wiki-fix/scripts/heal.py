#!/usr/bin/env python3
"""
Graph Self-Healing Tool

Automatically retrieves "Missing Entity Pages" from the wiki and generates
comprehensive definition pages for them using the LLM.
It resolves broken entity links by scanning existing contexts where the entity is referenced.

Usage:
    python scripts/heal.py
"""

import sys
import re
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).parent.parent.parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
ENTITIES_DIR = WIKI_DIR / "entities"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote: {path.relative_to(REPO_ROOT)}")


def extract_wikilinks(content: str) -> list[str]:
    return re.findall(r'\[\[([^\]]+)\]\]', content)


def all_wiki_pages() -> list[Path]:
    return [p for p in WIKI_DIR.rglob("*.md")
            if p.name not in ("index.md", "log.md", "lint-report.md", "health-report.md")]


def find_missing_entities(pages: list[Path]) -> list[str]:
    """Find entity-like names mentioned in 3+ pages but lacking their own page."""
    mention_counts: dict[str, int] = defaultdict(int)
    existing_pages = {p.stem.lower() for p in pages}
    for p in pages:
        content = read_file(p)
        links = extract_wikilinks(content)
        for link in links:
            if link.lower() not in existing_pages:
                mention_counts[link] += 1
    return [name for name, count in mention_counts.items() if count >= 3]


def search_sources(entity: str, pages: list[Path]) -> list[dict]:
    """Find pages where this entity is mentioned, return context snippets."""
    results = []
    for p in pages:
        if "entities" not in str(p.parent) and "concepts" not in str(p.parent):
            content = read_file(p)
            if entity.lower() in content.lower():
                # Find the line containing the entity
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if entity.lower() in line.lower():
                        results.append({
                            "page": str(p.relative_to(REPO_ROOT)),
                            "context": line.strip(),
                            "line": i + 1
                        })
                        break
    return results[:15]


def save_entity_page(name: str, content: str) -> None:
    """Write an entity page. Content is provided by Claude."""
    write_file(ENTITIES_DIR / f"{name}.md", content)


def heal() -> list[dict]:
    """Find missing entities and their contexts. Claude generates the content."""
    pages = all_wiki_pages()
    missing_entities = find_missing_entities(pages)

    if not missing_entities:
        print("Graph is fully connected. No missing entities found!")
        return []

    ENTITIES_DIR.mkdir(exist_ok=True, parents=True)
    print(f"Found {len(missing_entities)} missing entity nodes.")

    result = []
    for entity in missing_entities:
        contexts = search_sources(entity, pages)
        result.append({
            "name": entity,
            "contexts": contexts
        })
        print(f"  - {entity}: {len(contexts)} references found")

    print("\nClaude should generate entity pages using save_entity_page().")
    return result


if __name__ == "__main__":
    heal()