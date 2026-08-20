"""Small shared helpers (frontmatter parsing, hashing)."""
from __future__ import annotations

import hashlib
import json
import re

_FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(md: str) -> tuple[dict, str]:
    """Parse the simple YAML-ish frontmatter written by sync.py."""
    m = _FM_RE.match(md)
    if not m:
        return {}, md
    meta: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            meta[key] = [x.strip().strip('"') for x in inner.split(",") if x.strip()]
        elif val.startswith('"') and val.endswith('"'):
            meta[key] = val[1:-1]
        elif val.lstrip("-").isdigit():
            meta[key] = int(val)
        else:
            meta[key] = val
    return meta, md[m.end():]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
