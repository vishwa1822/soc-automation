import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { API_BASE } from "../apiBase"
import PageHeader from "../components/PageHeader"

const secondaryBtn = {
  background: "transparent",
  color: "var(--rb)",
  border: "1px solid rgba(64,93,230,0.35)"
}

export default function Soar({ onToggleSidebar, isSidebarOpen }) {
  const [alerts, setAlerts] = useState([])
  const [triggers, setTriggers] = useState([])
  const [autoBlockEnabled, setAutoBlockEnabled] = useState(true)
  const [riskThreshold, setRiskThreshold] = useState(70)
  const [blockedIps, setBlockedIps] = useState([])
  const [actionMessage, setActionMessage] = useState("")
  const [reporting, setReporting] = useState(false)
  const [automationOn, setAutomationOn] = useState(true)
  const [playbooks, setPlaybooks] = useState([
    { id: "pb-contain-login", name: "Contain Suspicious Login", trigger: "Impossible travel + MFA failures", owner: "IAM", enabled: true },
    { id: "pb-isolate-host", name: "Isolate Compromised Host", trigger: "Critical malware beacon", owner: "Endpoint", enabled: true },
    { id: "pb-honeytoken", name: "Honeytoken Response", trigger: "Credential/file token touched", owner: "SOC", enabled: true },
    { id: "pb-ip-block", name: "Block Malicious IP", trigger: "Repeated high-severity scanning", owner: "Network", enabled: true }
  ])

  const skipInitialThresholdPost = useRef(true)

  const mergeSoarState = useCallback((soar) => {
    if (!soar || typeof soar !== "object") return
    if (typeof soar.automation_on === "boolean") setAutomationOn(soar.automation_on)
    if (typeof soar.auto_block_enabled === "boolean") setAutoBlockEnabled(soar.auto_block_enabled)
    if (typeof soar.risk_threshold === "number") setRiskThreshold(soar.risk_threshold)
    if (Array.isArray(soar.blocked_ips)) setBlockedIps([...soar.blocked_ips])
    if (Array.isArray(soar.playbooks) && soar.playbooks.length > 0) setPlaybooks(soar.playbooks.map((p) => ({ ...p })))
    if (soar.last_message) setActionMessage(String(soar.last_message))
  }, [])

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await fetch(`${API_BASE}/soar/dashboard`)
        if (!res.ok) return
        const data = await res.json()
        setAlerts(Array.isArray(data.alerts) ? data.alerts : [])
        setTriggers(Array.isArray(data.triggers) ? data.triggers : [])
        mergeSoarState(data.soar)
      } catch {
        // Keep dashboard responsive if backend is unavailable.
      }
    }

    fetchDashboard()
    const interval = setInterval(fetchDashboard, 10000)
    return () => clearInterval(interval)
  }, [mergeSoarState])

  useEffect(() => {
    if (skipInitialThresholdPost.current) {
      skipInitialThresholdPost.current = false
      return
    }
    const t = setTimeout(async () => {
      try {
        const res = await fetch(`${API_BASE}/soar/threshold`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ threshold: riskThreshold })
        })
        if (!res.ok) return
        const data = await res.json()
        mergeSoarState(data.state)
      } catch {
        // ignore
      }
    }, 450)
    return () => clearTimeout(t)
  }, [riskThreshold, mergeSoarState])

  const enrichedAlerts = useMemo(() => {
    return alerts.map((alert, idx) => {
      const severity = String(alert?.severity || "LOW").toUpperCase()
      const ip = alert?.ip || alert?.ip_address || "unknown"
      const endpoint = alert?.endpoint || "n/a"
      return {
        id: `${alert?.timestamp || "now"}-${ip}-${idx}`,
        ip,
        endpoint,
        severity,
        timestamp: alert?.timestamp || "live",
        riskScore: riskScoreFromAlert(alert)
      }
    })
  }, [alerts])

  const riskyCandidates = useMemo(() => {
    return enrichedAlerts
      .filter((item) => item.riskScore >= riskThreshold && item.ip !== "unknown")
      .sort((a, b) => b.riskScore - a.riskScore)
      .slice(0, 6)
  }, [enrichedAlerts, riskThreshold])

  const history = useMemo(() => {
    const attackHistory = enrichedAlerts.slice(-8).map((item) => ({
      type: "attack",
      label: `${item.severity} alert on ${item.endpoint}`,
      ip: item.ip,
      time: item.timestamp
    }))
    const honeyHistory = triggers.slice(-8).map((item) => ({
      type: "honeytoken",
      label: `Trap hit at ${item.endpoint || "unknown endpoint"}`,
      ip: item.ip || "unknown",
      time: item.timestamp || "recent"
    }))
    return [...attackHistory, ...honeyHistory].slice(-12).reverse()
  }, [enrichedAlerts, triggers])

  const activePlaybooks = playbooks.filter((pb) => pb.enabled).length
  const autoActions = blockedIps.length + triggers.length
  const avgRisk = enrichedAlerts.length
    ? Math.round(enrichedAlerts.reduce((sum, item) => sum + item.riskScore, 0) / enrichedAlerts.length)
    : 0

  const handleBlockIp = async (ip, reason) => {
    if (!ip || ip === "unknown") return
    try {
      const res = await fetch(`${API_BASE}/soar/block-ip`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ip, reason: reason || "" })
      })
      if (!res.ok) return
      const data = await res.json()
      mergeSoarState(data.state)
    } catch {
      // ignore
    }
  }

  const handleRunAutoBlock = async () => {
    if (!autoBlockEnabled || !automationOn) {
      setActionMessage("Enable automation and auto-block first.")
      return
    }
    try {
      const res = await fetch(`${API_BASE}/soar/auto-block-run`, { method: "POST" })
      if (!res.ok) return
      const data = await res.json()
      mergeSoarState(data.state)
    } catch {
      // ignore
    }
  }

  const handleGenerateReport = () => {
    setReporting(true)
    try {
      const lines = [
        "SOC SOAR REPORT",
        `Generated: ${new Date().toLocaleString()}`,
        "",
        `Automation enabled: ${automationOn ? "Yes" : "No"}`,
        `Auto IP block enabled: ${autoBlockEnabled ? "Yes" : "No"} | Threshold: ${riskThreshold}`,
        `Active playbooks: ${activePlaybooks}/${playbooks.length}`,
        `Blocked IP count: ${blockedIps.length}`,
        "",
        "Blocked IPs:",
        ...(blockedIps.length ? blockedIps.map((ip) => `- ${ip}`) : ["- none"]),
        "",
        "Recent History:",
        ...(history.length
          ? history.map((item) => `- [${item.type}] ${item.time} | ${item.label} | ${item.ip}`)
          : ["- none"])
      ]
      const blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" })
      const url = URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = url
      link.download = `soar-report-${Date.now()}.txt`
      document.body.appendChild(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(url)
      setActionMessage("SOAR report generated and downloaded.")
    } finally {
      setReporting(false)
    }
  }

  const togglePlaybook = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/soar/playbook/${encodeURIComponent(id)}/toggle`, { method: "POST" })
      if (!res.ok) return
      const data = await res.json()
      mergeSoarState(data.state)
    } catch {
      // ignore
    }
  }

  const toggleAllPlaybooks = async () => {
    const target = !automationOn
    try {
      const res = await fetch(`${API_BASE}/soar/automation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled: target })
      })
      if (!res.ok) return
      const data = await res.json()
      mergeSoarState(data.state)
    } catch {
      // ignore
    }
  }

  const setAutoBlock = async (next) => {
    try {
      const res = await fetch(`${API_BASE}/soar/auto-block`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled: next })
      })
      if (!res.ok) return
      const data = await res.json()
      mergeSoarState(data.state)
    } catch {
      // ignore
    }
  }

  return (
    <div className="container">
      <PageHeader title="SOAR" subtitle="Playbook-driven response and risk-based actions" onToggleSidebar={onToggleSidebar} isSidebarOpen={isSidebarOpen} />

      <div style={{ flex: 1, minHeight: 0, minWidth: 0, overflow: "auto" }}>
        <div className="dashboard-grid">
        <div className="card card--blue dashboard-grid--full">
          <div className="title">SOAR Control Center</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))", gap: 10, marginTop: 8 }}>
            <Kpi label="Active playbooks" value={`${activePlaybooks}/${playbooks.length}`} />
            <Kpi label="Automated actions" value={`${autoActions}`} />
            <Kpi label="Avg risk score" value={`${avgRisk}`} />
            <Kpi label="Blocked IPs" value={`${blockedIps.length}`} />
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 10, marginTop: 12, alignItems: "center" }}>
            <button type="button" className="ai-button" style={{ marginTop: 0 }} onClick={toggleAllPlaybooks}>
              {automationOn ? "Pause Automation" : "Resume Automation"}
            </button>
            <button type="button" className="ai-button" style={{ ...secondaryBtn, marginTop: 0 }} onClick={handleGenerateReport} disabled={reporting}>
              {reporting ? "Generating..." : "Generate Report"}
            </button>
          </div>
          {actionMessage && (
            <p style={{ margin: "10px 0 0 0", fontSize: 12, color: "var(--muted)" }}>{actionMessage}</p>
          )}
        </div>

        <div className="card card--pink" style={{ minHeight: 0, display: "flex", flexDirection: "column" }}>
          <div className="title">Risk-Based IP Block</div>
          <p className="subtitle">Automatically block source IPs when risk score crosses threshold.</p>
          <label style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 10, cursor: "pointer", fontSize: 12, color: "var(--muted)", fontWeight: 700 }}>
            <input
              type="checkbox"
              checked={autoBlockEnabled}
              onChange={(e) => setAutoBlock(e.target.checked)}
              style={{ width: 16, height: 16, accentColor: "var(--rb)" }}
            />
            {autoBlockEnabled ? "Auto block enabled" : "Auto block disabled"}
          </label>
          <div style={{ marginTop: 12 }}>
            <label htmlFor="risk-threshold" style={{ display: "block", fontSize: 12, color: "var(--muted)", marginBottom: 6 }}>
              Risk threshold: {riskThreshold}
            </label>
            <input
              id="risk-threshold"
              type="range"
              min={40}
              max={95}
              step={5}
              value={riskThreshold}
              onChange={(e) => setRiskThreshold(Number(e.target.value))}
              style={{ width: "100%", accentColor: "#a678ff" }}
            />
          </div>
          <div style={{ marginTop: 12, flex: 1, minHeight: 0, overflow: "auto", display: "grid", gap: 8 }}>
            {riskyCandidates.length === 0 ? (
              <p className="subtitle" style={{ margin: 0 }}>
                No candidate IPs above threshold yet.
              </p>
            ) : (
              riskyCandidates.map((item) => (
                <div
                  key={item.id}
                  style={{
                    border: "1px solid var(--line)",
                    borderRadius: 10,
                    padding: "8px 10px",
                    background: "rgba(255,255,255,0.58)",
                    display: "grid",
                    gridTemplateColumns: "minmax(0, 1fr) auto",
                    gap: 10,
                    alignItems: "center"
                  }}
                >
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 700 }}>{item.ip}</div>
                    <div style={{ marginTop: 2, fontSize: 12, color: "var(--muted)" }}>
                      {item.endpoint} · score {item.riskScore}
                    </div>
                  </div>
                  <button type="button" className="ai-button" style={{ marginTop: 0 }} onClick={() => handleBlockIp(item.ip, `risk ${item.riskScore}`)} disabled={blockedIps.includes(item.ip)}>
                    {blockedIps.includes(item.ip) ? "Blocked" : "Block IP"}
                  </button>
                </div>
              ))
            )}
          </div>
          <button type="button" className="ai-button" onClick={handleRunAutoBlock} disabled={!autoBlockEnabled || !automationOn}>
            Run Auto-Block Now
          </button>
        </div>

        <div className="card card--sunset" style={{ minHeight: 0, display: "flex", flexDirection: "column" }}>
          <div className="title">Playbook Automation</div>
          <p className="subtitle">Primary response engine for containment, enrichment, and ticketing.</p>
          <div style={{ marginTop: 10, flex: 1, minHeight: 0, overflow: "auto" }}>
            <table style={{ width: "100%", fontSize: 12, tableLayout: "fixed" }}>
              <thead>
                <tr>
                  <th style={{ width: "22%" }}>Playbook</th>
                  <th style={{ width: "38%" }}>Trigger</th>
                  <th style={{ width: "14%" }}>Owner</th>
                  <th style={{ width: "12%" }}>State</th>
                  <th style={{ width: "14%" }} />
                </tr>
              </thead>
              <tbody>
                {playbooks.map((row) => (
                  <tr key={row.id}>
                    <td style={{ fontWeight: 700, verticalAlign: "top", wordBreak: "break-word" }}>{row.name}</td>
                    <td style={{ color: "var(--muted)", verticalAlign: "top", wordBreak: "break-word", minWidth: 0 }}>{row.trigger}</td>
                    <td style={{ verticalAlign: "top", wordBreak: "break-word" }}>{row.owner}</td>
                    <td style={{ verticalAlign: "top" }}>
                      <span className={`pill ${row.enabled ? "pill--low" : "pill--medium"}`}>{row.enabled ? "On" : "Off"}</span>
                    </td>
                    <td style={{ verticalAlign: "top", textAlign: "right" }}>
                      <button
                        type="button"
                        className="ai-button"
                        style={{ marginTop: 0, padding: "6px 10px", fontSize: 12, ...(row.enabled ? {} : secondaryBtn) }}
                        onClick={() => togglePlaybook(row.id)}
                      >
                        {row.enabled ? "Disable" : "Enable"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="card dashboard-grid--full" style={{ minHeight: 0, display: "flex", flexDirection: "column" }}>
          <div className="title">Attack & Honeytoken History</div>
          <p className="subtitle">Unified stream for threat alerts and deception-trigger events.</p>
          <div style={{ marginTop: 10, flex: 1, minHeight: 0, overflow: "auto" }}>
            {history.length === 0 ? (
              <p className="subtitle" style={{ margin: 0 }}>
                No recent activity yet.
              </p>
            ) : (
              <table style={{ width: "100%", fontSize: 12, tableLayout: "fixed" }}>
                <thead>
                  <tr>
                    <th style={{ width: "14%" }}>Time</th>
                    <th style={{ width: "14%" }}>Type</th>
                    <th style={{ width: "48%" }}>Event</th>
                    <th style={{ width: "24%" }}>IP</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((item, idx) => (
                    <tr key={`${item.time}-${item.ip}-${idx}`}>
                      <td style={{ color: "var(--muted)", fontWeight: 700, verticalAlign: "top", wordBreak: "break-word" }}>{item.time}</td>
                      <td style={{ verticalAlign: "top" }}>
                        <span className={`pill ${item.type === "honeytoken" ? "pill--high" : "pill--low"}`}>{item.type}</span>
                      </td>
                      <td style={{ verticalAlign: "top", wordBreak: "break-word", minWidth: 0 }}>{item.label}</td>
                      <td style={{ fontFamily: "ui-monospace, monospace", verticalAlign: "top", wordBreak: "break-all" }}>{item.ip}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
        </div>
      </div>
    </div>
  )
}

function Kpi({ label, value }) {
  return (
    <div
      style={{
        border: "1px solid var(--line)",
        borderRadius: 12,
        padding: 12,
        background: "rgba(255,255,255,0.62)",
        minHeight: 76,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center"
      }}
    >
      <div style={{ fontSize: 24, fontWeight: 800, color: "var(--ink)" }}>{value}</div>
      <div style={{ marginTop: 4, fontSize: 12, color: "var(--muted)" }}>{label}</div>
    </div>
  )
}

function computeRiskScore(severity) {
  if (severity === "CRITICAL") return 92
  if (severity === "HIGH") return 78
  if (severity === "MEDIUM") return 62
  return 44
}

function riskScoreFromAlert(alert) {
  const rs = alert?.risk_score
  if (typeof rs === "number" && !Number.isNaN(rs)) {
    return Math.min(100, Math.max(0, Math.round(rs)))
  }
  const severity = String(alert?.severity || "LOW").toUpperCase()
  return computeRiskScore(severity)
}
