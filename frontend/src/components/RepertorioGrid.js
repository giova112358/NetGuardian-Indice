import React, { useEffect, useState } from 'react';
import { fetchRepertori } from '../api/client';
import RepertorioCard from './RepertorioCard';

const RepertorioGrid = () => {
  const [repertori, setRepertori] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchRepertori();
        setRepertori(data);
      } catch (err) {
        setError("Impossibile caricare i repertori. Assicurati che il backend sia attivo.");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <div className="loading">Caricamento in corso...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="grid-container">
      {Object.entries(repertori).map(([code, data]) => (
        <RepertorioCard key={code} code={code} data={data} />
      ))}
    </div>
  );
};

export default RepertorioGrid;