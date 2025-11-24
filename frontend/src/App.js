// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import RepertorioGrid from './components/RepertorioGrid';
import IndiceRischio from './components/IndiceRischio';
import RiskResult from './components/RischioTable'; 

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>NetGuardian - Indice </h1>
          <nav className="app-nav">
            <Link to="/" className="nav-link">Mappa repertori</Link>
            <Link to="/rischio" className="nav-link">Interazioni</Link>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<RepertorioGrid />} />
            <Route path="/rischio" element={<IndiceRischio />} />
            <Route path="/risultato" element={<RiskResult />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;