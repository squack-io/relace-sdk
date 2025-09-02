"""
Bulk updates (files, diff, git) and clone.

ENV:
  RELACE_BASE_URL
  RELACE_API_KEY
  REPO_ID
"""

from __future__ import annotations

import os
from uuid import UUID

from relace_agent_client import AuthenticatedClient
from relace_agent_client.api.default import (
    clone_repo,
    update_repo_contents,
)
from relace_agent_client.models import (
    File as ModelFile,
)
from relace_agent_client.models import (
    FileDeleteOperation,
    FileRenameOperation,
    FileWriteOperation,
    RepoCloneResponse,
    RepoInfo,
    RepoUpdateDiff,
    RepoUpdateFiles,
    RepoUpdateGit,
    RepoUpdateRequest,
)

BASE_URL = os.getenv("RELACE_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("RELACE_API_KEY", "")
REPO_ID = os.getenv("REPO_ID", "")


def get_client() -> AuthenticatedClient:
    if not API_KEY:
        raise SystemExit("RELACE_API_KEY is required")
    return AuthenticatedClient(base_url=BASE_URL, token=API_KEY)


def update_files(repo_id: UUID) -> None:
    update = RepoUpdateRequest(
        source=RepoUpdateFiles(type_="files", files=[ModelFile(filename="hello.txt", content="hi")])
    )
    with get_client() as c:
        resp = update_repo_contents.sync_detailed(client=c, repo_id=repo_id, body=update)
    if isinstance(resp.parsed, RepoInfo):
        print("Files updated, head:", resp.parsed.repo_head)


def update_diff(repo_id: UUID) -> None:
    ops = RepoUpdateDiff(
        type_="diff",
        operations=[
            FileWriteOperation(type_="write", filename="src/util.py", content="def mul(a,b): return a*b\n"),
            FileRenameOperation(type_="rename", old_filename="hello.txt", new_filename="greeting.txt"),
            FileDeleteOperation(type_="delete", filename="obsolete.txt"),
        ],
    )
    req = RepoUpdateRequest(source=ops)
    with get_client() as c:
        resp = update_repo_contents.sync_detailed(client=c, repo_id=repo_id, body=req)
    if isinstance(resp.parsed, RepoInfo):
        print("Diff applied, head:", resp.parsed.repo_head)


def update_git(repo_id: UUID, url: str, branch: str | None = None) -> None:
    req = RepoUpdateRequest(source=RepoUpdateGit(type_="git", url=url, branch=branch))
    with get_client() as c:
        resp = update_repo_contents.sync_detailed(client=c, repo_id=repo_id, body=req)
    if isinstance(resp.parsed, RepoInfo):
        print("Git source applied, head:", resp.parsed.repo_head)


def clone(repo_id: UUID) -> None:
    with get_client() as c:
        resp = clone_repo.sync_detailed(client=c, repo_id=repo_id)
    if isinstance(resp.parsed, RepoCloneResponse):
        count = len(resp.parsed.files or [])
        print("Cloned files:", count)
        for f in resp.parsed.files or []:
            print("-", f.filename, len(f.content))


def main():
    if not REPO_ID:
        raise SystemExit("REPO_ID env var is required")
    repo_id = UUID(REPO_ID)

    update_files(repo_id)
    update_diff(repo_id)
    # update_git(repo_id, url="https://github.com/org/repo.git", branch="main")  # optional
    clone(repo_id)


if __name__ == "__main__":
    main()
