# @relace-ai/typescript-sdk

TypeScript client SDK for the Relace Agent API.

## Install

```sh
pnpm add @relace-ai/typescript-sdk
# or
npm i @relace-ai/typescript-sdk
# or
yarn add @relace-ai/typescript-sdk
```

## Usage

```ts
import { createRelaceClient } from "@relace-ai/typescript-sdk"

const client = createRelaceClient({
  baseUrl: "https://api.relace.ai",
  apiKey: process.env.RELACE_API_KEY!,
})

// Example: list repos
const res = await client.GET("/repo")
if (res.error) throw new Error(JSON.stringify(res.error))
console.log(res.data)
```

- All routes are typed from the OpenAPI spec.
- Pass a custom `fetch` if you need to use a polyfill or instrumentation.

## Node compatibility

- ESM-only package. Requires Node >= 18.

## Development

- Types are generated at the repo root via `pnpm run generate:typescript`.
- Build:

```sh
pnpm -F @relace-ai/typescript-sdk build
```

## License

ISC
