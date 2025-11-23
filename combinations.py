import itertools
import os
from repertori import load_repertori
import random


def generate_combos(path):
    """
    Generate all the possible triplettes of repertories
    Args:
        path: the file_path for the file with the list of rep
    Returns:
        combos: all the possible combination of three rep
    """
    repertori = load_repertori(path)
    rep_list = [*repertori]

    # Generate all combinations of 3 elements
    combos = list(itertools.combinations(rep_list, 3))
    return combos


def get_rand_combo(combos):
    if not combos:
        return None
    return random.choice(combos)


if __name__ == "__main__":
    data_path = "data"
    file_name = "repertori_map.yaml"

    file_path = os.path.join(data_path, file_name)

    combos = generate_combos(file_path)

    print(f"Total combinations found: {len(combos)}")
    for combo in combos:
        print(combo)

    print(f"Number of combinations: {len(combos)} ")

    rand_comb = get_rand_combo(combos)
    print(f"Random combination: {rand_comb}")
