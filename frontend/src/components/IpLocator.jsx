import { useState } from "react"

export default function IpLocator({ className = "" }) {

  const [ip, setIp] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const locate = async () => {
    if (!ip.trim()) return
    setLoading(true)
    setResult(null)
    try {
      const res = await fetch("http://127.0.0.1:8000/ip-lookup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ ip })
      })
      const data = await res.json()
      if (res.ok) {
        setResult(data)
      } else {
        setResult({ error: data.detail || "Lookup failed" })
      }
    } catch {
      setResult({ error: "IP lookup service not available" })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`card ${className}`.trim()}>

      <div className="title">
        IP Locator
      </div>

      <p className="subtitle">
        Resolve an IP address to approximate geo and provider.
      </p>

      <div style={{ display: "flex", gap: "8px", marginTop: "10px" }}>
        <input
          className="ai-input"
          style={{ flex: 1 }}
          type="text"
          placeholder="Enter IP, e.g. 8.8.8.8"
          value={ip}
          onChange={(e) => setIp(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              locate()
            }
          }}
        />
        <button
          className="ai-button"
          style={{ whiteSpace: "nowrap" }}
          disabled={loading}
          onClick={locate}
        >
          {loading ? "Locating..." : "Locate"}
        </button>
      </div>

      {result && (
        <div className="ai-response" style={{ marginTop: "12px" }}>
          {result.error ? (
            <div style={{ fontSize: "13px", color: "var(--pk)" }}>
              {result.error}
            </div>
          ) : (
            <div style={{ fontSize: "13px", color: "var(--ink)", display: "grid", rowGap: "4px" }}>
              <div><strong>IP:</strong> {result.ip}</div>
              <div><strong>Location:</strong> {result.city || "-"}, {result.country || "-"}</div>
              <div><strong>Coordinates:</strong> {result.lat ?? "-"}, {result.lon ?? "-"}</div>
              <div><strong>Org / ISP:</strong> {result.org || result.isp || "-"}</div>
            </div>
          )}
        </div>
      )}

    </div>
  )
}

