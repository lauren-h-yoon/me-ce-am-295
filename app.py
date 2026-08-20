#!/usr/bin/env python3
"""Root entrypoint so the Slack CLI (`slack run`) can start the Bolt app.
The real implementation lives in bot/app.py. Equivalent to `python -m bot.app`."""
from bot.app import main

if __name__ == "__main__":
    main()
