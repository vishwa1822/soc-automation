import { useEffect, useState } from "react"
import { API_BASE } from "../apiBase"
import HoneytokenPanel from "../components/HoneytokenPanel"
import AlertTable from "../components/AlertTable"
import AIChat from "../components/AIChat"
import IpLocator from "../components/IpLocator"

import PageHeader from "../components/PageHeader"

export default function Workspace({ onToggleSidebar, isSidebarOpen }) {
  return (
    <div className="container">
      <PageHeader title="Workspace" subtitle="SOC Operations Dashboard" onToggleSidebar={onToggleSidebar} isSidebarOpen={isSidebarOpen} />

      <div className="dashboard-grid">
        <InlineRiskCard className="card--blue" />
        <HoneytokenPanel className="card--sunset" />

        <div className="dashboard-grid--full">
          <AlertTable className="card--pink" />
        </div>

        <AIChat className="card--blue" />
        <IpLocator className="card--sunset" />
      </div>
    </div>
  )
}

function InlineRiskCard({ className = "" }) {
  const [status, setStatus] = useState(null)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch(`${API_BASE}/system-status`)
        if (!res.ok) return
        const data = await res.json()
        setStatus(data)
      } catch {
        // ignore
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 15000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className={`card ${className}`.trim()}>
      <div className="title">SOC Overview</div>
      <p className="subtitle">High-level status of the detection stack.</p>

      <div style={{ marginTop: "10px", display: "flex", alignItems: "baseline", gap: "10px" }}>
        <div style={{ fontSize: "26px", fontWeight: 900, color: "var(--ink)" }}>Live</div>
        <div style={{ fontSize: "12px", color: "var(--muted)" }}>Monitoring</div>
      </div>

      <div style={{ marginTop: "10px", fontSize: "13px", color: "var(--muted)" }}>
        Engine: {status?.engine || "SOC Detection Engine"} · Status: {status?.status || "running"} · Version: {status?.version || "1.0"}
      </div>

      <div style={{ marginTop: "10px", display: "flex", gap: "8px", flexWrap: "wrap" }}>
        {(status?.engines || ["honeytoken_engine", "enumeration_detector", "alert_engine"]).slice(0, 3).map((e) => (
          <span key={e} className="pill pill--low">{e}</span>
        ))}
      </div>
    </div>
  )
}

