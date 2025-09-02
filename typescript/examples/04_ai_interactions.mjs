// AI interactions: ask a question and retrieve relevant content
import createRelaceClient from '@relace-ai/agent-client'

const client = createRelaceClient({ apiKey: import.meta.env.RELACE_API_KEY })

;(async () => {
  let repo_id
  try {
    // Create from files to have some content
    const { data: created } = await client.POST('/repo', {
      body: {
        source: {
          type: 'files',
          files: [
            { filename: 'README.md', content: '# Project\nThis is a demo.\n' },
          ],
        },
      },
    })
    if (!created) {
      console.error('Failed to create repo')
      process.exit(1)
    }
    repo_id = created.repo_id

    // Ask a question
    const { data: answer } = await client.POST('/repo/{repo_id}/ask', {
      params: { path: { repo_id } },
      body: {
        query: 'What does this repository contain?',
        rerank: true,
        token_limit: 10_000,
      },
    })
    console.log('Answer:', answer?.answer)

    // Retrieve relevant content
    const { data: retrieval } = await client.POST('/repo/{repo_id}/retrieve', {
      params: { path: { repo_id } },
      body: {
        query: 'demo',
        rerank: true,
        include_content: true,
        score_threshold: 0.2,
        token_limit: 2000,
      },
    })
    console.log(
      'Retrieve results:',
      retrieval?.results.map((r) => ({ file: r.filename, score: r.score })),
    )
  } catch (e) {
    console.error(e)
    process.exit(1)
  } finally {
    if (repo_id)
      await client.DELETE('/repo/{repo_id}', { params: { path: { repo_id } } })
  }
})()
