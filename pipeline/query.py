#!/usr/bin/env python3
"""
Retrieval interface — the ONE thing the Slack agents call to stay grounded.

Enforces, in a single SQL query:
  * week-gating   : only chunks with week <= current_week (0 = always-available)
  * access control: students never see instructor-only material
  * agent routing : chunk must target this agent or 'all_student_agents'

Usage:
    python -m pipeline.query --q "How does ReAct combine reasoning and acting?" \
        --agent concept_tutor --week 3
"""
from __future__ import annotations

import argparse

from pipeline import config as C

STUDENT_ACCESS = (C.ACCESS_ALL, C.ACCESS_POST_DEADLINE)


def retrieve(
    question: str,
    agent: str = "all_student_agents",
    current_week: int | None = None,
    top_k: int | None = None,
    include_post_deadline: bool = False,
    scope_weeks: list[int] | None = None,
) -> list[dict]:
    """Vector search with week-gating + access control.

    scope_weeks: if given, restrict to exactly these weeks (e.g. [0, 5] = Week 5
    plus always-available globals). Otherwise return everything with week <=
    current_week (cumulative gating).
    """
    from pipeline.db import get_conn
    from pipeline.embeddings import Embedder

    week = current_week if current_week is not None else C.current_week()
    top_k = top_k or C.rag.top_k
    q_emb = Embedder().embed_query(question)

    # Access set: students see all_students always; post-deadline only when allowed.
    access_set = [C.ACCESS_ALL]
    if include_post_deadline or agent == "quiz_prep":
        access_set.append(C.ACCESS_POST_DEADLINE)
    # grading_agent would use instructor material, but that is never indexed here.

    if scope_weeks is not None:
        week_clause = "c.week = ANY(%(weeks)s)"
    else:
        week_clause = "c.week <= %(week)s"

    sql = f"""
        SELECT c.text, c.section_title, c.week, c.doc_type, d.title, d.source,
               1 - (c.embedding <=> %(qe)s::vector) AS similarity
        FROM chunks c
        JOIN documents d ON d.id = c.document_id
        WHERE {week_clause}
          AND c.access = ANY(%(access)s)
          AND (%(agent)s = ANY(c.agents) OR 'all_student_agents' = ANY(c.agents))
        ORDER BY c.embedding <=> %(qe)s::vector
        LIMIT %(k)s
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, {"qe": q_emb, "week": week, "weeks": scope_weeks or [],
                          "access": access_set, "agent": agent, "k": top_k})
        rows = cur.fetchall()

    results = []
    for text, section, wk, doc_type, title, source, sim in rows:
        if sim < C.rag.similarity_threshold:
            continue
        results.append({
            "text": text, "section_title": section, "week": wk,
            "doc_type": doc_type, "title": title, "source": source,
            "similarity": round(float(sim), 4),
        })
    return results


def get_context(question: str, agent: str, current_week: int | None = None,
                top_k: int | None = None) -> str:
    """Format retrieved chunks into a grounding block for an agent prompt."""
    results = retrieve(question, agent, current_week, top_k)
    if not results:
        return ("[COURSE CONTEXT — none found]\nNo course materials matched. Answer from "
                "general knowledge and say you couldn't find specific course materials.")
    parts = [f"[COURSE CONTEXT — {len(results)} passages, week-gated]"]
    for i, r in enumerate(results, 1):
        parts.append(
            f"\n--- Source {i}: {r['title']} (Week {r['week']}, {r['doc_type']}, "
            f"rel {r['similarity']:.2f}) ---\n{r['text']}"
        )
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Query the knowledge base")
    ap.add_argument("--q", required=True)
    ap.add_argument("--agent", default="concept_tutor")
    ap.add_argument("--week", type=int, default=None)
    ap.add_argument("--top-k", type=int, default=None)
    args = ap.parse_args()
    print(get_context(args.q, args.agent, args.week, args.top_k))


if __name__ == "__main__":
    main()
