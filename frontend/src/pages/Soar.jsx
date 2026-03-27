import PageHeader from "../components/PageHeader"

export default function Soar({ onToggleSidebar, isSidebarOpen }) {
  return (
    <div className="container">
      <PageHeader title="SOAR" subtitle="Reserved for future automation playbooks" onToggleSidebar={onToggleSidebar} isSidebarOpen={isSidebarOpen} />

      <div className="dashboard-grid" style={{ gridTemplateRows: "1fr" }}>
        <div className="card card--sunset dashboard-grid--full">
          <div className="title">Coming soon</div>
          <p className="subtitle">
            This section will host response workflows (containment, enrichment, ticketing, notifications).
          </p>
        </div>
      </div>
    </div>
  )
}

