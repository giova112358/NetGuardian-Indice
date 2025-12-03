import numpy as np
from typing import List
from itertools import groupby


def get_triplets(input_list):
    """
    Get triplets from a list using zip, overlapping by 2 elements.

    Args:
        input_list: List of elements to form triplets from.
    Returns:
        List of triplets formed from the input list.
    """

    return list(zip(input_list, input_list[1:], input_list[2:]))


def calcolo_livelli():
    pass


def calcolo_spostamento(livelli: List[float]) -> float:
    """
    Spostamento calculation based on levels.

    Args:
        livelli: List of numerical levels.
    Returns:
        Spostamento value as a float.
    """
    # Differenza
    differenza = [livelli[i + 1] - livelli[i] for i in range(len(livelli) - 1)]

    # Direzione
    direzione = []
    for diff in differenza:
        if diff < 0:
            direzione.append(-1)
        elif diff > 0:
            direzione.append(1)
        else:
            direzione.append(0)

    # Distanza
    distanza = [d**2 for d in differenza]

    # Spostamento
    spostamenti = np.array(direzione) * np.array(distanza)
    spostamento = np.sum(spostamenti)

    return spostamento


def calcolo_stazionarietà(livelli: List[float]) -> float:
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

    chi = {0: 0, 1: 0, 2: 1, 3: 2, 4: 3}

    temp = []
    for key, value in ripetizioni.items():
        temp.append(chi[key] * value)
    stazionarieta = sum(temp)

    return stazionarieta


if __name__ == "__main__":
    sample_list = [1, 2, 3, 4, 5, 1, 2, 3]

    triplets_zip = get_triplets(sample_list)

    print(f"Input List: {sample_list}")
    print(f"Triplets using zip: {triplets_zip}")
