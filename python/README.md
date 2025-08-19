# relace-agent-client

Python SDK for the Relace Agent API — manage repos, files, git-like ops, and AI interactions.

The client is generated with openapi-python-client and exposes typed models and endpoint helpers.

## Quickstart

```python
import os
from uuid import UUID

from relace_agent_client import AuthenticatedClient

BASE_URL = os.getenv("RELACE_BASE_URL", "https://api.example.com")
API_KEY = os.getenv("RELACE_API_KEY", "<YOUR_API_KEY>")

client = AuthenticatedClient(base_url=BASE_URL, token=API_KEY)
```

- Use context managers for connection reuse:

```python
from relace_agent_client.api.default import list_repo_metadata_repo_get

with client as c:
    repos = list_repo_metadata_repo_get.sync(client=c)
    print(repos)
```

Notes

- All endpoints have sync/sync_detailed/asyncio/asyncio_detailed variants.
- Most operations return `RepoInfo` with `repo_id` and current `repo_head` on success.
- Authentication uses an HTTP Bearer token.

## Create a repository

Create from a Git URL:

```python
from relace_agent_client.api.default import create_repo_repo_post
from relace_agent_client.models import RepoCreateRequest, RepoCreateGitSource

with client as c:
    req = RepoCreateRequest(
        source=RepoCreateGitSource(type_="git", url="https://github.com/org/repo.git", branch="main")
    )
    created = create_repo_repo_post.sync(client=c, body=req)
    repo_id = created.repo_id
    print("Created repo:", repo_id, created.repo_head)
```

Create from in-memory files:

```python
from relace_agent_client.api.default import create_repo_repo_post
from relace_agent_client.models import RepoCreateRequest, RepoCreateFilesSource, File as ModelFile

files = [
    ModelFile(filename="README.md", content="# Hello\n"),
    ModelFile(filename="src/app.py", content="print('hi')\n"),
]

with client as c:
    req = RepoCreateRequest(source=RepoCreateFilesSource(type_="files", files=files))
    info = create_repo_repo_post.sync(client=c, body=req)
    repo_id = info.repo_id
```

## List and get metadata

```python
from relace_agent_client.api.default import list_repo_metadata_repo_get, get_repo_metadata_repo_repo_id_get

with client as c:
    page = list_repo_metadata_repo_get.sync(client=c)
    for meta in (page.items or []):
        print(meta.repo_id, meta.created_at)

    md = get_repo_metadata_repo_repo_id_get.sync(client=c, repo_id=repo_id)
    print(md)
```

## File operations

Upload/overwrite a file (auto-committed):

```python
from io import BytesIO
from relace_agent_client.api.default import upload_file_repo_repo_id_file_file_path_put
from relace_agent_client.types import File as UploadFile

content = BytesIO(b"print('updated')\n")

with client as c:
    info = upload_file_repo_repo_id_file_file_path_put.sync(
        client=c,
        repo_id=repo_id,
        file_path="src/app.py",
        body=UploadFile(payload=content, file_name="app.py", mime_type="text/x-python"),
    )
    print(info.repo_head)
```

Download a file:

```python
from relace_agent_client.api.default import download_file_repo_repo_id_file_file_path_get

with client as c:
    data = download_file_repo_repo_id_file_file_path_get.sync(
        client=c, repo_id=repo_id, file_path="src/app.py"
    )
    print(data)
```

Delete a file:

```python
from relace_agent_client.api.default import delete_file_repo_repo_id_file_file_path_delete

with client as c:
    info = delete_file_repo_repo_id_file_file_path_delete.sync(
        client=c, repo_id=repo_id, file_path="README.md"
    )
    print(info.repo_head)
```

## Bulk updates (powerful)

Replace files in bulk:

```python
from relace_agent_client.api.default import update_repo_contents_repo_repo_id_update_post
from relace_agent_client.models import RepoUpdateRequest, RepoUpdateFiles, File as ModelFile

update = RepoUpdateRequest(
    source=RepoUpdateFiles(type_="files", files=[ModelFile(filename="new.txt", content="hello")])
)

with client as c:
    info = update_repo_contents_repo_repo_id_update_post.sync(client=c, repo_id=repo_id, body=update)
```

Apply a diff of operations:

```python
from relace_agent_client.models import RepoUpdateRequest, RepoUpdateDiff, FileWriteOperation, FileRenameOperation, FileDeleteOperation
from relace_agent_client.api.default import update_repo_contents_repo_repo_id_update_post

ops = RepoUpdateDiff(
    type_="diff",
    operations=[
        FileWriteOperation(type_="write", filename="src/util.py", content="def add(a,b): return a+b\n"),
        FileRenameOperation(type_="rename", old_filename="src/app.py", new_filename="src/main.py"),
        FileDeleteOperation(type_="delete", filename="obsolete.txt"),
    ],
)
req = RepoUpdateRequest(source=ops)

with client as c:
    info = update_repo_contents_repo_repo_id_update_post.sync(client=c, repo_id=repo_id, body=req)
```

Overwrite from a new Git source:

