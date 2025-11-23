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

export const fetchRepertoriNames = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/repertori/names`);
    if (!response.ok) {
      throw new Error("Errore nel recupero dei nomi dei repertori");
    }
    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

export const fetchInteractions = async (selectedRepertori) => {
  try {
    const response = await fetch(`${API_BASE_URL}/interactions/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ triplet: selectedRepertori }), 
    });

    if (!response.ok) {
      throw new Error("Errore nel recupero delle interazioni");
    }
    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};