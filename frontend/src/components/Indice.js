import React, { useState } from 'react';
import { fetchRepertoriNames, fetchMisure } from '../api/client';
import { useNavigate } from 'react-router-dom'; 

const Indice = () => {
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

  const handleRemove = (indexToRemove) => {
    setSavedValues(savedValues.filter((_, index) => index !== indexToRemove));
  };

  const handleCalculate = async () => {
    try {

      const result = await fetchMisure(savedValues);
      const dataToPass = {
        ...result,
        repertori: savedValues
      };
      navigate('/risultato-indice', { state: { data: dataToPass } });
    } catch (error) {
      console.error("Errore nel calcolo dell'indice:", error);
    }
  };

  return (
    <div className="risk-container">
      <div className="card risk-card">
        <div className="card-header">
          {/* Using Blue to differentiate from Interazioni (Orange) */}
          <div className="code-circle" style={{ backgroundColor: '#3498db' }}>I</div>
          <div className="header-info">
            <h3 className="original-name">Calcolo Indice</h3>
            <span className="type-badge badge-blue">Analisi Multipla</span>
          </div>
        </div>
        
        <div className="card-body">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h4 className="usage-title">Aggiungi Repertori</h4>
            <span className="counter-badge">
              Totale: {savedValues.length}
            </span>
          </div>
          
          <div className="risk-input-group">
            <select 
              className="risk-select" 
              value={selection} 
              onChange={(e) => setSelection(e.target.value)}
            >
              <option value="" disabled>Scegli un repertorio...</option>
              {repertoriNames.map((name, index) => (
                <option 
                  key={index} 
                  value={name}
                >
                  {name}
                </option>
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
              disabled={savedValues.length === 0}
            >
              Calcola
            </button>
          </div>

          {/* Matrix Layout Container */}
          {savedValues.length > 0 && (
            <div style={{ 
              marginTop: '2rem', 
              borderTop: '1px solid #eee', 
              paddingTop: '1rem' 
            }}>
              <h4 className="usage-title">Elementi Selezionati</h4>
              
              <div style={{ 
                display: 'flex', 
                flexWrap: 'wrap', 
                gap: '10px',
                alignItems: 'center'
              }}>
                {savedValues.map((val, index) => (
                  <div 
                    key={index} 
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      backgroundColor: '#f8f9fa',
                      border: '1px solid #ddd',
                      borderRadius: '8px',
                      padding: '0.5rem 1rem',
                      boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
                      transition: 'all 0.2s ease',
                      minWidth: '150px'
                    }}
                  >
                    <span className="level-chars" style={{ marginRight: '10px' }}>{val}</span>
                    <button 
                      className="btn-remove"
                      onClick={() => handleRemove(index)}
                      title="Rimuovi voce"
                      style={{ padding: 0 }}
                    >
                      &times;
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Indice;