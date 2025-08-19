import { afterAll, describe, expect, it } from "vitest"
import createRelaceClient from "../src"

describe('Repo CRUD integration', () => {
  const client = createRelaceClient({ apiKey: import.meta.env.RELACE_API_KEY })

  let repoId: string | undefined

  afterAll(async () => {
    if (!repoId) return
    try {
      await client.DELETE('/repo/{repo_id}', {
        params: { path: { repo_id: repoId } },
      })
    } catch {
      // ignore cleanup errors
    }
  })

  it('creates a repo (source: files) and returns RepoInfo', async () => {
    const createBody = {
      source: {
        type: 'files' as const,
        files: [
          { filename: 'README.md', content: '# Relace SDK Test\n' },
          { filename: 'src/index.ts', content: 'export const ok = true;\n' },
        ],
      },
      metadata: { test_suite: 'repo.crud.int' },
    }

    const { data, error, response } = await client.POST('/repo', {
      body: createBody,
    })

    expect(error).toBeUndefined()
    expect(response.status).toBeGreaterThanOrEqual(200)
    expect(response.status).toBeLessThan(300)
    expect(data).toBeDefined()
    expect(data!.repo_id).toMatch(/[0-9a-fA-F-]{36}/)
    expect(typeof data!.repo_head).toBe('string')

    repoId = data!.repo_id
  }, 60_000)

  it('gets repo metadata by id', async () => {
    expect(repoId).toBeDefined()
    const { data, error, response } = await client.GET('/repo/{repo_id}', {
      params: { path: { repo_id: repoId! } },
    })

    expect(error).toBeUndefined()
    expect(response.status).toBe(200)
    expect(data).toBeDefined()
    expect(data!.repo_id).toBe(repoId)
    expect(typeof data!.created_at).toBe('string')
  }, 60_000)

  it('lists repos and includes the created repo', async () => {
    const { data, error, response } = await client.GET('/repo', {})

    expect(error).toBeUndefined()
    expect(response.status).toBe(200)
    expect(data).toBeDefined()
    expect(Array.isArray(data!.items)).toBe(true)
    expect(data!.items.length).toBeGreaterThan(0)
    expect(data!.items.some((m) => m.repo_id === repoId)).toBe(true)
  }, 60_000)

  it('deletes the repo', async () => {
    const { error, response } = await client.DELETE('/repo/{repo_id}', {
      params: { path: { repo_id: repoId! } },
    })

    expect(error).toBeUndefined()
    expect(response.status).toBe(204)

    // mark as cleaned up to avoid afterAll double delete noise
    repoId = undefined
  }, 60_000)
})
