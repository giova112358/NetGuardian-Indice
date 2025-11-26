from pydantic import BaseModel
from typing import List, Dict, Optional, Any


# Schema for a single Repertorio
class Repertorio(BaseModel):
    original: str
    type: str
    usage: Optional[Dict[str, List[str]]] = None


# Request body for generating interactions
class InteractionRequest(BaseModel):
    triplet: List[str]


# Request body for indice calculation
class IndiceRequest(BaseModel):
    repertori: List[str]
