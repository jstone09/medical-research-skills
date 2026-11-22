#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

REQUIRED_KEYS = {"name", "description", "license", "author"}
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    data = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def validate_skill_md(path: Path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    meta = parse_frontmatter(txt)
    missing = sorted(REQUIRED_KEYS - set(meta))
    return {"path": str(path), "ok": not missing, "missing": missing, "meta": meta}


def main():
    root = Path.cwd()
    files = list(root.rglob("SKILL.md"))
    results = [validate_skill_md(p) for p in files]
    failed = [r for r in results if not r["ok"]]
    print(json.dumps({"checked": len(files), "failed": len(failed), "failures": failed}, indent=2))
    if failed:
        print("SKILL.md validation failed: missing required frontmatter keys", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
