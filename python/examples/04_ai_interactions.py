"""
AI interactions: run agent, ask question, retrieve relevant content.

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
    ask_question_repo_repo_id_ask_post,
    retrieve_relevant_content_repo_repo_id_retrieve_post,
    run_agent_repo_repo_id_agent_post,
)
from relace_agent_client.models import (
    RepoAgentRequest,
    RepoAgentRequestAgentInputs,
    RepoAskRequest,
    RepoAskResponse,
    RepoRetrieveRequest,
    RepoRetrieveResponse,
)

BASE_URL = os.getenv("RELACE_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("RELACE_API_KEY", "")
REPO_ID = os.getenv("REPO_ID", "")


def get_client() -> AuthenticatedClient:
    if not API_KEY:
        raise SystemExit("RELACE_API_KEY is required")
    return AuthenticatedClient(base_url=BASE_URL, token=API_KEY)


def run_agent(repo_id: UUID) -> None:
    inputs = RepoAgentRequestAgentInputs.from_dict({"task": "Add logging to main and write tests"})
    with get_client() as c:
        resp = run_agent_repo_repo_id_agent_post.sync_detailed(
            client=c, repo_id=repo_id, body=RepoAgentRequest(agent_name="code_maintainer", agent_inputs=inputs)
        )
    print("Agent response:", resp.parsed)


def ask(repo_id: UUID) -> None:
    with get_client() as c:
        resp = ask_question_repo_repo_id_ask_post.sync_detailed(
            client=c, repo_id=repo_id, body=RepoAskRequest(query="Where is the entry point?")
        )
    if isinstance(resp.parsed, RepoAskResponse):
        print("Answer:", resp.parsed.answer)


def retrieve(repo_id: UUID) -> None:
    with get_client() as c:
        resp = retrieve_relevant_content_repo_repo_id_retrieve_post.sync_detailed(
            client=c,
            repo_id=repo_id,
            body=RepoRetrieveRequest(query="authentication logic", include_content=True, score_threshold=0.4),
        )
    if isinstance(resp.parsed, RepoRetrieveResponse):
        for r in resp.parsed.results:
            print(f"{r.filename} (score={r.score})")


def main():
    if not REPO_ID:
        raise SystemExit("REPO_ID env var is required")
    repo_id = UUID(REPO_ID)

    run_agent(repo_id)
    ask(repo_id)
    retrieve(repo_id)


if __name__ == "__main__":
    main()
