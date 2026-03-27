export default function PageHeader({ title, subtitle, onToggleSidebar, isSidebarOpen }) {
  return (
    <div className="header">
      <div className="workspace-header">
        {!isSidebarOpen && (
          <button
            className="hamburger"
            type="button"
            onClick={onToggleSidebar}
            aria-label="Open Explorer"
            title="Open Explorer"
          >
            <span />
            <span />
            <span />
          </button>
        )}

        <div className="logo" aria-hidden="true">
          <img className="logo-img" src="/logo.png" alt="Sentinel SOC logo" />
        </div>

        <div>
          <h1 className="soc-title">{title}</h1>
          <p className="soc-subtitle">{subtitle}</p>
        </div>
      </div>
    </div>
  )
}
