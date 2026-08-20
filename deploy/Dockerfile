# ME/CE/AM 295 — Weekly AI TA bot image.
# The Claude Agent SDK spawns the Claude Code CLI (Node), so the image needs
# Node + @anthropic-ai/claude-code alongside Python. pandoc is included so the
# in-container content sync (pipeline.sync / gdrive_sync) can run if desired.
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg pandoc git tini \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get install -y --no-install-recommends nodejs \
 && npm install -g @anthropic-ai/claude-code \
 && npm cache clean --force \
 && apt-get purge -y --auto-remove curl gnupg \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code. content/ is provided at runtime via a volume (see docker-compose)
# so the bot reads the full, current corpus (incl. references) without baking it in.
COPY . .

ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app
# tini for correct signal handling (clean shutdown of the socket + claude subprocesses)
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "-m", "bot.app"]
