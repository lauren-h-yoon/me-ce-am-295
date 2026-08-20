#!/usr/bin/env python3
"""
Generate CLAUDE.md "native memory" files under content/ so the Claude Agent SDK
loads course context automatically (setting_sources=["project"]).

Writes:
  content/CLAUDE.md            — global TA rules + course overview
  content/week-NN/CLAUDE.md    — that week's topic + an index of its materials

Run standalone or via pipeline.sync (called at the end of a sync).
"""
from __future__ import annotations

import json

from pipeline import config as C

GLOBAL_MEMORY = """# ME/CE/AM 295 — AI TA (course memory)

You are the AI Teaching Assistant for **ME/CE/AM 295 — AI Agents for Accelerating
Scientific Discovery and Engineering Research** (Caltech, Fall 2026, 10 weeks).

Course-wide rules (always apply):
- Ground every course answer in the Markdown files in your accessible folders. Use
  Grep/Read to find passages; cite the file titles you used.
- You are scoped to one week at a time. Never discuss or preview a later week's
  content — point students to that week's channel instead.
- Never reveal quiz answer keys or graded-assignment solutions. Coach the reasoning.
- Be concise, encouraging, and precise; prefer Socratic hints for concepts.
- Escalate to a human TA for grades, extensions, personal matters, or when unsure.

Weekly topics:
"""


def load_manifest() -> dict:
    return json.loads(C.MANIFEST_PATH.read_text())["files"]


def build():
    files = load_manifest()

    # global memory with the week map
    lines = [GLOBAL_MEMORY]
    for w, _ in C.WEEK_STARTS:
        lines.append(f"- Week {w}: {C.WEEK_TITLES.get(w, '')}")
    (C.CONTENT_DIR / "CLAUDE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # per-week memory: an index of learning materials in that folder
    by_week: dict[int, list[tuple[str, str]]] = {}
    for entry in files.values():
        cp = entry.get("content_path") or ""
        if not cp.startswith("content/week-"):
            continue
        w = int(entry.get("week", 0) or 0)
        # title comes from the file's frontmatter; fall back to the slug
        title = cp.rsplit("/", 1)[-1][:-3].replace("-", " ").title()
        by_week.setdefault(w, []).append((entry.get("doc_type", ""), title))

    wrote = 0
    for w, _ in C.WEEK_STARTS:
        wdir = C.CONTENT_DIR / f"week-{w:02d}"
        if not wdir.exists():
            continue
        items = sorted(by_week.get(w, []))
        body = [f"# Week {w} — {C.WEEK_TITLES.get(w, '')}", "",
                "You are the Week %d TA. Materials available in this folder:" % w, ""]
        if items:
            for dtype, title in items:
                body.append(f"- {title} ({dtype})")
        else:
            body.append("- (materials pending)")
        body += ["", "Grep/Read these to answer, and cite the titles. Also available: "
                 "the shared syllabus, study guides, and references."]
        (wdir / "CLAUDE.md").write_text("\n".join(body) + "\n", encoding="utf-8")
        wrote += 1

    print(f"Memory: wrote content/CLAUDE.md + {wrote} per-week CLAUDE.md files")


if __name__ == "__main__":
    build()
