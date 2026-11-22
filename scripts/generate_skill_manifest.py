#!/usr/bin/env python3
import json
from pathlib import Path
import re

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta


def main():
    root = Path.cwd()
    out_path = Path("dist/skill-manifest.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    for md in root.rglob("SKILL.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        meta = parse_frontmatter(text)
        # infer category from path segments
        parts = md.parts
        category = None
        for cat in ("Academic Writing", "Data Analysis", "Evidence Insight", "Protocol Design", "Other"):
            if cat in parts:
                category = cat
                break
        entries.append(
            {
                "name": meta.get("name") or md.parent.name,
                "description": meta.get("description", ""),
                "path": str(md.parent.relative_to(root)),
                "category": category,
                "root": parts[1] if len(parts) > 1 else None,
            }
        )

    entries.sort(key=lambda e: (e.get("root") or "", e.get("category") or "", e["name"]))

    with out_path.open("w", encoding="utf-8") as f:
        json.dump({"count": len(entries), "skills": entries}, f, indent=2)
    print(f"Wrote {out_path} with {len(entries)} skills")


if __name__ == "__main__":
    main()