```python
from relace_agent_client.models import RepoUpdateRequest, RepoUpdateGit
from relace_agent_client.api.default import update_repo_contents_repo_repo_id_update_post

req = RepoUpdateRequest(source=RepoUpdateGit(type_="git", url="https://github.com/org/another.git", branch="main"))

with client as c:
    info = update_repo_contents_repo_repo_id_update_post.sync(client=c, repo_id=repo_id, body=req)
```

## Clone repository (get all files)

```python
from relace_agent_client.api.default import clone_repo_repo_repo_id_clone_get

with client as c:
    clone = clone_repo_repo_repo_id_clone_get.sync(client=c, repo_id=repo_id)
    for f in (clone.files or []):
        print(f.filename, len(f.content))
```

## Git-like operations

Pull from remote:

```python
from relace_agent_client.api.default import pull_remote_repo_repo_id_pull_patch
from relace_agent_client.models import RepoPullRequest

with client as c:
    info = pull_remote_repo_repo_id_pull_patch.sync(client=c, repo_id=repo_id, body=RepoPullRequest())
    print(info.repo_head)
```

Checkout a specific commit:

```python
from relace_agent_client.api.default import checkout_commit_repo_repo_id_checkout_patch
from relace_agent_client.models import RepoCheckoutRequest

target_hash = "<commit-sha>"
with client as c:
    info = checkout_commit_repo_repo_id_checkout_patch.sync(
        client=c, repo_id=repo_id, body=RepoCheckoutRequest(repo_head=target_hash)
    )
```

## AI interactions

Run an agent (SSE events are emitted server-side during processing):

```python
from relace_agent_client.api.default import run_agent_repo_repo_id_agent_post
from relace_agent_client.models import RepoAgentRequest, RepoAgentRequestAgentInputs

inputs = RepoAgentRequestAgentInputs.from_dict({
    "task": "Refactor utils and add unit tests",
    "priority": "high",
})

with client as c:
    result = run_agent_repo_repo_id_agent_post.sync(
        client=c,
        repo_id=repo_id,
        body=RepoAgentRequest(agent_name="code_maintainer", agent_inputs=inputs),
    )
    print(result)
```

Ask a question about the repo:

```python
from relace_agent_client.api.default import ask_question_repo_repo_id_ask_post
from relace_agent_client.models import RepoAskRequest

with client as c:
    res = ask_question_repo_repo_id_ask_post.sync(
        client=c, repo_id=repo_id, body=RepoAskRequest(query="Where does the app start?")
    )
    print(res.answer)
```

Retrieve relevant content:

```python
from relace_agent_client.api.default import retrieve_relevant_content_repo_repo_id_retrieve_post
from relace_agent_client.models import RepoRetrieveRequest

with client as c:
    r = retrieve_relevant_content_repo_repo_id_retrieve_post.sync(
        client=c,
        repo_id=repo_id,
        body=RepoRetrieveRequest(query="authentication logic", include_content=True, score_threshold=0.4),
    )
    for item in r.results:
        print(item.filename, item.score)
```

View the chat/event log:

```python
from relace_agent_client.api.default import get_chat_log_repo_repo_id_chat_get

with client as c:
    page = get_chat_log_repo_repo_id_chat_get.sync(client=c, repo_id=repo_id)
    print(page)
```

## Delete a repository

```python
from relace_agent_client.api.default import delete_repo_repo_repo_id_delete

with client as c:
    delete_repo_repo_repo_id_delete.sync(client=c, repo_id=repo_id)
```

## Async usage

Every endpoint has `asyncio` and `asyncio_detailed` variants:

```python
import asyncio
from relace_agent_client import AuthenticatedClient
from relace_agent_client.api.default import list_repo_metadata_repo_get

async def main():
    async with AuthenticatedClient(base_url=BASE_URL, token=API_KEY) as c:
        page = await list_repo_metadata_repo_get.asyncio(client=c)
        print(page)

asyncio.run(main())
```

## Examples

See runnable scripts in `python/examples/`:

- `01_create_repo.py` — create from files or Git
- `02_file_ops.py` — upload, download, delete
- `03_update_and_clone.py` — bulk update (files/diff/git) and clone
- `04_ai_interactions.py` — run agent, ask, retrieve
- `05_chat_and_git.py` — chat log, pull, checkout

## TLS/HTTPX customization

```python
from relace_agent_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url="https://internal-api.example.com",
    token=API_KEY,
    verify_ssl="/path/to/ca-bundle.pem",  # or False (not recommended)
)

# Access underlying httpx clients with:
# client.get_httpx_client() / client.get_async_httpx_client()
```

## Building / publishing this package

This project uses [uv](https://github.com/astral-sh/uv) to manage dependencies and packaging. Basics:

1. Update metadata in `pyproject.toml` (authors, version).
2. Private index: https://docs.astral.sh/uv/guides/integration/alternative-indexes/
3. Build: `uv build` (sdist + wheel).
4. Publish: `uv publish` (configure your index as needed).

Install into another project without publishing:

1. If that project uses uv: `uv add <path-to-this-client>`
2. If not using uv:
   - Build a wheel: `uv build --wheel`
   - Install: `pip install <path-to-wheel>`
