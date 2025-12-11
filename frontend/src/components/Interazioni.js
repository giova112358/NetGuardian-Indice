// src/components/IndiceRischio.js
import React, { useState } from 'react';
import { fetchRepertoriNames, fetchInteractions } from '../api/client';
import { useNavigate } from 'react-router-dom'; 

const Interazioni = () => {
  const [selection, setSelection] = useState("");
  const [savedValues, setSavedValues] = useState([]);
  const [repertoriNames, setRepertoriNames] = useState([]);

  const navigate = useNavigate(); 
  const MAX_SELECTIONS = 3;
  const isFull = savedValues.length >= MAX_SELECTIONS;

  const getRepertoriNames = async () => {
    try {
      const response = await fetchRepertoriNames();
      setRepertoriNames(response);
    } catch (error) {
      console.error("Errore nel recupero dei nomi dei repertori:", error);
    }
  };

  React.useEffect(() => {
    getRepertoriNames();
  }, []);

  const handleAdd = () => {
    // Check both if selection exists and if we are under the limit
    if (selection && !isFull) {
      // Prevent duplicates if necessary (optional, but good UX)
      if (!savedValues.includes(selection)) {
        setSavedValues([...savedValues, selection]);
        setSelection(""); 
      }
    }
  };

  const handleRemove = (indexToRemove) => {
    setSavedValues(savedValues.filter((_, index) => index !== indexToRemove));
  };

  const handleCalculate = async () => {
    try {
      const interactions = await fetchInteractions(savedValues);
      navigate('/risultato', { state: { data: interactions } });
    } catch (error) {
      console.error("Errore nel calcolo delle interazioni:", error);
    }
  };

  return (
    <div className="risk-container">
      <div className="card risk-card">
        <div className="card-header">
          <div className="code-circle" style={{ backgroundColor: '#e67e22' }}>R</div>
          <div className="header-info">
            <h3 className="original-name">Calcolo Interazione</h3>
            <span className="type-badge badge-orange">Input Dati</span>
          </div>
        </div>
        
        <div className="card-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h4 className="usage-title">Seleziona Repertorio</h4>
            {/* UX Improvement: Counter Badge */}
            <span className={`counter-badge ${isFull ? 'full' : ''}`}>
              {savedValues.length} / {MAX_SELECTIONS}
            </span>
          </div>
          
          <div className="risk-input-group">
            <select 
              className="risk-select" 
              value={selection} 
              onChange={(e) => setSelection(e.target.value)}
              disabled={isFull} // Disable input when limit reached
            >
              <option value="" disabled>
                {isFull ? "Limite raggiunto (3/3)" : "Scegli un repertorio..."}
              </option>
              {repertoriNames.map((name, index) => (
                <option 
                  key={index} 
                  value={name}
                  disabled={savedValues.includes(name)} // Gray out already selected items
                >
                  {name}
                </option>
              ))}
            </select>

            <button 
              className="btn-add" 
              onClick={handleAdd}
              disabled={!selection || isFull}
            >
              Aggiungi
            </button>
            
            <button 
              className="btn-calc" 
              onClick={handleCalculate}
              disabled={savedValues.length < 3}
            >
              Calcola
            </button>
          </div>

          {savedValues.length > 0 && (
            <div className="risk-list-container">
              <h4 className="usage-title" style={{ marginTop: '2rem' }}>Valori Inseriti</h4>
              <ul className="risk-list">
                {savedValues.map((val, index) => (
                  <li key={index} className="risk-list-item">
                    <span className="level-chars">{val}</span>
                    {/* UX Improvement: Delete Button */}
                    <button 
                      className="btn-remove"
                      onClick={() => handleRemove(index)}
                      title="Rimuovi voce"
                    >
                      &times;
                    </button>
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

export default Interazioni;