from fastapi import APIRouter, Depends, HTTPException
from backend.schemas import IndiceRequest
from backend.dependencies import get_repertori_data
from backend.core.interactions import generate_interactions_table
from backend.core.erc import calcolo_livelli, calcolo_spostamento, calcolo_stazionarieta
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
    livelli = calcolo_livelli(repertori)

    # Calculate spostamento
    spostamento = calcolo_spostamento(livelli)
    # spostamento = 0.0

    # Calculate stazionarietà
    stazionarieta = calcolo_stazionarieta(livelli)
    # stazionarieta = 0.0

    # Calculate misura_erc
    alpha = 1
    beta = 1
    misura_erc = alpha * spostamento + beta * stazionarieta
    # misura_erc = 0.0

    # Return calculations
    return {
        "spostamento": spostamento,
        "stazionarieta": stazionarieta,
        "misura_erc": misura_erc,
    }
