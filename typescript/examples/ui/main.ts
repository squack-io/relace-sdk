import createRelaceClient from "@relace-ai/agent-client"

const logEl = document.getElementById("log")!
function log(...args: any[]) {
  const line = args
    .map((a) => (typeof a === "string" ? a : JSON.stringify(a)))
    .join(" ")
  logEl.textContent += line + "\n"
}

// Values injected by Vite define() into window.* in vite.config.ts
const API_KEY: string = import.meta.env.RELACE_API_KEY

if (!API_KEY) log("Missing RELACE_API_KEY in env")

const client = createRelaceClient({ apiKey: API_KEY })
let repoId: string | undefined

const $ = (id: string) => document.getElementById(id) as HTMLInputElement

$("createRepo").addEventListener("click", async () => {
  try {
    const sourceType = $("sourceType").value as "files" | "git"
    let body: any = { metadata: { ui: "demo" } }
    if (sourceType === "git") {
      const url = $("gitUrl").value.trim()
      if (!url) return alert("Enter Git URL")
      body.source = { type: "git", url }
    } else {
      body.source = {
        type: "files",
        files: [{ filename: "README.md", content: "# UI demo\n" }],
      }
    }
    const { data, error } = await client.POST("/repo", { body })
    if (error) throw error
    repoId = data!.repo_id
    log("Repo created:", data)
  } catch (e) {
    console.error(e)
    log("Error:", String(e))
  }
})

$("runAgent").addEventListener("click", async () => {
  if (!repoId) return alert("Create a repo first")
  const agentName = $("agentName").value || "default"
  let inputs: Record<string, string> = {}
  try {
    inputs = JSON.parse(
      (document.getElementById("agentInputs") as HTMLTextAreaElement).value
    )
  } catch {}

  const res = await fetch(`/repo/${repoId}/agent`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify({
      agent_name: agentName,
      agent_inputs: inputs,
      overrides: null,
    }),
  })

  if (!res.ok || !res.body) {
    log("HTTP error", String(res.status))
    return
  }
  log("Agent stream opened...")
  const reader = res.body.getReader()
  const dec = new TextDecoder()
  let buffer = ""
  ;(async () => {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += dec.decode(value, { stream: true })
      let idx: number
      while ((idx = buffer.indexOf("\n\n")) !== -1) {
        const chunk = buffer.slice(0, idx)
        buffer = buffer.slice(idx + 2)
        for (const line of chunk.split("\n")) {
          const t = line.trim()
          if (!t) continue
          if (t.startsWith("data:")) {
            const payload = t.slice(5).trim()
            try {
              log("event:", JSON.parse(payload))
            } catch {
              log("data:", payload)
            }
          }
        }
      }
    }
    log("Agent stream closed.")
  })()
})
