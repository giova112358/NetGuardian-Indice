from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from backend.schemas import Repertorio
from backend.dependencies import get_repertori_data

router = APIRouter(prefix="/repertori", tags=["Repertori"])


@router.get("/", response_model=Dict[str, Repertorio])
def list_repertori(data: dict = Depends(get_repertori_data)):
    """Get all repertories."""
    return data


@router.get("/names", response_model=List[str])
def list_repertori_names(data: dict = Depends(get_repertori_data)):
    """Get all repertories names."""
    return list(data.keys())


@router.get("/ntgnames", response_model=List[str])
def list_repertori_names(data: dict = Depends(get_repertori_data)):
    """Get all repertories names."""
    names = [name for name in data.keys() if name not in ["AN", "CO", "DR", "PR", "GI"]]
    return names


@router.get("/{code}", response_model=Repertorio)
def get_repertorio(code: str, data: dict = Depends(get_repertori_data)):
    """Get a specific repertorio."""
    if code not in data:
        raise HTTPException(status_code=404, detail="Repertorio not found")
    return data[code]
