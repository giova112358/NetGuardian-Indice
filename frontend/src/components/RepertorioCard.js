import React from 'react';

const RepertorioCard = ({ code, data }) => {
  const { original, type, usage } = data;

  // Funzione per determinare il colore del badge in base al tipo
  const getTypeColor = (type) => {
    switch (type.toLowerCase()) {
      case 'generativo': return 'badge-green';
      case 'mantenimento': return 'badge-blue';
      case 'ibrido': return 'badge-orange';
      default: return 'badge-gray';
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="code-circle">{code}</div>
        <div className="header-info">
          <h3 className="original-name">{original}</h3>
          <span className={`type-badge ${getTypeColor(type)}`}>
            {type}
          </span>
        </div>
      </div>

      <div className="card-body">
        {usage ? (
          <div className="usage-container">
            <h4 className="usage-title">Livelli di Utilizzo</h4>
            <div className="usage-grid">
              {Object.entries(usage).map(([level, chars]) => (
                <div key={level} className="usage-item">
                  <span className="level-name">{level.replace('_', ' ')}:</span>
                  <span className="level-chars">
                    {chars.length > 0 ? chars.join(", ") : "-"}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="no-usage">
            <em>Nessun dato di utilizzo specifico</em>
          </div>
        )}
      </div>
    </div>
  );
};

export default RepertorioCard;