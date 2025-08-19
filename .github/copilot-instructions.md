# Relace SDK – AI working notes

Monorepo with generated SDKs for the Relace Agent API. Use codegen; don’t hand‑edit generated files.

## Big picture

- Canonical source: `openapi.json` at repo root → drives both SDKs.
- Packages:
  - `typescript/` — client on `openapi-fetch`. Factory: `typescript/src/index.ts` (`createRelaceClient`). Types in `typescript/src/relace.schema.ts` (generated).
  - `python/` — client from `openapi-python-client` under `python/relace_agent_client/` (generated `models/` + `api/default/`).
- Auth & base URL:
  - `Authorization: Bearer <RELACE_API_KEY>` on every request.
  - Base URL configurable (TS via `createRelaceClient({ baseUrl, apiKey })`; PY via `RELACE_BASE_URL`).

## Generated files (do not edit)

- TS: `typescript/src/relace.schema.ts`.
- PY: `python/relace_agent_client/models/**`, `python/relace_agent_client/api/**`.
- To change shapes/endpoints: modify `openapi.json` → regenerate.

## Codegen & lint (run at repo root)

- TS types: `pnpm run generate:typescript` (also rewrites `@description` → `@remarks`).
- PY client: `pnpm run generate:python` (uses `uvx openapi-python-client` then `ruff`).
- Lint: `pnpm run lint:typescript` and `pnpm run lint:python` (prefer these over the aggregate).

## TypeScript SDK

- ESM-only; entry `typescript/src/index.ts`.
- Package name in code: `@relace-ai/agent-client` (see `typescript/package.json`). The README title `@relace-ai/typescript-sdk` is legacy.
- Example (typed params):
  ```ts
  import createRelaceClient from '@relace-ai/agent-client'
  const client = createRelaceClient({ apiKey: import.meta.env.RELACE_API_KEY })
  const { data, error } = await client.GET('/repo/{repo_id}', {
    params: { path: { repo_id: '<uuid>' } },
  })
  ```
- Build: `pnpm -F @relace-ai/typescript-sdk build`; Test: `pnpm -F @relace-ai/typescript-sdk test` (needs `RELACE_API_KEY`).
- Examples: `typescript/examples/*.mjs` (e.g., `05_agent_stream_sse.mjs` for SSE).

## Python SDK

- Package: `relace_agent_client` with sync/async endpoint variants.
- Examples: `python/examples/` (e.g., `01_create_repo.py` supports files/git sources).
- Local build/publish: `uv build`, `uv publish` (see `python/README.md`).

## Conventions

- Use typed `client.GET/POST/DELETE` with `params.path/query` and `body`.
- Required env: `RELACE_API_KEY`; optional: `RELACE_BASE_URL` (Python default is `https://api.example.com`).
- Long ops (Run Agent) stream SSE server-side; plan custom fetch/event handling when building UIs.

## Pointers

- Schema/types: `typescript/src/relace.schema.ts`.
- TS factory: `typescript/src/index.ts`; tests: `typescript/tests/` (`repo.crud.int.test.ts`).
- PY surface: `python/relace_agent_client/`.
- OpenAPI: `openapi.json` at repo root.
