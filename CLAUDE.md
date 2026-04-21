# LLM Wiki Agent — Schema & Workflow Instructions

This wiki is maintained entirely by Claude Code. No API key or Python scripts needed — just open this repo in Claude Code and talk to it.

## Slash Commands (Claude Code)

| Command | What to say |
|---|---|
| `/wiki-ingest` | `ingest raw/my-article.md` |
| `/wiki-query` | `query: what are the main themes?` |
| `/wiki-health` | `health` (fast, every session) |
| `/wiki-lint` | `lint the wiki` (expensive, periodic) |
| `/wiki-graph` | `build the knowledge graph` |

Or just describe what you want in plain English:
- *"Ingest this file: raw/papers/attention-is-all-you-need.md"*
- *"What does the wiki say about transformer models?"*
- *"Check the wiki for orphan pages and contradictions"*
- *"Build the graph and show me what's connected to RAG"*

Claude Code reads this file automatically and follows the workflows below.

---

## Knowledge Base (KB) Concept

Wiki data is organized into **Knowledge Bases**. Each KB is independent:
- Has its own wiki, raw documents, and tree-index
- Has its own metadata (`kb-meta.json`)

```
doc-tree-wiki/
├── knowledge-base/
│   ├── deepseek-kb/           # Knowledge Base A
│   │   ├── kb-meta.json
│   │   ├── wiki/
│   │   ├── tree-index/
│   │   └── raw/
│   └── other-kb/              # Knowledge Base B
│       ├── kb-meta.json
│       └── ...
└── skills/
```

**KB Parameter Rules:**
- **Generation (ingest/build_tree_index)**: `--kb KB_NAME` or infer from path
- **Query (query/query_tree_index)**: `--kb KB_NAME` to specify, or search all KBs if not specified

---

For wiki conventions and detailed workflows, see: `wiki-shared/shared-instructions.md`
