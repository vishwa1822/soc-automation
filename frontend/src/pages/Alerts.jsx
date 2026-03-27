import AlertTable from "../components/AlertTable"
import PageHeader from "../components/PageHeader"

export default function Alerts({ onToggleSidebar, isSidebarOpen }) {
  return (
    <div className="container">
      <PageHeader title="Alerts" subtitle="Detections and system-generated alerts" onToggleSidebar={onToggleSidebar} isSidebarOpen={isSidebarOpen} />

      <div className="dashboard-grid" style={{ gridTemplateRows: "1fr" }}>
        <div className="dashboard-grid--full">
          <AlertTable className="card--pink" />
        </div>
      </div>
    </div>
  )
}

