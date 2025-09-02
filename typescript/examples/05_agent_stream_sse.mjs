// Agent run with SSE streaming: prints events as they arrive
// Note: The SDK method returns a standard fetch response content type unknown.
// We'll use the underlying fetch directly to read the SSE stream for this endpoint.

import createRelaceClient from '@relace-ai/agent-client'

const client = createRelaceClient({ apiKey: import.meta.env.RELACE_API_KEY })

// Helper to open SSE via fetch
/**
 * @param {string} repo_id
 * @param {{ agent_name: string, agent_inputs: Record<string,string>, overrides: any }} body
 */
async function runAgentStream(repo_id, body) {
  const res = await fetch(
    new URL(`/repo/${repo_id}/agent`, import.meta.env.RELACE_BASE_URL),
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${import.meta.env.RELACE_API_KEY}`,
        'Content-Type': 'application/json',
        Accept: 'text/event-stream',
      },
      body: JSON.stringify(body),
    },
  )
  if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`)

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  console.log('SSE stream opened. Events:')
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    let idx
    while ((idx = buffer.indexOf('\n\n')) !== -1) {
      const chunk = buffer.slice(0, idx)
      buffer = buffer.slice(idx + 2)
      for (const line of chunk.split('\n')) {
        const trimmed = line.trim()
        if (!trimmed) continue
        if (trimmed.startsWith('data:')) {
          const payload = trimmed.slice(5).trim()
          try {
            const evt = JSON.parse(payload)
            console.log('event:', evt)
          } catch {
            console.log('data:', payload)
          }
        }
      }
    }
  }
  console.log('SSE stream closed.')
}

;(async () => {
  let repo_id
  try {
    const { data: created } = await client.POST('/repo', {
      body: {
        source: {
          type: 'files',
          files: [{ filename: 'README.md', content: '# Agent demo\n' }],
        },
        metadata: { example: 'agent-sse' },
      },
    })
    if (!created) {
      console.error('Failed to create repo')
      process.exit(1)
    }
    repo_id = created.repo_id

    await runAgentStream(repo_id, {
      agent_name: process.env.RELACE_AGENT_NAME || 'default',
      agent_inputs: { goal: 'Say hello and write a file' },
      overrides: null,
    })
  } catch (e) {
    console.error(e)
    process.exit(1)
  } finally {
    if (repo_id)
      await client.DELETE('/repo/{repo_id}', { params: { path: { repo_id } } })
  }
})()
