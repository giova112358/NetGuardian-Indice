from fastapi import APIRouter, Depends, HTTPException
from backend.schemas import IndiceRequest
from backend.dependencies import get_repertori_data
from backend.core.erc import calcolo_livelli, calcolo_spostamento, calcolo_stazionarieta, calcolo_erc
import pandas as pd
import json


router = APIRouter(prefix="/indice", tags=["Interactions"])


@router.post("/misure")
def get_misure(request: IndiceRequest, repertori_data=Depends(get_repertori_data)):
    """
    Generates the interaction table for a given triplet.
    """
    # Extract data from request
    repertori = request.repertori

    # Calculate levels
    livelli, triplets = calcolo_livelli(repertori)

    # Calculate spostamento
    spostamento, distanza, direzione = calcolo_spostamento(livelli)
    # spostamento = 0.0

    # Calculate stazionarietà
    stazionarieta, ripetizioni = calcolo_stazionarieta(livelli)
    # stazionarieta = 0.0

    # Calculate misura_erc
    alpha = 1
    beta = 1
    misura_erc = calcolo_erc(spostamento, stazionarieta, alpha, beta)

    # Return calculations
    return {
        "triplette": triplets,  
        "livelli": livelli,
        "distanze": distanza,
        "direzioni": direzione,
        "ripetizioni": ripetizioni,
        "spostamento": spostamento,
        "stazionarieta": stazionarieta,
        "misura_erc": misura_erc,
    }
