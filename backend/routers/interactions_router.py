from fastapi import APIRouter, Depends, HTTPException
from backend.schemas import InteractionRequest
from backend.dependencies import get_repertori_data
from backend.core.interactions import generate_interactions_table
import pandas as pd
import json

router = APIRouter(prefix="/interactions", tags=["Interactions"])


@router.post("/generate")
def generate_table(
    request: InteractionRequest, data: dict = Depends(get_repertori_data)
):
    """
    Generates the interaction table for a given triplet.
    """
    if len(request.triplet) != 3:
        raise HTTPException(
            status_code=400, detail="Please provide exactly 3 repertori codes."
        )

    # Validate that all codes exist in data
    for code in request.triplet:
        if code not in data:
            raise HTTPException(
                status_code=404, detail=f"Repertorio code '{code}' not found."
            )

    # Call your existing core logic
    try:
        df = generate_interactions_table(tuple(request.triplet), data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Convert Pandas DataFrame to a JSON-friendly format
    if df is None:
        return {}
    result = df.to_dict(orient="index")
    return result
