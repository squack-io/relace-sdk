"""
Chat log and Git-like operations: chat listing, pull, checkout.

ENV:
  RELACE_BASE_URL
  RELACE_API_KEY
  REPO_ID
  CHECKOUT_SHA  (optional) commit to checkout
"""

from __future__ import annotations

import os
from uuid import UUID

from relace_agent_client import AuthenticatedClient
from relace_agent_client.api.default import (
    checkout_commit_repo_repo_id_checkout_patch,
    get_chat_log_repo_repo_id_chat_get,
    pull_remote_repo_repo_id_pull_patch,
)
from relace_agent_client.models import PagedResponseRepoLogItem, RepoCheckoutRequest, RepoInfo, RepoPullRequest

BASE_URL = os.getenv("RELACE_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("RELACE_API_KEY", "")
REPO_ID = os.getenv("REPO_ID", "")
CHECKOUT_SHA = os.getenv("CHECKOUT_SHA")


def get_client() -> AuthenticatedClient:
    if not API_KEY:
        raise SystemExit("RELACE_API_KEY is required")
    return AuthenticatedClient(base_url=BASE_URL, token=API_KEY)


def show_chat(repo_id: UUID) -> None:
    with get_client() as c:
        resp = get_chat_log_repo_repo_id_chat_get.sync_detailed(client=c, repo_id=repo_id)
    if isinstance(resp.parsed, PagedResponseRepoLogItem):
        for item in resp.parsed.items:
            print(item.timestamp, item.event_type)
    else:
        print("Failed to fetch chat:", resp.status_code)


def pull(repo_id: UUID) -> None:
    with get_client() as c:
        resp = pull_remote_repo_repo_id_pull_patch.sync_detailed(client=c, repo_id=repo_id, body=RepoPullRequest())
    if isinstance(resp.parsed, RepoInfo):
        print("Pulled. New head:", resp.parsed.repo_head)


def checkout(repo_id: UUID) -> None:
    sha = CHECKOUT_SHA
    if not sha:
        print("Set CHECKOUT_SHA to a commit hash to checkout a specific commit.")
        return
    with get_client() as c:
        resp = checkout_commit_repo_repo_id_checkout_patch.sync_detailed(
            client=c, repo_id=repo_id, body=RepoCheckoutRequest(repo_head=sha)
        )
    if isinstance(resp.parsed, RepoInfo):
        print("Checked out:", resp.parsed.repo_head)
    else:
        print("Checkout failed:", resp.status_code, resp.parsed)


def main():
    if not REPO_ID:
        raise SystemExit("REPO_ID env var is required")
    repo_id = UUID(REPO_ID)

    show_chat(repo_id)
    pull(repo_id)
    checkout(repo_id)


if __name__ == "__main__":
    main()
