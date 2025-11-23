// src/components/IndiceRischio.js
import React, { useState } from 'react';

const IndiceRischio = () => {
  const [selection, setSelection] = useState("");
  const [savedValues, setSavedValues] = useState([]);

  const handleAdd = () => {
    if (selection) {
      setSavedValues([...savedValues, selection]);
      setSelection(""); // Optional: Reset dropdown after adding
    }
  };

  return (
    <div className="risk-container">
      <div className="card risk-card">
        <div className="card-header">
          <div className="code-circle" style={{ backgroundColor: '#e67e22' }}>R</div>
          <div className="header-info">
            <h3 className="original-name">Calcolo Indice</h3>
            <span className="type-badge badge-orange">Input Dati</span>
          </div>
        </div>
        
        <div className="card-body">
          <h4 className="usage-title">Seleziona Parametro</h4>
          
          <div className="risk-input-group">
            <select 
              className="risk-select" 
              value={selection} 
              onChange={(e) => setSelection(e.target.value)}
            >
              <option value="" disabled>Scegli un valore...</option>
              <option value="PZ">PZ</option>
              <option value="VA">VA</option>
              <option value="GZ">GZ</option>
            </select>

            <button 
              className="btn-add" 
              onClick={handleAdd}
              disabled={!selection}
            >
              Aggiungi
            </button>
          </div>

          {/* Display the list only if there are items */}
          {savedValues.length > 0 && (
            <div className="risk-list-container">
              <h4 className="usage-title" style={{ marginTop: '2rem' }}>Valori Inseriti</h4>
              <ul className="risk-list">
                {savedValues.map((val, index) => (
                  <li key={index} className="risk-list-item">
                    <span className="level-chars">{val}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default IndiceRischio;