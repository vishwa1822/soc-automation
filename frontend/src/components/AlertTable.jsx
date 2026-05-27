import { useEffect, useState } from "react"
import { API_BASE } from "../apiBase"

export default function AlertTable({ className = "" }) {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await fetch(`${API_BASE}/alerts`)
        if (!res.ok) return
        const data = await res.json()
        const list = Array.isArray(data.alerts) ? data.alerts : []
        setAlerts(list.slice(-4).reverse())
      } catch {
        // ignore
      }
    }

    fetchAlerts()
    const interval = setInterval(fetchAlerts, 8000)
    return () => clearInterval(interval)
  }, [])

  const severityClass = (sev) => {
    if (!sev) return "pill"
    const s = String(sev).toUpperCase()
    if (s === "CRITICAL") return "pill pill--critical"
    if (s === "HIGH") return "pill pill--high"
    if (s === "MEDIUM") return "pill pill--medium"
    if (s === "LOW") return "pill pill--low"
    return "pill"
  }

  return (
    <div className={`card ${className}`.trim()}>
      <div className="title">Recent Alerts</div>
      <p className="subtitle">Latest detections across honeytokens and enumeration.</p>

      <table style={{ marginTop: "10px" }}>
        <thead>
          <tr>
            <th>Time</th>
            <th>Endpoint</th>
            <th>IP</th>
            <th>Severity</th>
          </tr>
        </thead>

        <tbody>
          {alerts.length === 0 && (
            <tr>
              <td colSpan={4} style={{ paddingTop: "10px", fontSize: "13px", color: "var(--muted)" }}>
                No alerts yet. The dashboard will populate as activity is detected.
              </td>
            </tr>
          )}

          {alerts.map((alert, index) => (
            <tr key={index}>
              <td>{alert.timestamp}</td>
              <td>{alert.endpoint || "-"}</td>
              <td>{alert.ip || alert.ip_address || "-"}</td>
              <td>
                <span className={severityClass(alert.severity)}>
                  {alert.severity || "N/A"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

