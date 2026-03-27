import { useState } from "react"
import Sidebar from "./components/Sidebar"
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import Workspace from "./pages/Workspace"
import Alerts from "./pages/Alerts"
import Visualization from "./pages/Visualization"
import Soar from "./pages/Soar"

function App() {
  // Explorer is hidden until user taps hamburger
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const toggleSidebar = () => setSidebarOpen((prev) => !prev)

  return (
    <BrowserRouter>
      <div className="app-root">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        <main className={`main ${sidebarOpen ? "main--shift" : ""}`.trim()}>
          <Routes>
            <Route path="/" element={<Navigate to="/home" replace />} />
            <Route path="/home" element={<Workspace onToggleSidebar={toggleSidebar} isSidebarOpen={sidebarOpen} />} />
            <Route path="/workspace" element={<Navigate to="/home" replace />} />
            <Route path="/visualization" element={<Visualization onToggleSidebar={toggleSidebar} isSidebarOpen={sidebarOpen} />} />
            <Route path="/alerts" element={<Alerts onToggleSidebar={toggleSidebar} isSidebarOpen={sidebarOpen} />} />
            <Route path="/soar" element={<Soar onToggleSidebar={toggleSidebar} isSidebarOpen={sidebarOpen} />} />
            <Route path="*" element={<Navigate to="/home" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App

