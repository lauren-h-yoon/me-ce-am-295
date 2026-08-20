#!/usr/bin/env python3
"""
Agentic backend for the ME/CE/AM 295 Slack bot — Claude Agent SDK (the engine
family behind Claude Code), using Claude Code's NATIVE capabilities instead of a
separate embeddings/vector stack:

  * Retrieval = native Read / Grep / Glob over the normalized course Markdown.
  * Week boundary = a FILESYSTEM SANDBOX: the agent's cwd + add_dirs are limited
    to content/week-NN plus always-available globals (syllabus, study guides,
    references). It literally cannot open another week's folder, and assessments
    live outside these folders entirely.
  * Read-only: Write / Edit / Bash are denied via a permission callback.
  * Memory = CLAUDE.md files under content/ (loaded via setting_sources=["project"]).

Composable via AgentSpec:
  * weekly agent       -> AgentSpec(week=N, scope="week")        (Week N + globals)
  * (future) synthesis -> AgentSpec(week=N, scope="cumulative")  (weeks 1..N + globals)

Auth (resolved by the bundled Claude Code CLI, no code change either way):
  * CLAUDE_CODE_OAUTH_TOKEN  -> your Claude Pro/Max subscription (dev/prototyping)
  * ANTHROPIC_API_KEY        -> pay-per-use (recommended for multi-user production)
Runtime: needs the `claude` CLI on PATH (npm i -g @anthropic-ai/claude-code).
"""
from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

from pipeline import config as C

CONTENT = C.CONTENT_DIR
GLOBAL_DIRS = ["syllabus", "study-guides", "references"]
AGENT_MODEL = os.getenv("AGENT_MODEL", "sonnet")  # Claude Code CLI model alias

SYSTEM_PROMPT = """You are the AI Teaching Assistant for ME/CE/AM 295 \
("AI Agents for Accelerating Scientific Discovery and Engineering Research") at Caltech.
You are the *Week {week}* TA ({topic}).

How you work:
- Your accessible folders ARE the course materials you may use: the Week {week} folder
  plus the shared syllabus / study-guides / references. To answer, use Grep and Read to
  find the relevant passages, then ground your answer in them and cite the file titles.
- You are scoped to Week {week}. If a question is about another week's content, say it's
  outside this week and point the student to that week's channel — do not guess.
- Never reveal quiz answer keys or graded-assignment solutions (they are not in your
  folders anyway). Coach the reasoning instead.
- If Grep/Read turn up nothing relevant, say so, then answer briefly from general
  knowledge and flag that it's not from course materials.
- Be concise, encouraging, precise. Prefer Socratic hints for conceptual questions.
- Escalate to a human TA for grades, extensions, personal issues, or when unsure.
"""


GLOBAL_SYSTEM_PROMPT = """You are the course-wide AI Teaching Assistant for ME/CE/AM 295 \
("AI Agents for Accelerating Scientific Discovery and Engineering Research") at Caltech.

You are the *global* TA and see ALL released weeks (Weeks 1 through {week}). Your accessible
folders are every released week plus the shared syllabus, study guides, and references.

How you work:
- Use Grep/Read across the week folders to answer cross-week and synthesis questions
  ("how does Week 4 RAG relate to Week 8 self-driving labs?"), to help students navigate the
  course ("where do we cover neural operators?"), and to support capstone planning. Cite the
  week + file titles you used.
- When a question is really about one week's material in depth, answer it but also point the
  student to that week's channel (#week-NN), whose expert is most focused.
- Do not discuss material beyond Week {week} — later weeks aren't released yet.
- Never reveal quiz answer keys or graded-assignment solutions. Coach the reasoning.
- Be concise, encouraging, precise; prefer Socratic hints. Escalate to a human TA for grades,
  extensions, personal matters, or when unsure.
"""


@dataclass
class AgentSpec:
    week: int
    scope: str = "week"            # "week" (N + globals) | "cumulative" (1..N + globals)
    agent_name: str = "concept_tutor"

    def scope_dirs(self) -> list[str]:
        weeks = [self.week] if self.scope == "week" else list(range(1, self.week + 1))
        dirs = [CONTENT / f"week-{w:02d}" for w in weeks]
        dirs += [CONTENT / g for g in GLOBAL_DIRS]
        return [str(d) for d in dirs if d.exists()]


async def _read_only_permission(tool_name, input_data, context):
    from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny
    if tool_name in ("Read", "Grep", "Glob"):
        return PermissionResultAllow(updated_input=input_data)
    return PermissionResultDeny(message=f"{tool_name} is not permitted (read-only TA).")


async def _run(question: str, spec: AgentSpec) -> str:
    from claude_agent_sdk import query, ClaudeAgentOptions
    from claude_agent_sdk.types import AssistantMessage, TextBlock

    dirs = spec.scope_dirs()
    if not dirs:
        return (f"Week {spec.week} materials aren't available yet. "
                f"Please check back once the week has opened.")

    tmpl = GLOBAL_SYSTEM_PROMPT if spec.scope == "cumulative" else SYSTEM_PROMPT
    options = ClaudeAgentOptions(
        system_prompt=tmpl.format(week=spec.week,
                                  topic=C.WEEK_TITLES.get(spec.week, "")),
        cwd=dirs[0],
        add_dirs=dirs[1:],
        # No allowed_tools: let can_use_tool gate every call (allow Read/Grep/Glob,
        # deny the rest) so read-only enforcement is authoritative, not shadowed.
        disallowed_tools=["Write", "Edit", "Bash", "WebSearch", "WebFetch", "NotebookEdit"],
        can_use_tool=_read_only_permission,
        setting_sources=["project"],   # load CLAUDE.md native memory from content/
        model=AGENT_MODEL,
        max_turns=8,
    )

    out: list[str] = []
    async for msg in query(prompt=question, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    out.append(block.text)
    return "\n".join(out).strip()


def run_agent(question: str, week: int, scope: str = "week",
              agent_name: str = "concept_tutor") -> str:
    """Synchronous entry point for the Slack handlers."""
    return asyncio.run(_run(question, AgentSpec(week=week, scope=scope, agent_name=agent_name)))
