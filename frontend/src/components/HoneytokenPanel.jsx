import { useEffect, useState } from "react"

export default function HoneytokenPanel({ className = "" }) {

  const [status, setStatus] = useState(null)
  const [triggers, setTriggers] = useState([])
  const [toggling, setToggling] = useState(false)

  const fetchData = async () => {
    try {
      const [statusRes, triggerRes] = await Promise.all([
        fetch("http://127.0.0.1:8000/honeytokens/status"),
        fetch("http://127.0.0.1:8000/honeytokens/triggers")
      ])

      const statusJson = await statusRes.json()
      const triggerJson = await triggerRes.json()

      setStatus(statusJson)
      setTriggers(Array.isArray(triggerJson.triggers) ? triggerJson.triggers.slice(-5).reverse() : [])
    } catch {
      // swallow network errors for dashboard
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 8000)
    return () => clearInterval(interval)
  }, [])

  const enabled = status?.enabled
  const activeCount = (status?.active_traps || []).length

  const toggleHoneytokens = async (target) => {
    setToggling(true)
    try {
      const endpoint = target === "enable"
        ? "http://127.0.0.1:8000/honeytokens/enable"
        : "http://127.0.0.1:8000/honeytokens/disable"
      await fetch(endpoint, { method: "POST" })
      await fetchData()
    } catch {
      // ignore failure, UI will stay as-is
    } finally {
      setToggling(false)
    }
  }

  return (
    <div className={`card ${className}`.trim()}>

      <div className="title">
        Honeytoken Traps
      </div>

      <p className="subtitle">
        Dynamic deception endpoints and recent trap activity.
      </p>

      <div style={{ display: "flex", marginTop: "14px", gap: "18px", alignItems: "flex-end" }}>

        <div>
          <div style={{ fontSize: "13px", color: "var(--muted)" }}>Status</div>
          <div style={{ marginTop: "4px" }}>
            {enabled ? (
              <span className="pill pill--high">Enabled</span>
            ) : (
              <span className="pill pill--low">Disabled</span>
            )}
          </div>
        </div>

        <div>
          <div style={{ fontSize: "13px", color: "var(--muted)" }}>Active traps</div>
          <div style={{ marginTop: "4px", fontSize: "20px", fontWeight: 800, color: "var(--ink)" }}>
            {activeCount}
          </div>
        </div>

        <div style={{ marginLeft: "auto", display: "flex", gap: "8px" }}>
          <button
            className="ai-button"
            style={{ padding: "7px 12px" }}
            disabled={toggling || enabled}
            onClick={() => toggleHoneytokens("enable")}
          >
            Enable
          </button>
          <button
            className="ai-button"
            style={{ padding: "7px 12px", background: "transparent", color: "var(--rb)", border: "1px solid rgba(64,93,230,0.35)" }}
            disabled={toggling || !enabled}
            onClick={() => toggleHoneytokens("disable")}
          >
            Disable
          </button>
        </div>

      </div>

      <div style={{ marginTop: "18px" }}>
        <div style={{ fontSize: "13px", color: "var(--muted)", marginBottom: "6px" }}>
          Recent triggers
        </div>

        {triggers.length === 0 && (
          <p style={{ fontSize: "13px", color: "var(--muted)" }}>
            No honeytoken activity observed yet.
          </p>
        )}

        {triggers.map((t, idx) => (
          <div
            key={idx}
            style={{
              padding: "6px 0",
              borderBottom: "1px solid var(--line)",
              fontSize: "12px",
              display: "flex",
              justifyContent: "space-between",
              gap: "12px"
            }}
          >
            <span style={{ color: "var(--ink)" }}>
              {t.endpoint}
            </span>
            <span style={{ color: "var(--muted)" }}>
              {t.ip || "unknown"}
            </span>
          </div>
        ))}
      </div>

    </div>
  )
}     

