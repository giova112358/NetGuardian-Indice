import numpy as np
from typing import Any, List, Tuple, Dict
from itertools import groupby
from backend.core.interactions import generate_interactions_table

from backend.core.repertori import load_repertori, load_momento_dialogico


def get_triplets(input_list):
    """
    Get triplets from a list using zip, overlapping by 2 elements.

    Args:
        input_list: List of elements to form triplets from.
    Returns:
        List of triplets formed from the input list.
    """
    #input_list_set = list(dict.fromkeys(input_list)) # Preserve the order but use set to dlete dplicates
    input_list_set = input_list
    if len(input_list_set) < 3:
        return []
    return list(zip(input_list_set, input_list_set[1:], input_list_set[2:]))


def check_triplets_nullo(triplets, data):
    """
    Remove triplets with more than one 'nullo' usage.
    Args:
        triplets: List of triplets.
        data: Dictionary with all the usages.
    Returns:
        Filtered list of triplets.
    """
    nullo_set = {"AN", "CO", "DR", "PR", "GI"}
    # Avoid mutating the input while iterating
    filtered = [
        triplet
        for triplet in triplets
        if sum(1 for item in triplet if item in nullo_set) <= 1
    ]
    return filtered


def calcolo_livelli(repertori: List[Any]):
    """
    Calculates levels for a list of repertori.
    Args:
        repertori: List of repertori.
    Returns:
        List of levels corresponding to each triplet.
    """
    if not repertori or len(repertori) < 3:
        return [], []

    repertori_data = load_repertori()

    # Get all triplets
    triplets = get_triplets(repertori)
    triplets_filtered = check_triplets_nullo(triplets, repertori_data)

    if not triplets_filtered:
        return [], []

    print(f"Triplets: {triplets}")
    print("")

    results = {}
    levels = []

    for triplet in triplets_filtered:
        # Generate the dataframe for triplet
        df = generate_interactions_table(triplet, repertori_data)

        # Find the maximum value in the 'Copertura' column
        max_value = df["Copertura"].max()

        # Find the levels (index) that correspond to this maximum value
        # We use a list in case there is a tie between levels
        max_levels = df[df["Copertura"] == max_value].index.tolist()

        # Store in dictionary
        results[tuple(triplet)] = max_levels

        mapping = {"Minimo": 1, "Medio": 2, "Medio-alto": 3, "Alto": 4}
        mapped_levels = [mapping.get(l, l) for l in max_levels]

        levels.append(mapped_levels[-1])  

    print(f"Triplets Levels: {results}")
    print("")

    print(f"Levels: {levels}")
    print("")

    # Convert results dict to a list of objects for JSON compatibility
    results_list = [
        {"triplet": list(triplet), "levels": levels}
        for triplet, levels in results.items()
    ]
    return levels, results_list

def calcolo_spostamento(livelli: List[int]) -> Tuple[float, List[float], List[int], List[float]]:
    """
    Calcola spostamento totale (SOMMA, non media).
    
    Returns:
      - spostamento_totale: float (somma di s_i)
      - distanze: List[float]
      - direzioni: List[int]
      - spostamenti: List[float] (per use in compute_stationarity_enhanced)
    """
    differenza = [livelli[i + 1] - livelli[i] for i in range(len(livelli) - 1)]
    momento_dialogico = load_momento_dialogico()
    livelli_momento = [momento_dialogico.get(level, 0) for level in livelli]
    differenza_momento = [
        abs(livelli_momento[i + 1] - livelli_momento[i])
        for i in range(len(livelli_momento) - 1)
    ]
    
    direzione = [
        -1 if diff < 0 else (1 if diff > 0 else 0)
        for diff in differenza
    ]
    
    distanza = [abs(d) for d in differenza_momento]
    spostamenti = np.array(direzione) * np.array(distanza)
    
    spostamento_totale = float(np.sum(spostamenti))
    
    return spostamento_totale, distanza, direzione, spostamenti.tolist()


def compute_stationarity_enhanced(levels: List[int], displacements: List[float], 
                                  λ=0.3, k_sat=5) -> float:
    """
    Calcola stazionarietà con coupling a spostamenti (formula migliorata).
    """
    MD = load_momento_dialogico()
    q = max(MD.values()) + 0.1
    gamma = {k: q - MD[k] for k in MD}
    
    episodes = []
    i = 0
    
    while i < len(levels):
        level = levels[i]
        start = i
        
        while i < len(levels) and levels[i] == level:
            i += 1
        
        duration = i - start
        
        # Accesso robusto a displacements
        if start == 0:
            s_entry = 0
        elif start - 1 < len(displacements):
            s_entry = displacements[start - 1]
        else:
            s_entry = 0
        
        episodes.append({
            'level': level,
            'duration': duration,
            's_entry': s_entry
        })
    
    T = 0
    for ep in episodes:
        level = ep['level']
        duration = ep['duration']
        s_entry = ep['s_entry']
        
        weight = gamma[level] + λ * abs(s_entry)
        contribution = weight * min(duration, k_sat)
        T += contribution
    
    return float(T)

def normalize_erc_tanh(erc, K=10):
    """
    K è la scala: valori > K saturano verso 1
    Consiglio: K = max_erc_osservato / 2
    """
    return np.tanh(erc / K)


def calcolo_erc(stazionarieta: float
                ) -> float:
    """
    Output: ∈ [0, 1]
    
    """
    ERC_raw = normalize_erc_tanh(stazionarieta)
    if ERC_raw <= 0:
        ERC_norm = 0.0
    else:
        ERC_norm = np.tanh(ERC_raw)
    
    return float(ERC_norm)