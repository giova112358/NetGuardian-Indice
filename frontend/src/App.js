import React from 'react';
import './App.css';
import RepertorioGrid from './components/RepertorioGrid';

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>NetGuardian - Indice Repertori</h1>
        <p>Visualizzazione interattiva della mappa dei repertori</p>
      </header>
      <main>
        <RepertorioGrid />
      </main>
    </div>
  );
}

export default App;