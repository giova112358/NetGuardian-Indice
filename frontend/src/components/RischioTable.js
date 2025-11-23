// src/components/RiskResult.js
import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const RiskResult = () => {
  const location = useLocation();
  const data = location.state?.data;

  if (!data) {
    return (
      <div className="risk-container">
        <div className="card risk-card">
          <div className="card-body" style={{ textAlign: 'center' }}>
            <h3>Nessun risultato disponibile</h3>
            <Link to="/rischio" className="btn-add" style={{ textDecoration: 'none' }}>
              Torna al calcolo
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const allRows = Object.values(data);
  const headers = allRows.length > 0 ? Object.keys(allRows[0]) : [];

  const maxCopertura = Math.max(
    ...allRows.map((row) => parseFloat(row.Copertura) || 0)
  );

  return (
    <div className="risk-container">
      <div className="card risk-card">
        <div className="card-header">
          <div className="code-circle" style={{ backgroundColor: '#2ecc71' }}>✓</div>
          <div className="header-info">
            <h3 className="original-name">Risultati Interazione</h3>
            <span className="type-badge badge-green">Report Completo</span>
          </div>
        </div>

        <div className="card-body">
          <div className="table-responsive">
            <table className="result-table">
              <thead>
                <tr>
                  <th>Livello</th>
                  {headers.map((header) => (
                    <th key={header}>{header}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.entries(data).map(([level, details]) => {
                  const currentValue = parseFloat(details.Copertura) || 0;
                  const isHighlight = currentValue === maxCopertura && maxCopertura > 0;

                  return (
                    <tr 
                      key={level} 
                      className={isHighlight ? "highlight-row" : ""}
                    >
                      <td className="level-cell">{level}</td>
                      {headers.map((header) => (
                        <td key={`${level}-${header}`}>
                          {details[header] ? (
                            <span className="data-value">{details[header]}</span>
                          ) : (
                            <span className="empty-value">-</span>
                          )}
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          
          <div style={{ marginTop: '2rem', textAlign: 'right' }}>
             <Link to="/rischio" className="btn-add" style={{ textDecoration: 'none', display: 'inline-block' }}>
               Nuovo Calcolo
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskResult;