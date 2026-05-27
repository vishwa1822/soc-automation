import { useEffect, useMemo, useState } from "react"
import { API_BASE } from "../apiBase"
import HoneytokenPanel from "../components/HoneytokenPanel"
import IpLocator from "../components/IpLocator"
import PageHeader from "../components/PageHeader"

export default function Visualization({ onToggleSidebar, isSidebarOpen }) {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await fetch(`${API_BASE}/alerts`)
        if (!res.ok) return
        const data = await res.json()
        setAlerts(Array.isArray(data.alerts) ? data.alerts : [])
      } catch {
        // ignore
      }
    }

    fetchAlerts()
    const interval = setInterval(fetchAlerts, 12000)
    return () => clearInterval(interval)
  }, [])

  const stats = useMemo(() => {
    const last = alerts.slice(-12)
    const counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 }
    for (const a of last) {
      const sev = String(a?.severity || "").toUpperCase()
      if (counts[sev] !== undefined) counts[sev] += 1
    }
    return { last, counts }
  }, [alerts])

  return (
    <div className="container">
      <PageHeader title="Visualization" subtitle="Quick stats and core widgets" onToggleSidebar={onToggleSidebar} isSidebarOpen={isSidebarOpen} />

      <div className="dashboard-grid" style={{ gridTemplateRows: "auto minmax(260px, 1fr)", alignItems: "start" }}>

        {/* Top: simple stats charts */}
        <div className="card card--blue dashboard-grid--full">
          <div className="title">Live Statistics</div>
          <p className="subtitle">Last 12 alerts summary</p>

          <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: "12px", marginTop: "10px" }}>
            <MiniBars counts={stats.counts} />
            <MiniRing counts={stats.counts} />
          </div>
        </div>

        {/* Bottom: widgets (kept at bottom in 2nd row) */}
        <HoneytokenPanel className="card--sunset" />
        <IpLocator className="card--pink" />

      </div>
    </div>
  )
}

function MiniBars({ counts }) {
  const max = Math.max(1, counts.CRITICAL, counts.HIGH, counts.MEDIUM, counts.LOW)
  const items = [
    { k: "CRITICAL", c: "var(--pk)" },
    { k: "HIGH", c: "var(--or)" },
    { k: "MEDIUM", c: "var(--ly)" },
    { k: "LOW", c: "var(--rb)" }
  ]

  return (
    <div style={{ border: "1px solid var(--line)", borderRadius: "12px", padding: "10px 12px", background: "rgba(255,255,255,0.55)" }}>
      <div style={{ fontSize: "12px", fontWeight: 800, color: "var(--ink)" }}>Severity Bars</div>
      <div style={{ display: "grid", gap: "8px", marginTop: "10px" }}>
        {items.map(({ k, c }) => {
          const v = counts[k]
          const w = Math.round((v / max) * 100)
          return (
            <div key={k} style={{ display: "grid", gridTemplateColumns: "78px 1fr 24px", alignItems: "center", gap: "10px" }}>
              <div style={{ fontSize: "11px", color: "var(--muted)", fontWeight: 700 }}>{k}</div>
              <div style={{ height: "10px", borderRadius: "999px", background: "rgba(20,25,40,0.08)", overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${w}%`, background: `linear-gradient(90deg, ${c}, rgba(255,255,255,0.0))` }} />
              </div>
              <div style={{ fontSize: "11px", color: "var(--ink)", fontWeight: 800 }}>{v}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function MiniRing({ counts }) {
  const total = counts.CRITICAL + counts.HIGH + counts.MEDIUM + counts.LOW || 1
  const pct = {
    CRITICAL: (counts.CRITICAL / total) * 100,
    HIGH: (counts.HIGH / total) * 100,
    MEDIUM: (counts.MEDIUM / total) * 100,
    LOW: (counts.LOW / total) * 100
  }

  const segments = [
    { p: pct.CRITICAL, c: "var(--pk)" },
    { p: pct.HIGH, c: "var(--or)" },
    { p: pct.MEDIUM, c: "var(--ly)" },
    { p: pct.LOW, c: "var(--rb)" }
  ]

  let acc = 0
  const stops = segments.map((s) => {
    const start = acc
    acc += s.p
    return { ...s, start, end: acc }
  })

  const conic = `conic-gradient(${stops.map(s => `${s.c} ${s.start}% ${s.end}%`).join(",")})`

  return (
    <div style={{ border: "1px solid var(--line)", borderRadius: "12px", padding: "10px 12px", background: "rgba(255,255,255,0.55)" }}>
      <div style={{ fontSize: "12px", fontWeight: 800, color: "var(--ink)" }}>Distribution</div>

      <div style={{ display: "flex", gap: "12px", alignItems: "center", marginTop: "10px" }}>
        <div style={{ width: "86px", height: "86px", borderRadius: "999px", background: conic, position: "relative" }}>
          <div style={{ position: "absolute", inset: "10px", borderRadius: "999px", background: "rgba(255,255,255,0.92)", border: "1px solid var(--line)" }} />
          <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center", fontSize: "12px", fontWeight: 900, color: "var(--ink)" }}>
            {total}
          </div>
        </div>

        <div style={{ display: "grid", gap: "6px" }}>
          <LegendDot label="Critical" color="var(--pk)" />
          <LegendDot label="High" color="var(--or)" />
          <LegendDot label="Medium" color="var(--ly)" />
          <LegendDot label="Low" color="var(--rb)" />
        </div>
      </div>
    </div>
  )
}

function LegendDot({ label, color }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "12px", color: "var(--muted)" }}>
      <span style={{ width: "10px", height: "10px", borderRadius: "999px", background: color, boxShadow: "0 6px 14px rgba(0,0,0,0.10)" }} />
      <span style={{ fontWeight: 700 }}>{label}</span>
    </div>
  )
}

