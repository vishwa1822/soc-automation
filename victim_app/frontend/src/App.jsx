import { useCallback, useEffect, useState } from "react"

const VICTIM_BASE = import.meta.env.VITE_VICTIM_API_BASE || "http://127.0.0.1:8080"

export default function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)
  const [socOk, setSocOk] = useState(null)

  const refreshHealth = useCallback(async () => {
    try {
      const r = await fetch(`${VICTIM_BASE}/health`)
      const data = await r.json()
      setSocOk(!!data.soc_reachable)
    } catch {
      setSocOk(false)
    }
  }, [])

  useEffect(() => {
    refreshHealth()
    const t = setInterval(refreshHealth, 8000)
    return () => clearInterval(t)
  }, [refreshHealth])

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage("")

    try {
      const response = await fetch(`${VICTIM_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      })
      const data = await response.json()
      const tail = data.soc_logged === false ? " (SOC log forward failed — is the API on :8000 running?)" : ""
      setMessage((data.status || "Done") + tail)
    } catch {
      setMessage("Error: could not reach the victim API. Start it from the victim_app folder: uvicorn app:app --port 8080")
    } finally {
      setLoading(false)
    }
  }

  const pingPath = async (path) => {
    try {
      await fetch(`${VICTIM_BASE}${path}`, { method: "GET" })
      setMessage(`Requested ${path} — check SOC alerts / timeline for the generated log.`)
    } catch {
      setMessage("Request failed — is the victim API running on :8080?")
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background:
          "radial-gradient(900px 400px at 20% 0%, rgba(64,93,230,0.12), transparent 55%), radial-gradient(700px 360px at 100% 20%, rgba(214,41,118,0.08), transparent 50%), #f4f5fb",
        fontFamily: "Inter, system-ui, sans-serif",
        padding: 16,
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 420,
          background: "#fff",
          borderRadius: 16,
          padding: "1.75rem",
          boxShadow: "0 18px 40px rgba(20,25,40,0.12)",
          border: "1px solid rgba(20,25,40,0.08)",
        }}
      >
        <p style={{ margin: "0 0 0.35rem 0", fontSize: 12, fontWeight: 700, color: "#6b6f80", letterSpacing: "0.06em" }}>
          VICTIM SIMULATOR
        </p>
        <h1 style={{ margin: "0 0 0.25rem 0", fontSize: 26, fontWeight: 800, color: "#101116" }}>Login portal</h1>
        <p style={{ margin: "0 0 1rem 0", fontSize: 13, color: "#6b6f80", lineHeight: 1.45 }}>
          Each sign-in sends a structured event to the SOC <strong>/ingest-log</strong> pipeline (same as the main dashboard log processor).
        </p>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginBottom: "1rem",
            fontSize: 12,
            padding: "8px 10px",
            borderRadius: 10,
            background: socOk === true ? "rgba(64,93,230,0.08)" : socOk === false ? "rgba(214,41,118,0.08)" : "rgba(20,25,40,0.05)",
            color: "#101116",
          }}
        >
          <span style={{ fontWeight: 800 }}>SOC API</span>
          <span style={{ color: "#6b6f80" }}>
            {socOk === null ? "checking…" : socOk ? "reachable on :8000" : "not reachable — start backend first"}
          </span>
        </div>

        <form onSubmit={handleLogin}>
          <label style={label}>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={input}
            placeholder="demo or admin"
            autoComplete="username"
          />

          <label style={{ ...label, marginTop: 14 }}>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={input}
            placeholder="demo or password123"
            autoComplete="current-password"
          />

          <button type="submit" disabled={loading} style={btn(loading)}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p style={{ margin: "12px 0 0 0", fontSize: 12, color: "#6b6f80", lineHeight: 1.5 }}>
          <strong>Demo success:</strong> <code style={code}>demo</code> / <code style={code}>demo</code> or{" "}
          <code style={code}>admin</code> / <code style={code}>password123</code>. Anything else records a failed login (401) for the SOC.
        </p>

        {message && (
          <div
            style={{
              marginTop: "1rem",
              padding: "0.75rem 0.85rem",
              borderRadius: 10,
              backgroundColor: message.includes("Error") || message.includes("failed") ? "rgba(214,41,118,0.08)" : "rgba(64,93,230,0.08)",
              color: "#101116",
              fontSize: 13,
              lineHeight: 1.45,
            }}
          >
            {message}
          </div>
        )}

        <div style={{ marginTop: "1.25rem", paddingTop: "1rem", borderTop: "1px solid rgba(20,25,40,0.08)" }}>
          <p style={{ margin: "0 0 8px 0", fontSize: 12, fontWeight: 700, color: "#6b6f80" }}>Extra traffic (optional)</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            <button type="button" style={ghostBtn} onClick={() => pingPath("/admin")}>
              Open /admin
            </button>
            <button type="button" style={ghostBtn} onClick={() => pingPath("/config")}>
              Open /config
            </button>
            <button type="button" style={ghostBtn} onClick={() => pingPath("/debug-console")}>
              Open /debug-console
            </button>
          </div>
          <p style={{ margin: "10px 0 0 0", fontSize: 11, color: "#6b6f80" }}>
            Victim API: <code style={code}>{VICTIM_BASE}</code> · Run from repo: <code style={code}>npm run dev:victim</code> (cwd must be{" "}
            <code style={code}>victim_app</code>, not <code style={code}>victim_app/victim_app</code>).
          </p>
        </div>
      </div>
    </div>
  )
}

const label = { display: "block", marginBottom: 6, fontWeight: 600, fontSize: 13, color: "#101116" }
const input = {
  width: "100%",
  padding: "10px 12px",
  border: "1px solid rgba(20,25,40,0.12)",
  borderRadius: 10,
  fontSize: 15,
  boxSizing: "border-box",
  outline: "none",
}
const btn = (loading) => ({
  width: "100%",
  marginTop: 16,
  padding: "11px 14px",
  border: "none",
  borderRadius: 10,
  fontSize: 15,
  fontWeight: 700,
  cursor: loading ? "not-allowed" : "pointer",
  color: "#fff",
  background: loading ? "#a8adbf" : "linear-gradient(90deg,#405DE6,#833AB4,#C13584)",
})
const ghostBtn = {
  padding: "7px 12px",
  fontSize: 12,
  fontWeight: 600,
  borderRadius: 8,
  border: "1px solid rgba(64,93,230,0.35)",
  background: "#fff",
  color: "#405DE6",
  cursor: "pointer",
}
const code = { background: "rgba(20,25,40,0.06)", padding: "2px 6px", borderRadius: 6, fontSize: 12 }
