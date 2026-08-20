# ME/CE/AM 295 — Course Infrastructure

AI teaching-assistant infrastructure for **ME/CE/AM 295** (Caltech, Fall 2026):
a self-updating knowledge base that grounds a **per-week Slack bot** and a
**per-week GitHub Pages site**, both fed from the same normalized content.

## The one idea

```
materials/            authoring source (docx / pdf / pptx / md) — instructors edit here
   │  pipeline/sync.py     extract → Markdown, hash, classify (week / type / access), dedupe
   ▼                       + CLAUDE.md memory files (pipeline/build_memory.py)
content/  + manifest.json  canonical normalized Markdown (git-versioned)
   │                        content/week-NN/ · syllabus/ · study-guides/ · references/
   │                        content/_assessments/  (quizzes — outside the agent's reach)
   ├── bot/agent.py  Claude Agent SDK agent, sandboxed to content/week-NN + globals
   │                 native Read/Grep/Glob retrieval · read-only · CLAUDE.md memory
   │                        ▼
   │      bot/app.py  Slack: #week-NN channels + assistant pane
   └── site/ (Quarto) → GitHub Pages (per-week card grid)
```

**Agentic backend (native, no embeddings).** The bot is a Claude Agent SDK agent
(the engine family behind Claude Code). It retrieves with Claude Code's **native
Read/Grep/Glob** over the normalized Markdown — no vector DB required. The week
boundary is a **filesystem sandbox**: `AgentSpec(week=N, scope="week")` sets the
agent's `cwd` + `add_dirs` to `content/week-NN` plus globals (syllabus, study
guides, references), so it *cannot open* another week's folder, and assessments
live outside entirely. It runs read-only (Write/Bash denied) and loads `CLAUDE.md`
as native memory. Cross-weekly agents are just `scope="cumulative"`.

*Optional upgrade:* a semantic pgvector path exists (`pipeline/index.py`,
`query.py`, `db/schema.sql`, `docker-compose.yml`) if you later want embeddings —
not needed for the native setup.

**Robustness contract.** Edit/add/rename/delete anything in `materials/`, re-run
`sync` + `index`, and only what changed is reprocessed (content-hash diffing);
removed sources are purged from `content/` and the vector store. Week number,
document type, and access level are derived from filenames — no hardcoded week
cap, so an 11th week just works. Answer keys (`*_Quiz_KEY`) are auto-classified
instructor-only and **never** enter `content/`, the site, or the student index.

## Layout

