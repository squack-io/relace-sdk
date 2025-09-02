import type { paths } from './relace.schema'
import createFetchClient from 'openapi-fetch'

export interface RelaceApiClientConfig {
  baseUrl?: string
  apiKey: string
  fetch?: typeof globalThis.fetch
  /** Additional headers to send on every request. Authorization will be set from apiKey. */
  headers?: Record<string, string>
}

/**
 * Create a typed Relace API client using openapi-fetch
 * - Adds Authorization header
 * - Allows custom fetch implementation (Node, polyfills, etc.)
 */
export const createRelaceClient = ({
  baseUrl = 'https://api.relace.run/v1/',
  apiKey,
  fetch = globalThis.fetch,
  headers,
}: RelaceApiClientConfig) =>
  createFetchClient<paths>({
    baseUrl,
    fetch,
    headers: {
      ...headers,
      Authorization: `Bearer ${apiKey}`,
    },
  })

export default createRelaceClient

// Re-export generated schema types for convenience
export type { paths as RelacePaths } from './relace.schema'
export type { components as RelaceComponents } from './relace.schema'
export type { operations as RelaceOperations } from './relace.schema'
