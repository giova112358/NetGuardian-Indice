import numpy as np
from typing import Any, List
from itertools import groupby
from backend.core.interactions import generate_interactions_table
from backend.config import REPERTORI_FILE
from backend.core.repertori import load_repertori


def get_triplets(input_list):
    """
    Get triplets from a list using zip, overlapping by 2 elements.

    Args:
        input_list: List of elements to form triplets from.
    Returns:
        List of triplets formed from the input list.
    """

    return list(zip(input_list, input_list[1:], input_list[2:]))


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
    repertori_data = load_repertori(REPERTORI_FILE)

    # Get all triplets
    triplets = get_triplets(repertori)
    triplets_filtered = check_triplets_nullo(triplets, repertori_data)

    if not triplets_filtered:
        return []

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
        results[triplet] = max_levels

        mapping = {"Minimo": 1, "Medio": 2, "Medio-alto": 3, "Alto": 4}
        mapped_levels = [mapping.get(l, l) for l in max_levels]

        levels.append(mapped_levels[0])  # TODO: handle ties properly
    print(f"Triplets Levels: {results}")
    print("")

    print(f"Levels: {levels}")
    print("")

    return levels


def calcolo_spostamento(livelli: List[int]) -> float:
    """
    Spostamento calculation based on levels.

    Args:
        livelli: List of numerical levels.
    Returns:
        Spostamento value as a float.
    """
    # Differenza
    differenza = [livelli[i + 1] - livelli[i] for i in range(len(livelli) - 1)]

    print(f"Differenza: {differenza}")
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
    distanza = [d**2 for d in differenza]

    print(f"Distanza: {distanza}")
    print("")

    # Spostamento
    spostamenti = np.array(direzione) * np.array(distanza)
    spostamento = np.sum(spostamenti)

    return float(spostamento)


def calcolo_stazionarieta(livelli: List[int]) -> float:
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

    chi = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

    temp = []
    for key, value in ripetizioni.items():
        temp.append(chi[key] * value)

    print(f"Temp: {temp}")
    print("")
    stazionarieta = sum(temp)

    return float(stazionarieta)


if __name__ == "__main__":
    sample_list = [1, 2, 3, 4, 5, 1, 2, 3]

    triplets_zip = get_triplets(sample_list)

    print(f"Input List: {sample_list}")
    print(f"Triplets using zip: {triplets_zip}")
