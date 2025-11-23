// src/api/client.js
const API_BASE_URL = "http://localhost:8000";

export const fetchRepertori = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/repertori/`);
    if (!response.ok) {
      throw new Error("Errore nel recupero dei dati");
    }
    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};