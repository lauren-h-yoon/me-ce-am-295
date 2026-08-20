#!/usr/bin/env python3
"""
Generate the Quarto site (site/) from normalized content/ + manifest.json.

Per-week pages mirror the Slack per-week channels. The site is fully data-driven:
weeks, the navbar, the schedule, and each week's material list are generated from
the manifest, so adding a week or a document needs no edits here — just re-run.

Publishing policy (defense in depth on top of sync's instructor-only exclusion):
  * only access == all_students is published
  * assessment/delivery aids (quiz, lecture_script) are withheld
  * by default only weeks whose start date has passed are published (calendar
    gating that matches the bot); pass --all to publish the whole term.

Usage:
    python -m pipeline.build_site            # calendar-gated
    python -m pipeline.build_site --all      # publish every week (preview / full-term)
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import date

from pipeline import config as C
from pipeline.util import parse_frontmatter

SITE = C.REPO_ROOT / "site"
MATERIALS_OUT = SITE / "materials"
WEEKS_OUT = SITE / "weeks"

# Withheld from the public site even though they live in content/.
# reference/reading = third-party papers (copyright) — kept off the public site;
# lecture_script = instructor delivery notes; quiz = assessment.
EXCLUDE_SITE_TYPES = {"quiz", "lecture_script", "reference", "reading"}

DOC_TYPE_LABEL = {
    "lecture_notes": "Lecture Notes",
    "lecture_slides": "Slides",
    "lecture_outline": "Lecture Outline",
    "lab": "Lab",
    "assignment": "Assignment",
    "reading": "Readings",
    "reference": "References",
    "study_guide": "Study Guides",
    "syllabus": "Syllabus",
}
WEEK_TITLES = C.WEEK_TITLES


def load_manifest() -> dict:
    return json.loads(C.MANIFEST_PATH.read_text())["files"]


def publishable(entry: dict) -> bool:
    return (entry.get("status") == "normalized"
            and entry.get("access") == C.ACCESS_ALL
            and entry.get("doc_type") not in EXCLUDE_SITE_TYPES
            and entry.get("content_path"))


def section_of(content_path: str) -> str:
    # content/<section>/<file>.md
    return content_path.split("/")[1]


def slug_of(content_path: str) -> str:
    return content_path.rsplit("/", 1)[-1][:-3]


def clean_copy(content_path: str) -> tuple[str, str]:
    """Copy a content md into site/materials with a clean (title-only) frontmatter.
    Returns (title, site_html_path_relative_to_site)."""
    src = C.REPO_ROOT / content_path
    meta, body = parse_frontmatter(src.read_text(encoding="utf-8"))
    title = meta.get("title") or slug_of(content_path)
    section = section_of(content_path)
    out = MATERIALS_OUT / section / (slug_of(content_path) + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    fm = f'---\ntitle: "{title}"\n---\n\n'
    out.write_text(fm + body.strip() + "\n", encoding="utf-8")
    return title, f"materials/{section}/{slug_of(content_path)}.html"


def qmd(title: str, body: str) -> str:
    return f'---\ntitle: "{title}"\n---\n\n{body}\n'


def build(publish_all: bool):
    # reset generated areas
    for d in (MATERIALS_OUT, WEEKS_OUT):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True, exist_ok=True)

    files = load_manifest()
    today = date.today()
    week_start = dict(C.WEEK_STARTS)
    open_weeks = {w for w, s in C.WEEK_STARTS if publish_all or s <= today}

    # bucket publishable docs
    by_week: dict[int, list] = {}
    globals_: dict[str, list] = {"study-guides": [], "references": [], "syllabus": []}
    for path, entry in sorted(files.items()):
        if not publishable(entry):
            continue
        week = int(entry.get("week", 0) or 0)
        title, href = clean_copy(entry["content_path"])
        item = (entry["doc_type"], title, href)
        if week >= 1:
            by_week.setdefault(week, []).append(item)
        else:
            sec = section_of(entry["content_path"])
            globals_.setdefault(sec, []).append(item)

    # ---- per-week pages ----
    for w, _ in C.WEEK_STARTS:
        wt = WEEK_TITLES.get(w, "")
        start = week_start.get(w)
        when = start.strftime("%b %-d, %Y") if start else "TBD"
        if w not in open_weeks:
            body = (f"::: {{.callout-note}}\n## 🔒 Opens {when}\n"
                    f"Week {w} materials unlock on {when}.\n:::")
            (WEEKS_OUT / f"week-{w:02d}.qmd").write_text(qmd(f"Week {w} — {wt}", body))
            continue
        items = by_week.get(w, [])
        lines = [f"*Opened {when}. Ask **@ai-ta** in `#week-{w:02d}` on Slack.*", ""]
        if not items:
            lines.append("_Materials will be posted here._")
        else:
            for dtype in ["lecture_notes", "lecture_slides", "lecture_outline",
                          "lab", "assignment", "reading"]:
                group = [(t, h) for (dt, t, h) in items if dt == dtype]
                if group:
                    lines.append(f"### {DOC_TYPE_LABEL.get(dtype, dtype.title())}")
                    for t, h in group:
                        lines.append(f"- [{t}](../{h})")
                    lines.append("")
        (WEEKS_OUT / f"week-{w:02d}.qmd").write_text(qmd(f"Week {w} — {wt}", "\n".join(lines)))

    # ---- schedule ----
    rows = ["| Week | Topic | Opens | Status |", "|---|---|---|---|"]
    for w, s in C.WEEK_STARTS:
        status = "✅ open" if w in open_weeks else "🔒 locked"
        rows.append(f"| [Week {w}](weeks/week-{w:02d}.qmd) | {WEEK_TITLES.get(w,'')} "
                    f"| {s:%b %-d, %Y} | {status} |")
    (SITE / "schedule.qmd").write_text(qmd("Schedule", "\n".join(rows)))

    # ---- syllabus (inline the normalized syllabus doc) ----
    syl = globals_["syllabus"]
    if syl:
        _, _, href = syl[0]
        (SITE / "syllabus.qmd").write_text(qmd(
            "Syllabus", f"[Open the full syllabus](../{href})\n\n"
            "See the [schedule](schedule.qmd) for weekly topics and open dates."))

    # ---- study guides & references landing ----
    def landing(title, items):
        if not items:
            return f"_No {title.lower()} yet._"
        return "\n".join(f"- [{t}](../{h})" for _, t, h in sorted(items))
    (SITE / "study-guides.qmd").write_text(qmd("Study Guides", landing("study guides", globals_["study-guides"])))
    # References (third-party papers) are NOT published — point enrolled students to Drive.
    ref_url = C.drive_folder_url(C.DRIVE_GLOBAL_FOLDERS["references"])
    (SITE / "references.qmd").write_text(qmd(
        "References",
        "The reading list — papers and further reading — is available to enrolled "
        f"students in the course [Google Drive → References folder]({ref_url}). "
        "Third-party papers are not reposted here for copyright reasons."))

    # ---- home ----
    cards = []
    for w, s in C.WEEK_STARTS:
        locked = "" if w in open_weeks else " locked"
        badge = '<span class="badge-open">● open</span>' if w in open_weeks \
            else f'<span class="badge-locked">🔒 opens {s:%b %-d}</span>'
        cards.append(
            f'<a class="week-card{locked}" href="weeks/week-{w:02d}.html">'
            f'<span class="wk-num">Week {w}</span>'
            f'<span class="wk-title">{WEEK_TITLES.get(w,"")}</span>{badge}</a>')
    home = ("ME/CE/AM 295 — **AI Agents for Accelerating Scientific Discovery and "
            "Engineering Research** (Caltech, Fall 2026).\n\n"
            "Browse by week below, check the [schedule](schedule.qmd), or ask the "
            "[AI TA](ai-ta.qmd) on Slack.\n\n"
            '<div class="week-grid">\n' + "\n".join(cards) + "\n</div>")
    (SITE / "index.qmd").write_text(qmd("ME/CE/AM 295", home))

    # ---- AI TA page ----
    (SITE / "ai-ta.qmd").write_text(qmd("AI Teaching Assistant",
        "Every week has a Slack channel `#week-NN` with an AI TA scoped to that "
        "week's materials.\n\n"
        "**How to use it**\n\n"
        "- Post in your week's channel or `@ai-ta` it; DMs work too.\n"
        "- It answers from the course materials for that week (and earlier).\n"
        "- It won't hand out quiz answer keys — it coaches the reasoning.\n"
        "- React ⭐ if an answer helped, 🚩 if it was wrong (a human TA reviews flags).\n\n"
        f"Join the workspace: [me-ce-am-295.slack.com](https://me-ce-am-295.slack.com)."))

    # ---- _quarto.yml (navbar generated from open weeks) ----
    week_menu = "\n".join(
        f"          - href: weeks/week-{w:02d}.qmd\n            text: \"Week {w}: {WEEK_TITLES.get(w,'')}\""
        for w, _ in C.WEEK_STARTS)
    quarto_yml = f"""project:
  type: website
  output-dir: _site

website:
  title: "ME/CE/AM 295"
  navbar:
    background: primary
    left:
      - href: index.qmd
        text: Home
      - href: schedule.qmd
        text: Schedule
      - text: Weeks
        menu:
{week_menu}
      - href: study-guides.qmd
        text: Study Guides
      - href: references.qmd
        text: References
      - href: syllabus.qmd
        text: Syllabus
      - href: ai-ta.qmd
        text: AI TA

format:
  html:
    theme: [cosmo, assets/styles.css]
    toc: true
    page-layout: full
"""
    (SITE / "_quarto.yml").write_text(quarto_yml)

    n_docs = sum(len(v) for v in by_week.values()) + sum(len(v) for v in globals_.values())
    print(f"Site generated: {len(open_weeks)} weeks open, {n_docs} documents published.")
    print(f"  render locally with:  quarto render site")


def main():
    ap = argparse.ArgumentParser(description="Generate Quarto site from content/")
    ap.add_argument("--all", action="store_true", help="publish every week (ignore calendar gating)")
    build(ap.parse_args().all)


if __name__ == "__main__":
    main()
