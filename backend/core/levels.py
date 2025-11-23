from backend.core.repertori import load_repertori
import os


def get_usage_sets(repertori):
    """
    Analyzes repertories and returns a dictionary containing
    a set of unique letters for each usage level.
    """
    target_levels = ["minimo", "medio", "medio_alto", "alto"]

    # Initialize a dictionary of sets
    usage_map = {level: set() for level in target_levels}

    for item in repertori.values():
        usages = item.get("usage")

        if usages:
            for level in target_levels:
                # Get the list of usages for this level
                letters = usages.get(level, [])

                # Directly update the set
                usage_map[level].update(letters)

    return usage_map


if __name__ == "__main__":
    data_path = "data"
    file_name = "repertori_map.yaml"
    file_path = os.path.join(data_path, file_name)

    # Load data
    repertori_data = load_repertori(file_path)

    # Process data
    results = get_usage_sets(repertori_data)
    print(results)

    # Print results cleanly
    for level, unique_letters in results.items():
        print(f"Level '{level}': {len(unique_letters)} unique usages")
