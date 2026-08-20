#!/usr/bin/env python3
"""
Index normalized content (content/**/*.md) into Postgres + pgvector.

Incremental by content hash: a document is re-chunked/re-embedded only when its
Markdown changed; documents whose content file disappeared are deleted (cascading
to their chunks). This is the second half of the robustness contract — the vector
store tracks content/, which tracks materials/.

Instructor-only material never reaches content/, so it can never be indexed here.

Usage:
    python -m pipeline.index init        # create tables/extension
    python -m pipeline.index reindex     # incremental (default)
    python -m pipeline.index reindex --force
    python -m pipeline.index stats
"""
from __future__ import annotations

import argparse
import sys

from pipeline import config as C
from pipeline.chunk import chunk_markdown
from pipeline.util import parse_frontmatter, sha256_text


def _iter_content():
    for p in sorted(C.CONTENT_DIR.rglob("*.md")):
        if p.name == "manifest.json":
            continue
        yield p


def reindex(force: bool = False):
    from pipeline.db import get_conn
    from pipeline.embeddings import Embedder

    embedder = Embedder()
    added = updated = skipped = deleted = 0
    seen_sources: set[str] = set()

    with get_conn() as conn:
        for path in _iter_content():
            md = path.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(md)
            source = meta.get("source") or str(path.relative_to(C.REPO_ROOT))
            content_rel = str(path.relative_to(C.REPO_ROOT))
            content_hash = sha256_text(md)
            seen_sources.add(source)

            with conn.cursor() as cur:
                cur.execute("SELECT id, content_hash FROM documents WHERE source = %s", (source,))
                row = cur.fetchone()

            if row and row[1] == content_hash and not force:
                skipped += 1
                continue

            week = int(meta.get("week", 0) or 0)
            doc_type = meta.get("doc_type", "lecture_notes")
            access = meta.get("access", C.ACCESS_ALL)
            agents = meta.get("agents") or C.agents_for(doc_type)

            chunks = chunk_markdown(
                md,
                chunk_tokens=C.rag.chunk_tokens,
                overlap_tokens=C.rag.chunk_overlap,
                min_chunk_tokens=C.rag.min_chunk_tokens,
            )
            if not chunks:
                continue
            embeddings = embedder.embed_documents([c.text for c in chunks])

            with conn.cursor() as cur:
                # Upsert the document row, then replace its chunks wholesale.
                cur.execute(
                    """
                    INSERT INTO documents (source, content_path, title, week, doc_type,
                                           access, agents, content_hash, updated_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s, now())
                    ON CONFLICT (source) DO UPDATE SET
                        content_path=EXCLUDED.content_path, title=EXCLUDED.title,
                        week=EXCLUDED.week, doc_type=EXCLUDED.doc_type,
                        access=EXCLUDED.access, agents=EXCLUDED.agents,
                        content_hash=EXCLUDED.content_hash, updated_at=now()
                    RETURNING id
                    """,
                    (source, content_rel, meta.get("title", path.stem), week,
                     doc_type, access, agents, content_hash),
                )
                doc_id = cur.fetchone()[0]
                cur.execute("DELETE FROM chunks WHERE document_id = %s", (doc_id,))
                for c, emb in zip(chunks, embeddings):
                    cur.execute(
                        """
                        INSERT INTO chunks (document_id, chunk_index, section_title, text,
                                            token_count, week, doc_type, access, agents, embedding)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """,
                        (doc_id, c.chunk_index, c.section_title, c.text, c.token_count,
                         week, doc_type, access, agents, emb),
                    )
            conn.commit()
            if row:
                updated += 1
                print(f"  [UPDATE] {content_rel} ({len(chunks)} chunks)")
            else:
                added += 1
                print(f"  [ADD]    {content_rel} ({len(chunks)} chunks)")

        # Purge documents whose content file disappeared.
        with conn.cursor() as cur:
            cur.execute("SELECT id, source FROM documents")
            for doc_id, source in cur.fetchall():
                if source not in seen_sources:
                    cur.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
                    print(f"  [PURGE]  {source}")
                    deleted += 1
        conn.commit()

    print(f"\nIndex: +{added} added, ~{updated} updated, ={skipped} unchanged, -{deleted} purged")


def stats():
    from pipeline.db import get_conn
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM documents")
        docs = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM chunks")
        chunks = cur.fetchone()[0]
        cur.execute("SELECT week, count(*) FROM chunks GROUP BY week ORDER BY week")
        by_week = cur.fetchall()
    print(f"documents: {docs}\nchunks: {chunks}")
    print("chunks by week:", {w: c for w, c in by_week})


def main():
    ap = argparse.ArgumentParser(description="Index content/ into Postgres+pgvector")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("init")
    r = sub.add_parser("reindex")
    r.add_argument("--force", action="store_true")
    sub.add_parser("stats")
    args = ap.parse_args()

    if args.cmd == "init":
        from pipeline.db import init_schema
        init_schema()
        print("Schema initialized.")
    elif args.cmd == "stats":
        stats()
    else:  # default reindex
        reindex(force=getattr(args, "force", False))


if __name__ == "__main__":
    main()
