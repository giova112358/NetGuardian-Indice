import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const IndiceResult = () => {
  const location = useLocation();
  const data = location.state?.data;

  // Fallback if accessed directly without data
  if (!data) {
    return (
      <div className="risk-container">
        <div className="card risk-card">
          <div className="card-body" style={{ textAlign: 'center', padding: '3rem' }}>
            <h3 style={{ color: '#666' }}>Nessun risultato disponibile</h3>
            <p>Effettua prima un calcolo dalla pagina Indice.</p>
            <Link to="/indice" className="btn-add" style={{ textDecoration: 'none', display: 'inline-block', marginTop: '1rem' }}>
              Vai al calcolo
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Destructure expected data. 
  // We handle potential casing differences or missing keys safely.
  const livelli = data.livelli;
  const differenze = data.differenze;
  const direzioni = data.direzioni;
  const ripetizioni = data.ripetizioni;
  const repertori = data.repertori || data.Repertori || [];
  const spostamento = data.Spostamento || data.spostamento || 0;
  const stazionarieta = data.Stazionarietà || data.stazionarieta || 0;
  const misuraErc = data['Misura ERC'] || data.misura_erc || 0;

  return (
    <div className="risk-container">
      <div className="card risk-card">
        {/* Header - Blue Theme for Indice */}
        <div className="card-header">
          <div className="code-circle" style={{ backgroundColor: '#3498db' }}>I</div>
          <div className="header-info">
            <h3 className="original-name">Risultati Indice</h3>
            <span className="type-badge badge-blue">Analisi Sintetica</span>
          </div>
        </div>

        <div className="card-body">
          
          {/* Section 1: Repertori Grid */}
          <div style={{ marginBottom: '2.5rem' }}>
            <h4 className="usage-title">Repertori Analizzati</h4>
            <div style={{ 
              display: 'flex', 
              flexWrap: 'wrap', 
              gap: '10px',
              padding: '1rem',
              backgroundColor: '#f8f9fa',
              borderRadius: '8px',
              border: '1px solid #eee'
            }}>
              {repertori.length > 0 ? (
                repertori.map((rep, index) => (
                  <div 
                    key={index} 
                    style={{
                      backgroundColor: 'rgba(52, 152, 219, 0.1)',
                      color: '#2980b9',
                      border: '1px solid rgba(52, 152, 219, 0.3)',
                      borderRadius: '6px',
                      padding: '0.5rem 1rem',
                      fontFamily: 'Courier New, monospace',
                      fontWeight: 'bold',
                      fontSize: '0.95rem'
                    }}
                  >
                    {rep}
                  </div>
                ))
              ) : (
                <span className="empty-value">Nessun repertorio specificato</span>
              )}
            </div>
          </div>

          <hr style={{ border: '0', borderTop: '1px solid #eee', margin: '2rem 0' }} />

          {/* Section 2: Indicatori Intermedi */}
          <div>
            <h4 className="usage-title">Indicatori Intermedi</h4>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
              gap: '1.5rem',
              marginTop: '1rem'
            }}>
              <ListMetricCard 
                label="Livelli" 
                values={livelli || []} 
                color="#9b59b6"
              />
              <ListMetricCard 
                label="Differenza" 
                values={differenze || []} 
                color="#3498db"
              />
              <ListMetricCard 
                label="Direzione" 
                values={direzioni || []} 
                color="#1abc9c"
              />
              <DictMetricCard 
                label="Ripetizioni" 
                data={ripetizioni || {}} 
                color="#e67e22"
              />
            </div>
          </div>

          <hr style={{ border: '0', borderTop: '1px solid #eee', margin: '2rem 0' }} />

          {/* Section 3: Indicatori Finali */}
          <div>
            <h4 className="usage-title">Indicatori Finali</h4>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
              gap: '1.5rem',
              marginTop: '1rem'
            }}>
              <MetricCard 
                label="Spostamento" 
                value={spostamento} 
                color="#e74c3c"
              />
              <MetricCard 
                label="Stazionarietà" 
                value={stazionarieta} 
                color="#f39c12"
              />
              <MetricCard 
                label="Misura ERC" 
                value={misuraErc} 
                color="#2ecc71"
              />
            </div>
          </div>

          {/* Footer Action */}
          <div style={{ marginTop: '3rem', textAlign: 'right' }}>
             <Link to="/indice" className="btn-add" style={{ textDecoration: 'none', display: 'inline-block' }}>
               Nuovo Calcolo
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper Sub-component for consistent metric cards
const MetricCard = ({ label, value, color }) => (
  <div style={{
    backgroundColor: '#fff',
    border: '1px solid #e0e0e0',
    borderRadius: '12px',
    padding: '1.5rem',
    textAlign: 'center',
    boxShadow: '0 4px 6px rgba(0,0,0,0.02)',
    transition: 'transform 0.2s',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center'
  }}>
    <h5 style={{ 
      margin: '0 0 1rem 0', 
      color: '#666', 
      textTransform: 'uppercase', 
      fontSize: '0.85rem',
      letterSpacing: '1px'
    }}>
      {label}
    </h5>
    <div style={{ 
      fontSize: '2.5rem', 
      fontWeight: '700', 
      color: color,
      fontFamily: 'Segoe UI, Roboto, sans-serif'
    }}>
      {/* Format number to max 3 decimals if it's a number */}
      {typeof value === 'number' ? value.toLocaleString('it-IT', { maximumFractionDigits: 3 }) : value}
    </div>
  </div>
);

