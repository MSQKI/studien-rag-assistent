import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import {
  Home,
  MessageSquare,
  CreditCard,
  Network,
  Database,
} from 'lucide-react';

const Layout: React.FC = () => {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>Study Platform</h1>
          <p>Dein intelligenter Lernassistent</p>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Home />
            <span>Dashboard</span>
          </NavLink>

          <NavLink to="/rag" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <MessageSquare />
            <span>RAG Chat</span>
          </NavLink>

          <NavLink to="/flashcards" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <CreditCard />
            <span>Karteikarten</span>
          </NavLink>

          <NavLink to="/graph" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Network />
            <span>Knowledge Graph</span>
          </NavLink>

          <NavLink to="/data" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
            <Database />
            <span>Datenverwaltung</span>
          </NavLink>
        </nav>

        <div style={{ padding: '20px', marginTop: 'auto', opacity: 0.6, fontSize: '12px' }}>
          <p>v2.0.0</p>
          <p>Powered by OpenAI & Neo4j</p>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
