#!/usr/bin/env python3
"""
Ingest a source document into the LLM Wiki.

Usage:
    python scripts/ingest.py <path-to-source>
    python scripts/ingest.py raw/articles/my-article.md
    python scripts/ingest.py --validate-only   # run validation on existing wiki

Claude reads the source and generates wiki pages:
  - Creates wiki/sources/<slug>.md
  - Updates wiki/index.md
  - Updates wiki/overview.md (if warranted)
  - Creates/updates entity and concept pages
  - Appends to wiki/log.md
  - Runs post-ingest validation (broken links, index coverage)

The script provides save_source_page(), save_entity_page(), save_concept_page()
for Claude to write the generated content.
"""

import sys
import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
LOG_FILE = WIKI_DIR / "log.md"
INDEX_FILE = WIKI_DIR / "index.md"
OVERVIEW_FILE = WIKI_DIR / "overview.md"
SCHEMA_FILE = REPO_ROOT / "CLAUDE.md"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote: {path.relative_to(REPO_ROOT)}")


def update_index(new_entry: str, section: str = "Sources"):
    content = read_file(INDEX_FILE)
    if not content:
        content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md) — living synthesis\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"
    section_header = f"## {section}"
    if section_header in content:
        content = content.replace(section_header + "\n", section_header + "\n" + new_entry + "\n")
    else:
        content += f"\n{section_header}\n{new_entry}\n"
    write_file(INDEX_FILE, content)


def append_log(entry: str):
    existing = read_file(LOG_FILE)
    write_file(LOG_FILE, entry.strip() + "\n\n" + existing)


def save_source_page(slug: str, content: str) -> None:
    """Write a source page. Content is provided by Claude."""
    write_file(WIKI_DIR / "sources" / f"{slug}.md", content)


def save_entity_page(path: str, content: str) -> None:
    """Write an entity page. Path like 'entities/EntityName.md', content provided by Claude."""
    write_file(WIKI_DIR / path, content)


def save_concept_page(path: str, content: str) -> None:
    """Write a concept page. Path like 'concepts/ConceptName.md', content provided by Claude."""
    write_file(WIKI_DIR / path, content)


def extract_wikilinks(content: str) -> list[str]:
    """Extract all [[WikiLink]] targets from page content."""
    return re.findall(r'\[\[([^\]]+)\]\]', content)


def all_wiki_pages() -> set[str]:
    """Return set of all wiki page stems (case-insensitive)."""
    pages = set()
    for p in WIKI_DIR.rglob("*.md"):
        if p.name not in ("index.md", "log.md", "lint-report.md"):
            pages.add(p.stem.lower())
    return pages


def validate_ingest(changed_pages: list[str] | None = None) -> dict:
    """Validate wiki integrity after an ingest.

    Checks:
      1. Broken wikilinks in changed pages (or all pages if none specified)
      2. Pages not registered in index.md

    Returns dict with 'broken_links' and 'unindexed' lists.
    """
    existing_pages = all_wiki_pages()
    index_content = read_file(INDEX_FILE).lower()

    # Determine which pages to scan for broken links
    if changed_pages:
        scan_paths = [WIKI_DIR / p for p in changed_pages if (WIKI_DIR / p).exists()]
    else:
        scan_paths = [p for p in WIKI_DIR.rglob("*.md")
                      if p.name not in ("index.md", "log.md", "lint-report.md")]

    # Check 1: Broken wikilinks
    broken_links = []
    for page_path in scan_paths:
        content = read_file(page_path)
        rel = str(page_path.relative_to(WIKI_DIR))
        for link in extract_wikilinks(content):
            # Normalize: strip paths, check stem only
            link_stem = Path(link).stem.lower() if '/' in link else link.lower()
            if link_stem not in existing_pages:
                broken_links.append((rel, link))

    # Check 2: Unindexed pages (only check changed pages)
    unindexed = []
    for p in (changed_pages or []):
        page_path = WIKI_DIR / p
        if page_path.exists():
            # Check if the page filename appears in index.md
            stem = page_path.stem.lower()
            if stem not in index_content and p not in ("log.md", "overview.md"):
                unindexed.append(p)

    return {"broken_links": broken_links, "unindexed": unindexed}


def ingest(source_path: str):
    """Ingest a source document. Claude generates the content and calls save_*_page functions."""
    source = Path(source_path)
    if not source.exists():
        print(f"Error: file not found: {source_path}")
        sys.exit(1)

    print(f"\nIngesting: {source.name}")
    print("  Claude will generate the wiki pages from this source.")
    print("  Use save_source_page(), save_entity_page(), save_concept_page() to write pages.")
    print()


if __name__ == "__main__":
    # Handle --validate-only flag
    if len(sys.argv) == 2 and sys.argv[1] == "--validate-only":
        print("Running wiki validation (no ingest)...\n")
        result = validate_ingest()
        if result["broken_links"]:
            print(f"Broken wikilinks: {len(result['broken_links'])}")
            for page, link in result["broken_links"][:20]:
                print(f"  wiki/{page} → [[{link}]]")
            if len(result["broken_links"]) > 20:
                print(f"  ... and {len(result['broken_links']) - 20} more")
        else:
            print("No broken wikilinks found.")
        print()
        pages = all_wiki_pages()
        index_content = read_file(INDEX_FILE).lower()
        unindexed_all = []
        for p in WIKI_DIR.rglob("*.md"):
            if p.name in ("index.md", "log.md", "lint-report.md", "overview.md"):
                continue
            if p.stem.lower() not in index_content:
                unindexed_all.append(str(p.relative_to(WIKI_DIR)))
        if unindexed_all:
            print(f"Pages not in index.md: {len(unindexed_all)}")
            for up in unindexed_all[:20]:
                print(f"  wiki/{up}")
            if len(unindexed_all) > 20:
                print(f"  ... and {len(unindexed_all) - 20} more")
        else:
            print("All pages are indexed.")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest.py <path-to-source> [path2 ...] [dir1 ...]")
        print("       python scripts/ingest.py --validate-only")
        sys.exit(1)
        
    paths_to_process = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.is_file() and p.suffix == ".md":
            paths_to_process.append(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                if f.is_file():
                    paths_to_process.append(f)
        else:
            import glob
            for f in glob.glob(arg, recursive=True):
                g_p = Path(f)
                if g_p.is_file() and g_p.suffix == ".md":
                    paths_to_process.append(g_p)
                    
    # Deduplicate while preserving order
    unique_paths = []
    seen = set()
    for p in paths_to_process:
        abs_p = p.resolve()
        if abs_p not in seen:
            seen.add(abs_p)
            unique_paths.append(p)

    if not unique_paths:
        print("Error: no markdown files found to ingest.")
        sys.exit(1)
        
    if len(unique_paths) > 1:
        print(f"Batch mode: found {len(unique_paths)} files to ingest.")
        
    for p in unique_paths:
        ingest(str(p))
