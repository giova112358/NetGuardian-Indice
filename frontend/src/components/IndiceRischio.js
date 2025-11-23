// src/components/IndiceRischio.js
import React, { useState } from 'react';
import { fetchRepertoriNames, fetchInteractions } from '../api/client';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const IndiceRischio = () => {
  const [selection, setSelection] = useState("");
  const [savedValues, setSavedValues] = useState([]);
  const [repertoriNames, setRepertoriNames] = useState([]);

  const navigate = useNavigate(); 

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
    if (selection) {
      setSavedValues([...savedValues, selection]);
      setSelection(""); 
    }
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
              <option value="" disabled>Scegli un repertorio...</option>
              {repertoriNames.map((name, index) => (
                <option key={index} value={name}>{name}</option>
              ))}
            </select>

            <button 
              className="btn-add" 
              onClick={handleAdd}
              disabled={!selection}
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