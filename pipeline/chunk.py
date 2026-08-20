"""
Markdown-aware chunking for the ME/CE/AM 295 knowledge base.

Dependency-free (tiktoken used if present, else a char-based token estimate) so
it can be unit-tested without the AI/DB stack. Splits normalized Markdown into
~chunk_tokens windows with sentence-level overlap, tracking the nearest heading
as `section_title` for source attribution.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
except Exception:  # tiktoken not installed — approximate
    _ENC = None


def count_tokens(text: str) -> int:
    if _ENC is not None:
        return len(_ENC.encode(text))
    # ~4 chars per token is a reasonable English approximation
    return max(1, len(text) // 4)


FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def strip_frontmatter(md: str) -> str:
    return FRONTMATTER_RE.sub("", md, count=1)


@dataclass
class Chunk:
    text: str
    section_title: str
    chunk_index: int
    token_count: int


def _blocks(md: str):
    """Yield (section_title, block_text) for each paragraph/heading block."""
    current_section = ""
    buf: list[str] = []

    def flush():
        nonlocal buf
        if buf:
            block = "\n".join(buf).strip()
            buf = []
            if block:
                return block
        return None

    for line in md.splitlines():
        m = HEADING_RE.match(line)
        if m:
            b = flush()
            if b:
                yield current_section, b
            current_section = m.group(2).strip()
            yield current_section, line.strip()  # keep heading text as its own block
        elif line.strip() == "":
            b = flush()
            if b:
                yield current_section, b
        else:
            buf.append(line)
    b = flush()
    if b:
        yield current_section, b


def _split_long(text: str, max_tokens: int) -> list[str]:
    """Split an oversized block into <=max_tokens pieces on sentence boundaries."""
    sentences = SENT_SPLIT_RE.split(text)
    out, cur, cur_tok = [], [], 0
    for s in sentences:
        st = count_tokens(s)
        if cur and cur_tok + st > max_tokens:
            out.append(" ".join(cur))
            cur, cur_tok = [], 0
        cur.append(s)
        cur_tok += st
    if cur:
        out.append(" ".join(cur))
    return out


def chunk_markdown(
    md: str,
    chunk_tokens: int = 512,
    overlap_tokens: int = 64,
    min_chunk_tokens: int = 64,
) -> list[Chunk]:
    md = strip_frontmatter(md)

    # Pack blocks greedily up to chunk_tokens.
    packed: list[tuple[str, str]] = []  # (section_title, text)
    cur_text: list[str] = []
    cur_section = ""
    cur_tok = 0

    def emit():
        nonlocal cur_text, cur_tok
        if cur_text:
            packed.append((cur_section, "\n\n".join(cur_text).strip()))
            cur_text, cur_tok = [], 0

    for section, block in _blocks(md):
        btok = count_tokens(block)
        if btok > chunk_tokens:
            emit()
            for piece in _split_long(block, chunk_tokens):
                packed.append((section, piece))
            cur_section = section
            continue
        if cur_tok + btok > chunk_tokens and cur_text:
            emit()
        if not cur_text:
            cur_section = section
        cur_text.append(block)
        cur_tok += btok
    emit()

    # Add sentence-level overlap: prepend tail of previous chunk to each chunk.
    chunks: list[Chunk] = []
    prev_tail = ""
    for i, (section, text) in enumerate(packed):
        body = (prev_tail + "\n\n" + text).strip() if prev_tail else text
        tok = count_tokens(body)
        if tok < min_chunk_tokens and chunks:
            # merge tiny trailing fragment into previous chunk
            prev = chunks[-1]
            merged = prev.text + "\n\n" + text
            chunks[-1] = Chunk(merged, prev.section_title, prev.chunk_index, count_tokens(merged))
        else:
            chunks.append(Chunk(body, section, len(chunks), tok))
        # compute overlap tail for next chunk
        sents = SENT_SPLIT_RE.split(text)
        tail, ttok = [], 0
        for s in reversed(sents):
            ttok += count_tokens(s)
            tail.insert(0, s)
            if ttok >= overlap_tokens:
                break
        prev_tail = " ".join(tail)

    return chunks


if __name__ == "__main__":
    import sys
    from pathlib import Path
    p = Path(sys.argv[1])
    cs = chunk_markdown(p.read_text())
    print(f"{p.name}: {len(cs)} chunks")
    for c in cs[:3]:
        print(f"  [{c.chunk_index}] §{c.section_title!r} ({c.token_count} tok): {c.text[:80]!r}")
