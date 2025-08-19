"""
Create a repository from files or a Git URL.

ENV:
  RELACE_BASE_URL: API base URL (default: https://api.example.com)
  RELACE_API_KEY:  Bearer token

Usage:
  python 01_create_repo.py files
  python 01_create_repo.py git https://github.com/org/repo.git [branch]
"""

from __future__ import annotations

import os
import sys

from relace_agent_client import AuthenticatedClient
from relace_agent_client.api.default import create_repo_repo_post
from relace_agent_client.models import (
    File as ModelFile,
)
from relace_agent_client.models import (
    RepoCreateFilesSource,
    RepoCreateGitSource,
    RepoCreateRequest,
    RepoInfo,
)


def get_client() -> AuthenticatedClient:
    base_url = os.getenv("RELACE_BASE_URL", "https://api.example.com")
    api_key = os.getenv("RELACE_API_KEY", "")
    if not api_key:
        raise SystemExit("RELACE_API_KEY is required")
    return AuthenticatedClient(base_url=base_url, token=api_key)


def create_from_files(client: AuthenticatedClient) -> None:
    files = [
        ModelFile(filename="README.md", content="# New Repo\n"),
        ModelFile(filename="src/main.py", content="print('hello from relace')\n"),
    ]
    req = RepoCreateRequest(source=RepoCreateFilesSource(type_="files", files=files))
    with client as c:
        resp = create_repo_repo_post.sync_detailed(client=c, body=req)
    if isinstance(resp.parsed, RepoInfo):
        print("Created repo:", resp.parsed.repo_id, "head:", resp.parsed.repo_head)
    else:
        print("Create failed:", resp.status_code, resp.parsed)


def create_from_git(client: AuthenticatedClient, url: str, branch: str | None) -> None:
    req = RepoCreateRequest(source=RepoCreateGitSource(type_="git", url=url, branch=branch))
    with client as c:
        resp = create_repo_repo_post.sync_detailed(client=c, body=req)
    if isinstance(resp.parsed, RepoInfo):
        print("Created repo from git:", resp.parsed.repo_id, "head:", resp.parsed.repo_head)
    else:
        print("Create from git failed:", resp.status_code, resp.parsed)


def main(argv: list[str]) -> None:
    if len(argv) < 2 or argv[1] not in {"files", "git"}:
        print(__doc__)
        raise SystemExit(2)

    client = get_client()
    mode = argv[1]
    if mode == "files":
        create_from_files(client)
    else:
        if len(argv) < 3:
            print("Provide git URL. Optionally a branch.")
            raise SystemExit(2)
        url = argv[2]
        branch = argv[3] if len(argv) > 3 else None
        create_from_git(client, url, branch)


if __name__ == "__main__":
    main(sys.argv)
