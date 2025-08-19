// File operations example: upload, download, delete a file via single-file endpoints.
import createRelaceClient from '@relace-ai/agent-client'

const client = createRelaceClient({ apiKey: import.meta.env.RELACE_API_KEY })

;(async () => {
  try {
    // Create empty repo
    const { data: created } = await client.POST('/repo', {
      body: { metadata: { example: 'file-ops' } },
    })

    if (!created) {
      console.error('Failed to create repo')
      process.exit(1)
    }

    const repo_id = created.repo_id
    const file_path = 'hello.txt'

    // Upload/overwrite a file (auto-committed)
    await client.PUT('/repo/{repo_id}/file/{file_path}', {
      params: { path: { file_path, repo_id } },
      body: Buffer.from('Hello Relace!\n').toString(),
      headers: { 'content-type': 'application/octet-stream' },
    })
    console.log('Uploaded', file_path)

    // Download file
    const { data: fileContent } = await client.GET(
      '/repo/{repo_id}/file/{file_path}',
      {
        params: { path: { repo_id, file_path } },
      }
    )
    console.log('Downloaded content:', fileContent)

    // Delete file (auto-committed)
    await client.DELETE('/repo/{repo_id}/file/{file_path}', {
      params: { path: { repo_id, file_path } },
    })
    console.log('Deleted', file_path)

    // Cleanup repo
    await client.DELETE('/repo/{repo_id}', { params: { path: { repo_id } } })
  } catch (e) {
    console.error('Example failed:', e)
    process.exit(1)
  }
})()
