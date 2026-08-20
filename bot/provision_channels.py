#!/usr/bin/env python3
"""
One-time provisioning of the per-week channel structure in the me-ce-am-295
workspace. Idempotent: existing channels are reused, not duplicated.

Creates:  #announcements, #general, #ai-ta-help, and #week-01 .. #week-NN
(N = max week in pipeline/config.py, so adding weeks needs no edit here).

Run:
    export SLACK_BOT_TOKEN=xoxb-...      # from the installed app
    python -m bot.provision_channels          # create + set topics + join
    python -m bot.provision_channels --dry-run
"""
from __future__ import annotations

import argparse
import os
import re
import sys

from pipeline import config as C

CORE_CHANNELS = [
    ("announcements", "Official course announcements. Read-only for students."),
    ("general", "General course chat and logistics."),
]


def week_channels() -> list[tuple[str, str]]:
    out = []
    for w, start in C.WEEK_STARTS:
        out.append((f"week-{w:02d}",
                    f"Week {w} materials & discussion — opens {start:%b %-d}. "
                    f"@weekly is scoped to Week {w} here."))
    return out


def provision(dry_run: bool = False):
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token:
        sys.exit("SLACK_BOT_TOKEN not set (install the app, then export the xoxb- token).")

    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    client = WebClient(token=token)

    # Map existing channels once.
    existing: dict[str, str] = {}
    cursor = None
    while True:
        resp = client.conversations_list(types="public_channel", limit=200, cursor=cursor)
        for ch in resp["channels"]:
            existing[ch["name"]] = ch["id"]
        cursor = resp.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    for name, topic in CORE_CHANNELS + week_channels():
        if name in existing:
            cid = existing[name]
            action = "exists"
        elif dry_run:
            print(f"  [DRY] would create #{name}")
            continue
        else:
            try:
                cid = client.conversations_create(name=name, is_private=False)["channel"]["id"]
                action = "created"
            except SlackApiError as e:
                print(f"  [ERROR] #{name}: {e.response['error']}")
                continue

        if dry_run:
            print(f"  [DRY] #{name} ({action}) -> set topic")
            continue

        try:
            client.conversations_join(channel=cid)
        except SlackApiError:
            pass
        try:
            client.conversations_setTopic(channel=cid, topic=topic)
        except SlackApiError as e:
            print(f"  [warn] topic #{name}: {e.response['error']}")

        # Link the channel to its Google Drive folder (idempotent bookmark).
        m = re.match(r"week-(\d+)$", name)
        drive_url = (C.drive_week_url(int(m.group(1))) if m
                     else C.drive_folder_url(C.DRIVE_ROOT_FOLDER_ID) if name == "general"
                     else None)
        if drive_url:
            try:
                existing = {b.get("link") for b in
                            client.bookmarks_list(channel_id=cid).get("bookmarks", [])}
                if drive_url not in existing:
                    label = f"📁 {'Week ' + m.group(1) if m else 'Course'} materials (Drive)"
                    client.bookmarks_add(channel_id=cid, title=label, type="link", link=drive_url)
                    print(f"  #{name:<16} + Drive bookmark")
            except SlackApiError as e:
                print(f"  [warn] bookmark #{name}: {e.response['error']}")

        print(f"  #{name:<16} {action:<8} {cid}")


def main():
    ap = argparse.ArgumentParser(description="Provision per-week Slack channels")
    ap.add_argument("--dry-run", action="store_true")
    provision(ap.parse_args().dry_run)


if __name__ == "__main__":
    main()
