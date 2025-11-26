from fastapi import APIRouter, Depends, HTTPException
from backend.schemas import IndiceRequest
from backend.dependencies import get_repertori_data
from backend.core.interactions import generate_interactions_table
import pandas as pd
import json

router = APIRouter(prefix="/indice", tags=["Interactions"])


@router.post("/misure")
def generate_table(request: IndiceRequest, repertori_data=Depends(get_repertori_data)):
    """
    Generates the interaction table for a given triplet.
    """

    spostamento = 0.5
    stazionarietà = 0.5
    misura_erc = 0.5

    # Return calculations
    return {
        "spostamento": spostamento,
        "stazionarietà": stazionarietà,
        "misura_erc": misura_erc,
    }
