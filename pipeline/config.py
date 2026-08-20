"""
ME/CE/AM 295 — Course infra: central configuration.

Single source of truth for paths, the teaching calendar (week gating),
document-type / access classification rules, and provider settings.

Design note (robustness to change): NOTHING here hardcodes a maximum week
count. `detect_week` accepts any positive integer, and `current_week` is
derived from the calendar. Adding a Week 11 folder Just Works.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
MATERIALS_DIR = REPO_ROOT / "materials"   # authoring source (docx/pdf/pptx)
CONTENT_DIR = REPO_ROOT / "content"       # generated normalized Markdown
MANIFEST_PATH = CONTENT_DIR / "manifest.json"

# Folders under materials/ that are NEVER ingested.
EXCLUDE_DIRS = {"Archive", "TA & Setup", "__pycache__"}

# Filename fragments that mark superseded / duplicate files to skip.
EXCLUDE_FILE_MARKERS = ("_dup_", "_old_", "_superseded", "~$")

# Duplicate copies like "Ref_01_...(1).pdf" — skip the "(N)" siblings.
DUP_COPY_RE = re.compile(r"\(\d+\)\.[A-Za-z0-9]+$")


# ------------------------------------------------------------------
# Teaching calendar / week gating (Fall 2026, Caltech)
# ------------------------------------------------------------------
# Tuesday that each teaching week opens. Extend this list to add weeks;
# nothing else needs to change.
WEEK_STARTS: list[tuple[int, date]] = [
    (1, date(2026, 9, 29)),
    (2, date(2026, 10, 6)),
    (3, date(2026, 10, 13)),
    (4, date(2026, 10, 20)),
    (5, date(2026, 10, 27)),
    (6, date(2026, 11, 3)),
    (7, date(2026, 11, 10)),
    (8, date(2026, 11, 17)),
    (9, date(2026, 11, 24)),
    (10, date(2026, 12, 1)),
]
TERM_END = date(2026, 12, 11)

# Human-readable week topics (shared by the bot's suggested prompts and the site).
WEEK_TITLES = {
    1: "The Dawn of Agentic AI", 2: "Foundations of LLMs",
    3: "Agentic Frameworks", 4: "Retrieval-Augmented Generation",
    5: "Scientific ML & PINNs", 6: "Neural Operators",
    7: "Code Generation", 8: "Generative Design & Self-Driving Labs",
    9: "Evaluation, Reliability & Deployment", 10: "Ethics & the Future",
}


# ------------------------------------------------------------------
# Google Drive — the course source-of-truth (folder "ME/CE/AM 295 (Caltech)",
# owned by daraio@caltech.edu, shared to the course team). Each week channel
# links to its folder; a sync can pull these into materials/ (see gdrive_sync).
# ------------------------------------------------------------------
DRIVE_ROOT_FOLDER_ID = "1fzD6QRkkigSvLJKSjw90P-J-aqpyaFZc"
DRIVE_WEEK_FOLDERS: dict[int, str] = {
    1: "1qJ78VNP_mDy5Y4Ml5Hp--aeGnnAVQY53",
    2: "1883RtiSBS2VK_9rWBT9KNSiRYK6uzUhF",
    3: "1l2ucpMiI2rnBcp5LHPGz7VLF9flVofvJ",
    4: "13vn2h2KaB9UGAGwsJOEWRyE6j_Aa87ey",
    5: "14xBPb_7IsmXj1gyoX9hRpGlhY5xZRVb9",
    6: "1mPQNUM5Kvg6t65XD5CFZeEr1oA-wAOeA",
    7: "1Ed5pqUcB7rTEJURlkwFltEwcttJ86c1h",
    8: "1UAVAxFTCCv47L_ouo5ziCE9K-0lyXIS7",
    9: "1LpSePvTUGbexvrRdReu_U0VM4vOwF9nf",
    10: "1PwpQFqem2pAMuM0u6Yqzrp5ulA7zEYrq",
}
DRIVE_GLOBAL_FOLDERS: dict[str, str] = {
    "study-guides": "1-xX_ITau3iXyeaOkjgu5RXj7CeV2S9D9",
    "references": "14nd8yWllcRdtkEcYE_lqylw5p_pDiujy",
}


def drive_folder_url(folder_id: str) -> str:
    return f"https://drive.google.com/drive/folders/{folder_id}"


def drive_week_url(week: int) -> str | None:
    fid = DRIVE_WEEK_FOLDERS.get(week)
    return drive_folder_url(fid) if fid else None


def current_week(today: date | None = None) -> int:
    """Gating week for `today`. Before term start -> 1; after the last week
    starts, stays at the final week. Can be overridden with CURRENT_WEEK env."""
    override = os.getenv("CURRENT_WEEK")
    if override:
        return int(override)
    today = today or date.today()
    week = WEEK_STARTS[0][0]
    for w, start in WEEK_STARTS:
        if today >= start:
            week = w
    return week


def max_week() -> int:
    return max(w for w, _ in WEEK_STARTS)


# ------------------------------------------------------------------
# Document classification
# ------------------------------------------------------------------
# Detect "Week 10", "Week10", "week_3", "wk-2", "w4_" -> int (any positive N).
WEEK_PATTERNS = [
    re.compile(r"week[_\s-]*(\d+)", re.I),
    re.compile(r"\bwk[_\s-]*(\d+)", re.I),
    re.compile(r"\bw(\d+)[_\s-]", re.I),
]

# doc_type ordering matters: earlier, more specific patterns win.
# NOTE: solution_key / rubric are checked BEFORE quiz so "Quiz_KEY" is never
# mis-filed as a student-visible quiz.
DOC_TYPE_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("syllabus",        ("syllabus", "course_overview")),
    ("study_guide",     ("study_guide", "study-guide", "studyguide")),
    ("solution_key",    ("_key", "answer_key", "solution", "_sol")),
    ("rubric",          ("rubric", "grading_criteria")),
    ("quiz",            ("quiz", "assessment")),
    ("lecture_outline", ("lecture_outline", "lecture-outline")),
    ("lecture_script",  ("presentation_script", "presentation-script", "_script")),
    ("lecture_slides",  ("slides", "slide", "presentation", "deck", ".pptx")),
    ("lab",             ("lab_instructions", "lab-", "hands-on-lab")),
    ("assignment",      ("assignment", "homework", "hw_", "hw1", "hw2", "briefing")),
    ("reading",         ("reading", "reading_list")),
    ("reference",       ("ref_", "reference", "_review", "_survey", "_critique")),
]

# Access levels.
ACCESS_ALL = "all_students"
ACCESS_POST_DEADLINE = "post_deadline"
ACCESS_INSTRUCTOR = "instructor_only"

INSTRUCTOR_ONLY_TYPES = {"solution_key", "rubric"}
POST_DEADLINE_TYPES = {"quiz"}

# Which agent(s) a doc_type is exposed to (student-facing routing hint).
AGENT_ACCESS = {
    "syllabus":        ["syllabus_agent", "all_student_agents"],
    "study_guide":     ["all_student_agents"],
    "lecture_outline": ["all_student_agents", "concept_tutor"],
    "lecture_script":  ["all_student_agents", "concept_tutor"],
    "lecture_notes":   ["all_student_agents", "concept_tutor"],
    "lecture_slides":  ["all_student_agents", "concept_tutor"],
    "lab":             ["all_student_agents", "lab_coach"],
    "assignment":      ["all_student_agents", "lab_coach"],
    "reading":         ["all_student_agents", "literature_scout"],
    "reference":       ["all_student_agents", "literature_scout"],
    "quiz":            ["quiz_prep"],
    "solution_key":    ["grading_agent"],
    "rubric":          ["grading_agent"],
}


def detect_week(*texts: str) -> int:
    """Return week number from any of the given strings (filename, path). 0 = all-weeks."""
    for text in texts:
        for pat in WEEK_PATTERNS:
            m = pat.search(text)
            if m:
                return int(m.group(1))
    return 0


def detect_doc_type(name: str, path: str = "") -> str:
    hay = f"{path}/{name}".lower()
    for doc_type, markers in DOC_TYPE_RULES:
        if any(m in hay for m in markers):
            return doc_type
    return "lecture_notes"  # default for core weekly content docs


def access_level_for(doc_type: str) -> str:
    if doc_type in INSTRUCTOR_ONLY_TYPES:
        return ACCESS_INSTRUCTOR
    if doc_type in POST_DEADLINE_TYPES:
        return ACCESS_POST_DEADLINE
    return ACCESS_ALL


def agents_for(doc_type: str) -> list[str]:
    return AGENT_ACCESS.get(doc_type, ["all_student_agents"])


# ------------------------------------------------------------------
# Chunking / retrieval defaults
# ------------------------------------------------------------------
@dataclass
class RAGConfig:
    embed_model: str = os.getenv("VOYAGE_EMBED_MODEL", "voyage-3")
    embed_dim: int = 1024              # voyage-3 output dimension
    chunk_tokens: int = 512
    chunk_overlap: int = 64
    min_chunk_tokens: int = 64
    top_k: int = 6
    similarity_threshold: float = 0.25  # cosine similarity floor
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/me_ce_am_295")


rag = RAGConfig()