// Helper Sub-component for dictionary-based metric cards (e.g., ripetizioni)
const DictMetricCard = ({ label, data, color }) => {
  const entries = Object.entries(data);
  return (
    <div style={{
      backgroundColor: '#fff',
      border: '1px solid #e0e0e0',
      borderRadius: '12px',
      padding: '1.5rem',
      boxShadow: '0 4px 6px rgba(0,0,0,0.02)',
      transition: 'transform 0.2s',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center'
    }}>
      <h5 style={{ 
        margin: '0 0 1rem 0', 
        color: '#666', 
        textTransform: 'uppercase', 
        fontSize: '0.85rem',
        letterSpacing: '1px'
      }}>
        {label}
      </h5>
      <div style={{ 
        display: 'flex',
        flexDirection: 'column',
        gap: '6px',
        width: '100%'
      }}>
        {entries.length > 0 ? (
          entries.map(([key, value], idx) => (
            <div 
              key={idx}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                backgroundColor: '#f8f9fa',
                borderRadius: '6px',
                padding: '0.5rem'
              }}
            >
              <span style={{
                color: '#666',
                fontSize: '0.9rem',
                fontWeight: '500'
              }}>
                Livello {key}
              </span>
              <span style={{
                backgroundColor: `${color}20`,
                color: color,
                border: `1px solid ${color}40`,
                borderRadius: '6px',
                padding: '0.25rem 0.6rem',
                fontFamily: 'Courier New, monospace',
                fontWeight: 'bold',
                fontSize: '0.95rem'
              }}>
                {value}
              </span>
            </div>
          ))
        ) : (
          <span style={{ color: '#ccc', fontStyle: 'italic', textAlign: 'center' }}>—</span>
        )}
      </div>
    </div>
  );
};

// Helper Sub-component for list-based metric cards
const ListMetricCard = ({ label, values, color }) => (
  <div style={{
    backgroundColor: '#fff',
    border: '1px solid #e0e0e0',
    borderRadius: '12px',
    padding: '1.5rem',
    boxShadow: '0 4px 6px rgba(0,0,0,0.02)',
    transition: 'transform 0.2s',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center'
  }}>
    <h5 style={{ 
      margin: '0 0 1rem 0', 
      color: '#666', 
      textTransform: 'uppercase', 
      fontSize: '0.85rem',
      letterSpacing: '1px'
    }}>
      {label}
    </h5>
    <div style={{ 
      display: 'flex',
      flexWrap: 'wrap',
      gap: '8px',
      justifyContent: 'center'
    }}>
      {values.length > 0 ? (
        values.map((val, idx) => (
          <span 
            key={idx}
            style={{
              backgroundColor: `${color}20`,
              color: color,
              border: `1px solid ${color}40`,
              borderRadius: '6px',
              padding: '0.4rem 0.8rem',
              fontFamily: 'Courier New, monospace',
              fontWeight: 'bold',
              fontSize: '1rem'
            }}
          >
            {typeof val === 'number' ? val.toLocaleString('it-IT', { maximumFractionDigits: 3 }) : val}
          </span>
        ))
      ) : (
        <span style={{ color: '#ccc', fontStyle: 'italic' }}>—</span>
      )}
    </div>
  </div>
);

export default IndiceResult;