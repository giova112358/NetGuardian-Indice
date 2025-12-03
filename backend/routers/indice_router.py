from fastapi import APIRouter, HTTPException
from typing import List
from backend.schemas import InteractionRequest
from backend.dependencies import get_repertori_data
from backend.core.interactions import generate_interactions_table
from backend.core.erc import get_triplets
import pandas as pd
import json

router = APIRouter(prefix="/misure", tags=["Interactions"])


# --- The API Endpoint ---
@router.post("/calculate-misure")
async def calculate_misure(payload: List[str]):
    """ """
    try:

        result_triplets = get_triplets(payload)

        return {
            "status": "success",
            "original_count": len(payload),
            "triplets": result_triplets,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
