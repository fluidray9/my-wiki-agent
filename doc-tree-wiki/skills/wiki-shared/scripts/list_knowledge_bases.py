#!/usr/bin/env python3
"""
List all knowledge bases.

Usage:
    python skills/wiki-shared/scripts/list_knowledge_bases.py
"""

import json
import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent.parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def list_knowledge_bases() -> list[dict]:
    """List all knowledge bases by scanning knowledge-base/ directory.

    Returns:
        [{"name": "deepseek-kb", "description": "...", "path": Path}, ...]
    """
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
                        "path": str(kb_path)
                    })
                except json.JSONDecodeError:
                    kb_list.append({
                        "name": kb_name,
                        "description": "",
                        "path": str(kb_path)
                    })
            else:
                kb_list.append({
                    "name": kb_name,
                    "description": "",
                    "path": str(kb_path)
                })
    return kb_list


def main():
    parser = argparse.ArgumentParser(description="List all knowledge bases")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    kbs = list_knowledge_bases()
    if not kbs:
        print("No knowledge bases found.")
        return

    if args.json:
        print(json.dumps(kbs, indent=2, ensure_ascii=False))
    else:
        print(f"Found {len(kbs)} knowledge base(s):\n")
        for kb in kbs:
            print(f"  - {kb['name']}")
            if kb['description']:
                print(f"    {kb['description']}")


if __name__ == "__main__":
    main()
