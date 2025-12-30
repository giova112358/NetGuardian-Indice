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
    input_list_set = list(dict.fromkeys(input_list)) # Preserve the order but use set to dlete dplicates
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


def calcolo_spostamento(livelli: List[int]) -> Tuple[float, List[int], List[int]]:
    """
    Spostamento calculation based on levels.

    Args:
        livelli: List of numerical levels.
    Returns:
        Spostamento value as a float.
    """
    # Differenza
    differenza = [livelli[i + 1] - livelli[i] for i in range(len(livelli) - 1)]

    # Differenza momenti dialogici
    momento_dialogico = load_momento_dialogico()
    livelli_momento = [momento_dialogico.get(level, 0) for level in livelli]
    differenza_momento = [
        abs(livelli_momento[i + 1] - livelli_momento[i])
        for i in range(len(livelli_momento) - 1)
    ]

    print(f"Differenza: {differenza}")
    print(f"Differenza Momenti Dialogici: {differenza_momento}")
    print("")

    # Direzione
    direzione = []
    for diff in differenza:
        if diff < 0:
            direzione.append(-1)
        elif diff > 0:
            direzione.append(1)
        else:
            direzione.append(0)

    print(f"Direzione: {direzione}")
    print("")

    # Distanza
    distanza = [abs(d) for d in differenza_momento]

    print(f"Distanza: {distanza}")
    print("")

    # Spostamento
    spostamenti = np.array(direzione) * np.array(distanza)
    spostamento = np.sum(spostamenti) / len(livelli)

    return float(spostamento), distanza, direzione


def calcolo_stazionarieta(livelli: List[int]) -> Tuple[float, List[int]]:
    """
    Stazionarietà calculation based on levels.

    Args:
        livelli: List of numerical levels.
    Returns:
        Stazionarietà value as a float.
    """

    def consecutive_repetitions(livelli):
        return {key: sum(1 for _ in group) for key, group in groupby(livelli)}

    ripetizioni = consecutive_repetitions(livelli)

    print(f"Ripetizioni consecutive: {ripetizioni}")
    print("")

    # Calcolo coefficienti per livelli stazionarietà
    
    chi = {1: 1, 2: 2, 3: 3, 4: 4}

    temp = []
    for key, value in ripetizioni.items():
        temp.append(chi[key] * value)

    print(f"Temp: {temp}")
    print("")
    stazionarieta = sum(temp) / len(livelli)
    print(f"Stazionarietà: {stazionarieta}")
    print("")

    return float(stazionarieta), ripetizioni

def calcolo_erc(spostamento, stazionarieta,  alpha=0.5, beta=0.5, scale_s=1.0, scale_t=1.0):
    """
    Normalizza S e T con sigmoid per ottenere ERC_normalized ∈ [0, 1]
    
    Args:
        S: spostamento totale (può essere negativo)
        T: stazionarietà totale (sempre positiva)
        alpha, beta: parametri di calibrazione
        scale: fattore di scaling per controllo della curvatura
    
    Returns:
        ERC_normalized: valore tra 0 e 1
    """
    # Ensure equal weighting (normalize alpha and beta to sum to 1)
    weight_sum = alpha + beta
    alpha_norm = alpha / weight_sum
    beta_norm = beta / weight_sum

    if spostamento <= 0:
        S_norm = 0
    else:
        # Normalize spostamento to [0, 1] using sigmoid
        # Negative values → [0, 0.5), zero → 0.5, positive values → (0.5, 1]
        S_norm = 1 / (1 + np.exp(-spostamento / scale_s))
    
    # Normalize stazionarieta to [0, 1] using sigmoid
    # Higher stationarity → values closer to 1
    T_norm = 1 / (1 + np.exp(-stazionarieta / scale_t))

    # Linear combination with normalized weights
    # Result is guaranteed to be in [0, 1] since both components are in [0, 1]
    #ERC = alpha_norm * S_norm + beta_norm * T_norm
    ERC = S_norm + T_norm

    # Applica sigmoid con scaling
    return float(ERC)


if __name__ == "__main__":
    sample_list = [1, 2, 3, 4, 5, 1, 2, 3]

    triplets_zip = get_triplets(sample_list)

    print(f"Input List: {sample_list}")
    print(f"Triplets using zip: {triplets_zip}")