| Path | What |
|---|---|
| `materials/` | Course content (weeks 1–10, study guides, references). Authoring source. |
| `content/` | Generated normalized Markdown + `manifest.json` (the index). |
| `pipeline/config.py` | Calendar/week-gating + classification rules (single source of truth). |
| `pipeline/sync.py` | materials → content normalization (incremental). |
| `pipeline/chunk.py` | Markdown-aware, token-sized chunking. |
| `pipeline/index.py` | content → Postgres + pgvector (incremental embed). |
| `pipeline/query.py` | Grounded retrieval: week-gating + access control (the bot's one call). |
| `db/schema.sql` | Postgres schema (pgvector, dim 1024 for Voyage `voyage-3`). |
| `bot/agent.py` | Claude Agent SDK backend: week-scoped agent + `search_course_materials` tool. |
| `bot/slack_app_manifest.yaml` / `manifest.json` | Slack app definition (YAML is the readable source; JSON is generated for the CLI). |
| `bot/provision_channels.py` | Creates `#week-01…#week-10` + core channels (idempotent). |
| `bot/app.py` | Socket-Mode bot; channel + assistant-pane surfaces, both routed to `agent.py`. |
| `app.py` · `slack.json` · `Makefile` | Root entrypoint + Slack CLI hooks + convenience targets. |
| `docker-compose.yml` | Local Postgres + pgvector. |
| `site/` | Quarto site → GitHub Pages *(layer 3 — in progress)*. |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt           # + system: brew install pandoc
npm install -g @anthropic-ai/claude-code   # `claude` CLI — the agent backend spawns it
cp .env.example .env                       # fill ANTHROPIC / VOYAGE / SLACK / DATABASE_URL
```

Shortcut: `make kb` runs sync + Postgres + schema + index in one go; `make help` lists targets.

### 1. Build the knowledge base (native — no DB, no keys)
```bash
python -m pipeline.sync                   # materials → content/ + CLAUDE.md memory
```
That's the whole knowledge base for the native backend: clean per-week Markdown the
agent reads directly. *(Optional semantic upgrade: `docker compose up -d` →
`python -m pipeline.index init && reindex` with `VOYAGE_API_KEY` + `DATABASE_URL`.)*

### 1b. Agent auth (pick one)
```bash
claude setup-token           # A) subscription (Pro/Max) → paste into CLAUDE_CODE_OAUTH_TOKEN  (dev)
# export ANTHROPIC_API_KEY=… # B) pay-per-use → recommended for multi-user production
```

### 2. Slack (workspace: `me-ce-am-295`)

**Two grounded surfaces, one backend:**
- **Per-week channels** — `@ai-ta` in `#week-NN` answers scoped to Week NN.
- **Assistant pane (Agents & AI Apps)** — a dedicated AI-assistant thread with live
  status and week-aware suggested prompts. Opening it from `#week-NN` auto-scopes to
  that week (via `get_thread_context`). Requires the Slack **Developer Program** or a
  paid workspace (manifest enables `assistant_view` + `assistant:write`).

**Dev in a sandbox first (recommended with the Developer Program):** create the app in
your **developer sandbox** org (Enterprise Grid, all paid features + betas), red-team it
there, then install the same manifest to production **me-ce-am-295**.

1. api.slack.com/apps → **Create New App → From a manifest** → pick the sandbox
   (or **me-ce-am-295**) workspace → paste `bot/slack_app_manifest.yaml`.
2. **Install to Workspace** → copy the **Bot User OAuth Token** → `SLACK_BOT_TOKEN`.
3. **Basic Information → App-Level Tokens** → generate with `connections:write`
   → copy → `SLACK_APP_TOKEN`.
4. Provision channels and run the bot:
   ```bash
   export SLACK_BOT_TOKEN=xoxb-...
   python -m bot.provision_channels        # creates #week-01..10 + core channels
   python -m bot.app                        # starts the Socket-Mode bot   (or: make bot)
   ```
   Health check: `@ai-ta what is this week about?` in `#week-01`.

**Slack CLI flow (alternative to the web steps above).** With the [Slack CLI](https://tools.slack.dev/slack-cli):
```bash
slack login            # authenticate (interactive — run it yourself)
slack app link         # adopt this repo's manifest.json into a new/existing app
slack run              # start the Bolt app locally against your sandbox (Socket Mode)
```
`slack.json` + `app.py` (root) make the CLI able to run this Bolt app; `manifest.json`
is generated from `bot/slack_app_manifest.yaml` (regenerate with
`python -c "import yaml,json;json.dump(yaml.safe_load(open('bot/slack_app_manifest.yaml')),open('manifest.json','w'),indent=2)"`).

### 3. Weekly operation
- `CURRENT_WEEK` is derived from the calendar in `pipeline/config.py` (override with
  the env var for testing). Week channels auto-defer if their week hasn't opened.
- When materials change: `python -m pipeline.sync && python -m pipeline.index reindex`.

### 4. GitHub Pages site
```bash
python -m pipeline.build_site --all   # generate site/ from content/ (--all = full term; omit for calendar-gated)
quarto render site                    # local preview (needs quarto installed)
```
Deploy: push to a GitHub repo, then **Settings → Pages → Source: GitHub Actions**.
`.github/workflows/publish.yml` rebuilds on push, every Tuesday (so gated weeks
unlock automatically), and on manual dispatch. No API key needed — it uses the
built-in Actions token.

## Status
- ✅ Layer 0 — content sync/normalization + CLAUDE.md memory (111 files; quizzes isolated)
- ✅ Layer 1 — **native retrieval** (Read/Grep/Glob, filesystem-sandboxed per week); pgvector path optional
- ✅ Layer 2 — Slack per-week bot: **Claude Agent SDK backend** + channels + assistant pane + Slack CLI project
- ✅ Layer 3 — Quarto per-week card-grid site + Pages CI (91 docs, 10 weeks)

**To go live (your side — no keys shared here):** `python -m pipeline.sync`; install the
`claude` CLI + `claude setup-token` (subscription) or set `ANTHROPIC_API_KEY`; create the
Slack app from `manifest.json` in your sandbox; `python -m bot.provision_channels` then
`make bot` (or `slack run`); push the repo + enable Pages. No Docker/embeddings needed.
