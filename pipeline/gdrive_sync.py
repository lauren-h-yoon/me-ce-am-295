#!/usr/bin/env python3
"""
Sync the course Google Drive folder -> materials/  (Drive = source of truth).

The folder "ME/CE/AM 295 (Caltech)" (config.DRIVE_ROOT_FOLDER_ID, owned by
daraio@caltech.edu) mirrors the local materials/ layout (Week N/, Study Guides/,
References/). This pulls it down so the normal pipeline stays current with what
the professor/TAs edit in Drive:

    gdrive_sync  ->  materials/  ->  pipeline.sync  ->  content/  ->  week agent

Auth (runtime, on the bot host — separate from the claude.ai Drive connection
used during setup): a Google **service account** with read access to the folder.
Share the Drive folder with the service account's email, then:

    pip install google-api-python-client google-auth
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json
    python -m pipeline.gdrive_sync                # incremental (by modifiedTime)

Excludes the same folders as the local pipeline (Archive, TA & Setup).
State is kept in content/.gdrive_state.json for incrementality.
"""
from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

from pipeline import config as C

STATE_PATH = C.CONTENT_DIR / ".gdrive_state.json"

# Google-native types must be exported; everything else downloads as-is.
EXPORT_MIME = {
    "application/vnd.google-apps.document":
        ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx"),
    "application/vnd.google-apps.presentation":
        ("application/vnd.openxmlformats-officedocument.presentationml.presentation", ".pptx"),
    "application/vnd.google-apps.spreadsheet":
        ("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx"),
}
FOLDER_MIME = "application/vnd.google-apps.folder"


def _service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(
        __import__("os").environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    return build("drive", "v3", credentials=creds)


def _list_children(svc, folder_id: str) -> list[dict]:
    out, token = [], None
    while True:
        resp = svc.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id,name,mimeType,modifiedTime,md5Checksum)",
            pageToken=token, pageSize=1000,
        ).execute()
        out.extend(resp.get("files", []))
        token = resp.get("nextPageToken")
        if not token:
            break
    return out


def _download(svc, f: dict, dest: Path):
    from googleapiclient.http import MediaIoBaseDownload
    export = EXPORT_MIME.get(f["mimeType"])
    if export:
        mime, ext = export
        if not dest.name.endswith(ext):
            dest = dest.with_suffix(ext)
        req = svc.files().export_media(fileId=f["id"], mimeType=mime)
    else:
        req = svc.files().get_media(fileId=f["id"])
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, req)
    done = False
    while not done:
        _, done = dl.next_chunk()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(buf.getvalue())
    return dest


def sync(dest_root: Path, dry_run: bool = False) -> dict:
    svc = _service()
    state = json.loads(STATE_PATH.read_text()) if STATE_PATH.exists() else {}
    new_state, stats = {}, {"downloaded": 0, "skipped": 0, "folders": 0}

    def walk(folder_id: str, rel: Path):
        for f in _list_children(svc, folder_id):
            name = f["name"]
            if f["mimeType"] == FOLDER_MIME:
                if name in C.EXCLUDE_DIRS:
                    continue
                stats["folders"] += 1
                walk(f["id"], rel / name)
                continue
            key = f["id"]
            token = f.get("md5Checksum") or f.get("modifiedTime")
            new_state[key] = token
            target = dest_root / rel / name
            if state.get(key) == token and target.exists():
                stats["skipped"] += 1
                continue
            if dry_run:
                print(f"  [PULL] {rel / name}")
            else:
                out = _download(svc, f, target)
                print(f"  [PULL] {rel / name} -> {out.relative_to(C.REPO_ROOT)}")
            stats["downloaded"] += 1

    print(f"Drive sync: {C.DRIVE_ROOT_FOLDER_ID} -> {dest_root}")
    walk(C.DRIVE_ROOT_FOLDER_ID, Path("."))
    if not dry_run:
        STATE_PATH.write_text(json.dumps(new_state, indent=2))
    print(f"  downloaded {stats['downloaded']}, skipped {stats['skipped']}, "
          f"folders {stats['folders']}")
    print("  next: python -m pipeline.sync  (normalize -> content/)")
    return stats


def main():
    ap = argparse.ArgumentParser(description="Pull the course Google Drive -> materials/")
    ap.add_argument("--dest", default=str(C.MATERIALS_DIR), help="destination root")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    sync(Path(args.dest), dry_run=args.dry_run)


if __name__ == "__main__":
    main()
