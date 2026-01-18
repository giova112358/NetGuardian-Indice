from fastapi import APIRouter, Depends
from backend.schemas import IndiceRequest
from backend.dependencies import get_repertori_data
from backend.core.erc import (
    calcolo_livelli, calcolo_spostamento,
    calcolo_erc, compute_stationarity_enhanced
)

router = APIRouter(prefix="/indice", tags=["Interactions"])

@router.post("/misure")
def get_misure(request: IndiceRequest, repertori_data=Depends(get_repertori_data)):
    """
    Calcola tutte le misure ERC, inclusa quella enhancata.
    """
    repertori = request.repertori
    
    # 1. Calcola livelli
    livelli, triplets = calcolo_livelli(repertori)
    
    # 2. Calcola spostamento (ora CORRETTO: somma)
    spostamento, distanza, direzione, spostamenti = calcolo_spostamento(livelli)
    
    # 3. Calcola stazionarietà enhancata (NUOVA formula con coupling)
    stazionarieta_enhanced = compute_stationarity_enhanced(
        livelli, spostamenti, λ=0.3, k_sat=5
    )
    
    # 4. Calcola ERC 
    alpha = 0.5
    beta = 0.5
    lambda_final = 1.0

    # Calcola livello massimo raggiunto
    num_messages = len(repertori)
    
    misura_erc = calcolo_erc(
        stazionarieta_enhanced,
    )
    
    # 5. Classifica rischio
    if misura_erc < 0.35:
        livello_rischio = "MINIMO"
    elif misura_erc < 0.60:
        livello_rischio = "MEDIO"
    elif misura_erc < 0.80:
        livello_rischio = "MEDIO-ALTO"
    else:
        livello_rischio = "ALTO"
    
    return {
        "triplette": triplets,
        "livelli": livelli,
        "distanze": distanza,
        "direzioni": direzione,
        "spostamento": spostamento,
        "spostamenti_vettore": spostamenti,
        "stazionarieta": round(stazionarieta_enhanced, 4),
        "misura_erc": round(misura_erc, 4),
        "parametri_erc": {
            "alpha": alpha,
            "beta": beta,
            "lambda_final": lambda_final
        }
    }
