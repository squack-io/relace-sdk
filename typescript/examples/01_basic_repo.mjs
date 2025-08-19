// Basic example: create a repo from files, fetch metadata, and delete it.
// Requirements: set RELACE_API_KEY in your environment. Optionally RELACE_BASE_URL.
import createRelaceClient from '@relace-ai/agent-client'

const client = createRelaceClient({ apiKey: import.meta.env.RELACE_API_KEY })

// 1) Create a repo from a couple of files
const { data: created, error: createErr } = await client.POST('/repo', {
  body: {
    source: {
      type: 'files',
      files: [
        { filename: 'README.md', content: '# Hello from Relace\n' },
        {
          filename: 'src/index.ts',
          content: "export const hello='world'\n",
        },
      ],
    },
    metadata: { example: 'basic' },
  },
})
if (createErr) throw createErr
console.log('Created repo:', created)

// 2) Get metadata
const { data: meta } = await client.GET('/repo/{repo_id}', {
  params: { path: { repo_id: created.repo_id } },
})
console.log('Metadata:', meta)

// 3) Cleanup
const { response } = await client.DELETE('/repo/{repo_id}', {
  params: { path: { repo_id: created.repo_id } },
})
console.log('Deleted repo, status:', response.status)
