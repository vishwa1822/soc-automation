import { useState } from "react"

export default function AIChat({ className = "" }) {
  const [query, setQuery] = useState("")
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState(null)

  const askAI = async () => {
    if (!query.trim()) return
    setLoading(true)
    setResponse(null)
    try {
      const res = await fetch("http://127.0.0.1:8000/ask-soc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      })
      const data = await res.json()
      if (data.status === "success") {
        setResponse(data)
      } else {
        setResponse({ analysis: "AI could not process this query." })
      }
    } catch {
      setResponse({ analysis: "AI backend is not available right now." })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`card ${className}`.trim()}>
      <div className="title">Ask AI</div>
      <p className="subtitle">Summarize alerts, explain patterns, or investigate users.</p>

      <input
        className="ai-input"
        type="text"
        placeholder="e.g. Explain recent admin activity"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") askAI()
        }}
      />

      <button className="ai-button" disabled={loading} onClick={askAI}>
        {loading ? "Asking..." : "Ask AI"}
      </button>

      {response && (
        <div className="ai-response">
          <div style={{ fontWeight: 800, marginBottom: "4px", color: "var(--ink)" }}>AI Response</div>
          <div style={{ fontSize: "13px", color: "var(--ink)" }}>
            {response.analysis || "No explanation available."}
          </div>
        </div>
      )}
    </div>
  )
}

