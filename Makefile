# ME/CE/AM 295 course infra — convenience targets.
# Prereqs: python deps installed (pip install -r requirements.txt), pandoc,
# the `claude` CLI (for the bot), and a filled-in .env.
# Uses the local venv automatically if present.
PYTHON ?= $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)

.PHONY: help sync db-up db-init index kb site bot slack-run clean-site

help:
	@echo "sync      normalize materials/ -> content/"
	@echo "db-up     start local Postgres+pgvector (Docker)"
	@echo "db-init   create schema (run once, after db-up)"
	@echo "index     embed content/ -> vector store (needs VOYAGE_API_KEY)"
	@echo "kb        full knowledge base: sync + db-up + db-init + index"
	@echo "site      generate + render the Quarto site (needs quarto)"
	@echo "bot       run the Slack bot via Socket Mode (python -m bot.app)"
	@echo "slack-run run the bot via the Slack CLI (needs `slack login`)"

sync:
	$(PYTHON) -m pipeline.sync

db-up:
	docker compose up -d

db-init:
	$(PYTHON) -m pipeline.index init

index:
	$(PYTHON) -m pipeline.index reindex

kb: sync db-up
	@echo "waiting for Postgres…" && sleep 5
	$(MAKE) db-init
	$(MAKE) index
	$(PYTHON) -m pipeline.index stats

site:
	$(PYTHON) -m pipeline.build_site --all
	quarto render site

bot:
	$(PYTHON) -m bot.app

slack-run:
	slack run

clean-site:
	rm -rf site/_site site/.quarto site/materials site/weeks site/*.qmd site/_quarto.yml
