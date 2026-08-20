# Deploying the Weekly AI TA to an always-on host

The bot is a long-running Socket-Mode process. This guide runs it 24/7 on a
remote VM you SSH into — either with **Docker** (recommended, self-contained) or
**systemd** (plain VM, no containers).

## What the host needs
- The **`claude` CLI (Node)** — the Claude Agent SDK spawns it. `npm i -g @anthropic-ai/claude-code`. (Baked into the Docker image already.)
- Python 3.12 + the deps in `requirements.txt`.
- A filled-in **`.env`** (never commit it):
  - `SLACK_BOT_TOKEN=xoxb-…`, `SLACK_APP_TOKEN=xapp-…`
  - **Auth — for a class, use `ANTHROPIC_API_KEY=…` (pay-per-use with a spend cap).**
    The personal-subscription `CLAUDE_CODE_OAUTH_TOKEN` works too but Anthropic's
    policy restricts subscription auth for multi-user serving — prefer the API key in production.
  - Optional: `CURRENT_WEEK=10` to unlock all weeks, or omit to gate by the Fall-2026 calendar.
- A populated **`content/`** corpus (see next).

## Provide the full content corpus
The public repo intentionally omits third-party papers (references), quizzes, and
lecture scripts. The bot benefits from the full set. Two options on the host:

**A. Pull from Google Drive (keeps Drive as source of truth) — recommended**
```bash
pip install google-api-python-client google-auth
# Create a Google service account, share the course Drive folder with its email,
# download its JSON key, then:
export GOOGLE_APPLICATION_CREDENTIALS=/opt/me-ce-am-295/sa.json
python -m pipeline.gdrive_sync     # Drive -> materials/
python -m pipeline.sync            # materials/ -> content/  (+ CLAUDE.md memory)
```

**B. Copy your local content/ up**
```bash
rsync -av --delete ./content/ user@host:/opt/me-ce-am-295/content/
```

## Option 1 — Docker (recommended)
```bash
git clone https://github.com/lauren-h-yoon/me-ce-am-295 && cd me-ce-am-295
#   create .env  (see above) ; populate content/  (see above)
cd deploy
docker compose up -d --build
docker compose logs -f            # look for "⚡️ Bolt app is running!"
```
Updates: `git pull && docker compose up -d --build`. Auto-restarts on crash/reboot (`restart: unless-stopped`).

## Option 2 — systemd (plain VM)
```bash
sudo mkdir -p /opt/me-ce-am-295 && sudo chown $USER /opt/me-ce-am-295
git clone https://github.com/lauren-h-yoon/me-ce-am-295 /opt/me-ce-am-295
cd /opt/me-ce-am-295
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
npm install -g @anthropic-ai/claude-code
#   create .env ; populate content/
sudo useradd -r -s /usr/sbin/nologin weekly 2>/dev/null; sudo chown -R weekly /opt/me-ce-am-295
sudo cp deploy/weekly-bot.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now weekly-bot
journalctl -u weekly-bot -f       # look for "⚡️ Bolt app is running!"
```
Updates: `git pull && sudo systemctl restart weekly-bot`.

## Weekly operation
- Refresh materials: re-run the content sync (A or B), then restart the service/container.
- Provision channels once: `python -m bot.provision_channels` (or `PROVISION_ON_START=1`).
- Health check: `@weekly` in `#week-05`, or the assistant pane / `#ask-anything`.

## Notes
- Only ONE instance should run per Slack app (Socket Mode). Don't also run it on your laptop.
- Logs: Docker → `docker compose logs`; systemd → `journalctl -u weekly-bot`.
- The GitHub Pages site deploys separately via GitHub Actions — no host needed.
