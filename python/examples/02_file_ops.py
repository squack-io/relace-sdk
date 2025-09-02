"""
Basic file operations: upload, download, delete.

ENV:
  RELACE_BASE_URL
  RELACE_API_KEY
  REPO_ID  (UUID)

Usage:
  python 02_file_ops.py upload path/to/local.txt repo/path.txt
  python 02_file_ops.py download repo/path.txt
  python 02_file_ops.py delete repo/path.txt
"""

from __future__ import annotations

import os
import sys
from io import BytesIO
from uuid import UUID

from relace_agent_client import AuthenticatedClient
from relace_agent_client.api.default import (
    delete_file,
    download_file,
    upload_file,
)
from relace_agent_client.models import RepoInfo
from relace_agent_client.types import File as UploadFile

BASE_URL = os.getenv("RELACE_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("RELACE_API_KEY", "")
REPO_ID = os.getenv("REPO_ID", "")


def client() -> AuthenticatedClient:
    if not API_KEY:
        raise SystemExit("RELACE_API_KEY is required")
    return AuthenticatedClient(base_url=BASE_URL, token=API_KEY)


def cmd_upload(repo_id: UUID, local_path: str, repo_path: str) -> None:
    with open(local_path, "rb") as f:
        body = UploadFile(payload=BytesIO(f.read()), file_name=os.path.basename(local_path))
    with client() as c:
        resp = upload_file.sync_detailed(client=c, repo_id=repo_id, file_path=repo_path, body=body)
    if isinstance(resp.parsed, RepoInfo):
        print("Uploaded. New head:", resp.parsed.repo_head)
    else:
        print("Upload failed:", resp.status_code, resp.parsed)


def cmd_download(repo_id: UUID, repo_path: str) -> None:
    with client() as c:
        data = download_file.sync(client=c, repo_id=repo_id, file_path=repo_path)
    print(data)


def cmd_delete(repo_id: UUID, repo_path: str) -> None:
    with client() as c:
        resp = delete_file.sync_detailed(client=c, repo_id=repo_id, file_path=repo_path)
    if isinstance(resp.parsed, RepoInfo):
        print("Deleted. New head:", resp.parsed.repo_head)
    else:
        print("Delete failed:", resp.status_code, resp.parsed)


def main(argv: list[str]) -> None:
    if not REPO_ID:
        raise SystemExit("REPO_ID env var is required")
    repo_id = UUID(REPO_ID)

    if len(argv) < 2:
        print(__doc__)
        raise SystemExit(2)

    action = argv[1]
    if action == "upload" and len(argv) >= 4:
        cmd_upload(repo_id, argv[2], argv[3])
    elif action == "download" and len(argv) >= 3:
        cmd_download(repo_id, argv[2])
    elif action == "delete" and len(argv) >= 3:
        cmd_delete(repo_id, argv[2])
    else:
        print(__doc__)
        raise SystemExit(2)


if __name__ == "__main__":
    main(sys.argv)
