from functools import lru_cache
from fastapi import HTTPException
from backend.config import REPERTORI_FILE
from backend.core.repertori import load_repertori


# lru_cache ensures we read the file only once, not on every request
@lru_cache()
def get_repertori_data():
    data = load_repertori(REPERTORI_FILE)
    if not data:
        raise HTTPException(status_code=500, detail="Could not load repertori data")
    return data
