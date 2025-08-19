# Relace SDK Monorepo

This repository contains the SDKs for interacting with the Relace API, generated from an OpenAPI specification. It's a monorepo containing both TypeScript and Python SDKs.

## Monorepo Structure

- `openapi.json`: The OpenAPI specification file that defines the API.
- `python/`: Contains the Python SDK.
- `typescript/`: Contains the TypeScript SDK.
- `.github/workflows/`: Contains the GitHub Actions workflows for CI/CD.

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v20 or higher)
- [pnpm](https://pnpm.io/) (v10.12.1 or higher)
- [Python](https://www.python.org/) (v3.11 or higher)
- [uv](https://docs.astral.sh/uv/guides/install-python/)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/squack-io/relace-sdk.git
    cd relace-sdk
    ```

2.  **Install dependencies:**
    This command will install dependencies for both the TypeScript and Python packages.
    ```bash
    pnpm install -w
    ```

## Development

### Code Generation

The SDKs are generated from the `openapi.json` file. If you make changes to the OpenAPI spec, you'll need to regenerate the clients.

- **TypeScript:**

  ```bash
  pnpm run generate:typescript
  ```

- **Python:**
  ```bash
  pnpm run generate:python
  ```

### Linting

To ensure code quality, run the linters:

- **TypeScript:**

  ```bash
  pnpm run lint:typescript
  ```

- **Python:**

  ```bash
  pnpm run lint:python
  ```

- **All:**
  ```bash
  pnpm run lint
  ```

## Publishing

Both SDKs use tag-based publishing in CI with version validation against package metadata.

### Tag formats (CI triggers)

- TypeScript (npm): `typescript-sdk-v<version>` (e.g., `typescript-sdk-v0.1.0`)
- Python (PyPI): `python-sdk-v<version>` (e.g., `python-sdk-v0.1.0`)

### Release steps (CI)

1. Bump version in the package:

- TypeScript: edit `typescript/package.json` "version"
- Python: edit `python/pyproject.toml` `[project].version`

2. Commit and push.
3. Create and push a tag (using the formats above). CI will:

- Regenerate clients from `openapi.json` (TS), build, and publish.
- Validate the tag version matches the package version before publishing.

Required repo secrets for CI:

- npm: `NPM_TOKEN` (npm automation token)
- PyPI: `PYPI_TOKEN` (project token)

### Local publishing (advanced)

TypeScript (npm):

1. `pnpm install -w`
2. `pnpm run generate:typescript`
3. `pnpm -F @relace-ai/typescript-sdk build`
4. From `typescript/`: `npm publish --access public` (requires `npm login` and proper 2FA setup, if enabled)

Python (PyPI):

1. Ensure `uv` is installed
2. From `python/`: `uv build`
3. From `python/`: `uv publish --token <pypi_token>`

Note

- Generated files should not be edited by hand. To change types/endpoints, edit `openapi.json` then rerun the generators.
