import { NavLink } from "react-router-dom"

export default function Sidebar({ isOpen = true, onClose }) {

  const linkClass = ({ isActive }) =>
    `sidebar-item ${isActive ? "sidebar-item--active" : ""}`.trim()

  const bigLinkClass = ({ isActive }) =>
    `sidebar-item sidebar-item--large ${isActive ? "sidebar-item--active" : ""}`.trim()

  return (

    <aside className={`sidebar ${isOpen ? "" : "sidebar--closed"}`.trim()}>

      <div className="sidebar-title" role="button" aria-label="Close Explorer" onClick={onClose}>
        Explorer
        <span className="sidebar-title-arrows" aria-hidden="true">
          <span className="sidebar-title-arrow">&#x276E;</span>
          <span className="sidebar-title-arrow">&#x276E;</span>
        </span>
      </div>

      <ul className="sidebar-menu">
        <li>
          <NavLink to="/workspace" className={linkClass}>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink to="/alerts" className={linkClass}>
            Alerts
          </NavLink>
        </li>
        <li>
          <NavLink to="/visualization" className={linkClass}>
            Visualization
          </NavLink>
        </li>
        <li>
          <NavLink to="/soar" className={linkClass}>
            SOAR
            <span className="sidebar-badge">&nbsp;future</span>
          </NavLink>
        </li>
      </ul>

    </aside>

  )

}

