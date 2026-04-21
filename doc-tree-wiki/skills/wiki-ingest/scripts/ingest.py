#!/usr/bin/env python3
"""
Ingest a source document into the LLM Wiki.

Usage:
    python scripts/ingest.py <path-to-source> --kb my-kb
    python scripts/ingest.py raw/my-kb/doc.md          # KB inferred from path
    python scripts/ingest.py --validate-only --kb my-kb # Validate specific KB

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
import shutil
import hashlib
import re
import json
import argparse
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).parent.parent.parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"
SCHEMA_FILE = REPO_ROOT / "wiki-shared" / "shared-instructions.md"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote: {path.relative_to(REPO_ROOT)}")


def copy_source_to_raw(source_path: str, kb_name: str) -> list[str]:
    """Copy source files to knowledge-base/{kb}/raw/. Skip if already exists.

    Returns list of copied file paths.
    """
    src = Path(source_path)
    dst_dir = KB_DIR / kb_name / "raw"
    dst_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    paths_to_copy = []

    if src.is_file():
        paths_to_copy = [src]
    elif src.is_dir():
        paths_to_copy = list(src.rglob("*.md"))

    for src_file in paths_to_copy:
        dst_file = dst_dir / src_file.name
        if dst_file.exists():
            print(f"  skip (exists): {dst_file.relative_to(KB_DIR)}")
        else:
            shutil.copy2(src_file, dst_file)
            print(f"  copied: {src_file.name} -> {dst_file.relative_to(KB_DIR)}")
            copied.append(src_file.name)

    return copied


def infer_kb_name(source_path: str) -> str:
    """Infer KB name from source path.

    Example: knowledge-base/deepseek-kb/raw/doc.md -> deepseek-kb
             raw/deepseek-kb/doc.md -> deepseek-kb
    """
    path = Path(source_path)
    parts = path.parts
    if 'knowledge-base' in parts:
        kb_idx = parts.index('knowledge-base')
        if len(parts) > kb_idx + 1:
            return parts[kb_idx + 1]
    if 'raw' in parts:
        raw_idx = parts.index('raw')
        if len(parts) > raw_idx + 1:
            return parts[raw_idx + 1]
    return None


def ensure_kb_dirs(kb_name: str) -> dict:
    """Ensure KB directory structure exists and return paths."""
    kb_path = KB_DIR / kb_name
    dirs = {
        "kb": kb_path,
        "kb_meta": kb_path / "kb-meta.json",
        "wiki": kb_path / "wiki",
        "raw": kb_path / "raw",
        "log": kb_path / "wiki" / "log.md",
        "index": kb_path / "wiki" / "index.md",
        "overview": kb_path / "wiki" / "overview.md",
        "sources": kb_path / "wiki" / "sources",
        "entities": kb_path / "wiki" / "entities",
        "concepts": kb_path / "wiki" / "concepts",
        "syntheses": kb_path / "wiki" / "syntheses",
    }

    # Create directories
    for key in ["wiki", "raw", "sources", "entities", "concepts", "syntheses"]:
        dirs[key].mkdir(parents=True, exist_ok=True)

    # Create kb-meta.json if not exists
    if not dirs["kb_meta"].exists():
        meta = {
            "name": kb_name,
            "description": f"Knowledge base: {kb_name}",
            "created": date.today().isoformat()
        }
        write_file(dirs["kb_meta"], json.dumps(meta, indent=2, ensure_ascii=False))

    # Create index.md if not exists
    if not dirs["index"].exists():
        index_content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md) — living synthesis\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"
        write_file(dirs["index"], index_content)

    return dirs


def get_kb_dirs(kb_name: str) -> dict:
    """Get KB directory paths (assumes KB exists)."""
    kb_path = KB_DIR / kb_name
    return {
        "kb": kb_path,
        "kb_meta": kb_path / "kb-meta.json",
        "wiki": kb_path / "wiki",
        "raw": kb_path / "raw",
        "log": kb_path / "wiki" / "log.md",
        "index": kb_path / "wiki" / "index.md",
        "overview": kb_path / "wiki" / "overview.md",
        "sources": kb_path / "wiki" / "sources",
        "entities": kb_path / "wiki" / "entities",
        "concepts": kb_path / "wiki" / "concepts",
        "syntheses": kb_path / "wiki" / "syntheses",
    }


class IngestContext:
    """Context for a single ingest operation."""
    def __init__(self, kb_name: str):
        self.kb_name = kb_name
        self.dirs = get_kb_dirs(kb_name)

    @property
    def wiki_dir(self):
        return self.dirs["wiki"]

    @property
    def log_file(self):
        return self.dirs["log"]

    @property
    def index_file(self):
        return self.dirs["index"]

    @property
    def overview_file(self):
        return self.dirs["overview"]

    def update_index(self, new_entry: str, section: str = "Sources"):
        content = read_file(self.index_file)
        if not content:
            content = "# Wiki Index\n\n## Overview\n- [Overview](overview.md) — living synthesis\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Syntheses\n"
        section_header = f"## {section}"
        if section_header in content:
            content = content.replace(section_header + "\n", section_header + "\n" + new_entry + "\n")
        else:
            content += f"\n{section_header}\n{new_entry}\n"
        write_file(self.index_file, content)

    def append_log(self, entry: str):
        existing = read_file(self.log_file)
        write_file(self.log_file, entry.strip() + "\n\n" + existing)

    def save_source_page(self, slug: str, content: str):
        write_file(self.dirs["sources"] / f"{slug}.md", content)

    def save_entity_page(self, path: str, content: str):
        """Write an entity page. Path like 'entities/EntityName.md', content provided by Claude."""
        write_file(self.dirs["entities"] / path, content)

    def save_concept_page(self, path: str, content: str):
        """Write a concept page. Path like 'concepts/ConceptName.md', content provided by Claude."""
        write_file(self.dirs["concepts"] / path, content)

    def extract_wikilinks(self, content: str) -> list[str]:
        """Extract all [[WikiLink]] targets from page content."""
        return re.findall(r'\[\[([^\]]+)\]\]', content)

    def all_wiki_pages(self) -> set[str]:
        """Return set of all wiki page stems (case-insensitive)."""
        pages = set()
        for p in self.wiki_dir.rglob("*.md"):
            if p.name not in ("index.md", "log.md", "lint-report.md"):
                pages.add(p.stem.lower())
        return pages

    def validate_ingest(self, changed_pages: list[str] = None) -> dict:
        """Validate wiki integrity after an ingest."""
        existing_pages = self.all_wiki_pages()
        index_content = read_file(self.index_file).lower()

        # Determine which pages to scan for broken links
        if changed_pages:
            scan_paths = [self.wiki_dir / p for p in changed_pages if (self.wiki_dir / p).exists()]
        else:
            scan_paths = [p for p in self.wiki_dir.rglob("*.md")
                          if p.name not in ("index.md", "log.md", "lint-report.md")]

        # Check 1: Broken wikilinks
        broken_links = []
        for page_path in scan_paths:
            content = read_file(page_path)
            rel = str(page_path.relative_to(self.wiki_dir))
            for link in self.extract_wikilinks(content):
                link_stem = Path(link).stem.lower() if '/' in link else link.lower()
                if link_stem not in existing_pages:
                    broken_links.append((rel, link))

        # Check 2: Unindexed pages
        unindexed = []
        for p in (changed_pages or []):
            page_path = self.wiki_dir / p
            if page_path.exists():
                stem = page_path.stem.lower()
                if stem not in index_content and p not in ("log.md", "overview.md"):
                    unindexed.append(p)

        return {"broken_links": broken_links, "unindexed": unindexed}


def ingest(source_path: str, ctx: IngestContext):
    """Ingest a source document. Claude generates the content and calls save_*_page functions."""
    source = Path(source_path)
    if not source.exists():
        print(f"Error: file not found: {source_path}")
        sys.exit(1)

    # Copy source files to KB raw/ directory
    print(f"\nCopying sources to KB raw/...")
    copied = copy_source_to_raw(source_path, ctx.kb_name)
    if copied:
        print(f"  {len(copied)} file(s) copied")

    print(f"\nIngesting: {source.name}")
    print(f"  KB: {ctx.kb_name}")
    print("  Claude will generate the wiki pages from this source.")
    print("  Use save_source_page(), save_entity_page(), save_concept_page() to write pages.")
    print()


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest a source document into the LLM Wiki")
    parser.add_argument("--kb", help="Knowledge base name (e.g., 'deepseek-kb'). If not provided, inferred from path.")
    parser.add_argument("--validate-only", action="store_true", help="Validate wiki integrity only")
    parser.add_argument("paths", nargs="*", help="Path to source file(s) or directory")
    args = parser.parse_args()

    # Determine KB name
    kb_name = args.kb
    if not kb_name:
        # Try to infer from paths
        for p in args.paths:
            inferred = infer_kb_name(p)
            if inferred:
                kb_name = inferred
                break
        if not kb_name:
            print("Error: --kb parameter required if cannot infer from path")
            print("Usage: python ingest.py <source-file> --kb my-kb")
            sys.exit(1)

    # Ensure KB directories exist
    dirs = ensure_kb_dirs(kb_name)
    ctx = IngestContext(kb_name)

    # Handle --validate-only flag
    if args.validate_only:
        print(f"Running wiki validation for KB: {kb_name}...\n")
        result = ctx.validate_ingest()
        if result["broken_links"]:
            print(f"Broken wikilinks: {len(result['broken_links'])}")
            for page, link in result["broken_links"][:20]:
                print(f"  wiki/{page} → [[{link}]]")
            if len(result["broken_links"]) > 20:
                print(f"  ... and {len(result['broken_links']) - 20} more")
        else:
            print("No broken wikilinks found.")
        print()
        pages = ctx.all_wiki_pages()
        index_content = read_file(ctx.index_file).lower()
        unindexed_all = []
        for p in ctx.wiki_dir.rglob("*.md"):
            if p.name in ("index.md", "log.md", "lint-report.md", "overview.md"):
                continue
            if p.stem.lower() not in index_content:
                unindexed_all.append(str(p.relative_to(ctx.wiki_dir)))
        if unindexed_all:
            print(f"Pages not in index.md: {len(unindexed_all)}")
            for up in unindexed_all[:20]:
                print(f"  wiki/{up}")
            if len(unindexed_all) > 20:
                print(f"  ... and {len(unindexed_all) - 20} more")
        else:
            print("All pages are indexed.")
        sys.exit(0)

    if not args.paths:
        print("Usage: python ingest.py <source-file(s)> --kb my-kb")
        sys.exit(1)

    paths_to_process = []
    for arg in args.paths:
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
        ingest(str(p), ctx)
