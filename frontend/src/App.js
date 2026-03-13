import React, { useState, useEffect } from "react";
import "./App.css";
import { ThemeProvider, useTheme } from "./context/ThemeContext";
import Sidebar from "./components/Sidebar/Sidebar";
import Header from "./components/Header/Header";
import GraphPlaceholder from "./components/Graph/GraphPlaceholder";
import ChatPanel from "./components/Chat/ChatPanel";

function AppInner() {
  const { isDark } = useTheme();

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 492);

  /* Detect screen resize */
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 492);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  /* Sidebar open */
  const handleOpen = () => {
    if (isMobile) setMobileOpen(true);
    else setSidebarOpen(true);
  };

  /* Sidebar close */
  const handleClose = () => {
    if (isMobile) setMobileOpen(false);
    else setSidebarOpen(false);
  };

  return (
    <div className={`app-root ${isDark ? "dark" : "light"}`}>

      {/* Mobile overlay */}
      <div
        className={`sidebar-overlay ${mobileOpen ? "visible" : ""}`}
        onClick={() => setMobileOpen(false)}
      />

      {/* Sidebar */}
      <div className={`sidebar-wrap ${mobileOpen ? "sidebar-open" : ""}`}>
        <Sidebar
          isOpen={isMobile ? mobileOpen : sidebarOpen}
          onOpen={handleOpen}
          onClose={handleClose}
        />
      </div>

      {/* Main Layout */}
      <div className="main-area">

        <div className="center-col">
          <Header
            sidebarOpen={isMobile ? mobileOpen : sidebarOpen}
            onOpenSidebar={handleOpen}
          />

          <div className="graph-wrap">
            <GraphPlaceholder />
          </div>
        </div>

        <div className="chat-wrap">
          <ChatPanel />
        </div>

      </div>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AppInner />
    </ThemeProvider>
  );
}

export default App;