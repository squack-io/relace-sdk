// Repo update (files/diff/git) and clone example
import createRelaceClient from '@relace-ai/agent-client'

const client = createRelaceClient({ apiKey: import.meta.env.RELACE_API_KEY })

;(async () => {
  let repo_id
  try {
    const { data: created } = await client.POST('/repo', {
      body: {
        source: {
          type: 'files',
          files: [{ filename: 'a.txt', content: 'A1\n' }],
        },
        metadata: { example: 'update-clone' },
      },
    })
    if (!created) {
      console.error('Failed to create repo')
      process.exit(1)
    }
    repo_id = created.repo_id

    // 1) Update via diff ops
    await client.POST('/repo/{repo_id}/update', {
      params: { path: { repo_id } },
      body: {
        source: {
          type: 'diff',
          operations: [
            { type: 'write', filename: 'b.txt', content: 'B1\n' },
            { type: 'rename', old_filename: 'a.txt', new_filename: 'a2.txt' },
          ],
        },
      },
    })

    // 2) Clone current working tree
    const { data: clone } = await client.GET('/repo/{repo_id}/clone', {
      params: { path: { repo_id } },
    })
    console.log('Cloned files:')
    for (const f of clone?.files ?? [])
      console.log(`- ${f.filename} (${f.content.length} bytes)`)
  } catch (e) {
    console.error(e)
    process.exit(1)
  } finally {
    if (repo_id)
      await client.DELETE('/repo/{repo_id}', { params: { path: { repo_id } } })
  }
})()
