// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import RepertorioGrid from './components/RepertorioGrid';
import Interazioni from './components/Interazioni';
import RiskResult from './components/RischioTable'; 
import Indice from './components/Indice';
import IndiceResult from './components/IndiceTable';

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>NetGuardian - Indice </h1>
          <nav className="app-nav">
            <Link to="/" className="nav-link">Mappa repertori</Link>
            <Link to="/interazioni" className="nav-link">Interazioni</Link>
            <Link to="/indice" className="nav-link">Indice</Link>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<RepertorioGrid />} />
            <Route path="/interazioni" element={<Interazioni />} />
            <Route path="/risultato" element={<RiskResult />} />
            <Route path="/indice" element={<Indice />} />
            <Route path="/risultato-indice" element={<IndiceResult />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;