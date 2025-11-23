import pandas as pd
from backend.core.repertori import load_repertori
from backend.core.levels import get_usage_sets


def generate_interactions_table(triplete, data):
    """
    Generates a table representing the interactions of the usages

    Args:
        triplete: a triplete of repertoires
        data: the dictionary with all the usages
    Returns:
        df: a dataframe with the interactions
    """

    selected_keys = list(triplete)

    # Define the rows we want (usage levels)
    levels = ["minimo", "medio", "medio_alto", "alto"]
    table_rows = []

    for level in levels:
        row_data = []
        interaction_parts = []

        for key in selected_keys:
            # Get the usage list for this level (e.g., ['a', 'b'])
            usage_list = data[key]["usage"].get(level)

            # Convert list to string (e.g., "ab") or empty string if list is empty/None
            if usage_list:
                cell_str = "".join(usage_list)
            else:
                cell_str = ""

            row_data.append(cell_str)

            # Add to interaction parts only if it's not empty
            if cell_str:
                interaction_parts.append(cell_str)

        # Create the "Interazione" string
        interaction_full = "".join(interaction_parts)

        # Add the interaction column to the row data
        row_data.append(interaction_full)
        table_rows.append(row_data)

    # Create DataFrame
    columns = selected_keys + ["Interazione"]
    # Capitalize index names for display
    index_labels = [l.capitalize().replace("_", "-") for l in levels]

    df = pd.read_json
    df = pd.DataFrame(table_rows, columns=columns, index=index_labels)

    percs = perc_usages_interact(df["Interazione"], data)
    df["Copertura"] = percs

    return df


def perc_usages_interact(interaction, data):
    """
    Calculates and prints the percentage of interactions per level.
    Optimized to use .iloc to avoid FutureWarnings and reduce redundant calculations.
    """
    usage_dict = get_usage_sets(data)

    # Map keys to the positional index in the 'interaction' series
    keys_order = ["minimo", "medio", "medio_alto", "alto"]

    unique_counts = [len(set(interaction.iloc[i])) for i in range(4)]

    # Calculate percentages
    percs = []
    for i, key in enumerate(keys_order):
        total = len(usage_dict[key])
        unique = unique_counts[i]
        value = unique / total if total > 0 else 0
        percs.append(round(value, 2))

    return percs


if __name__ == "__main__":
    import os

    data_path = "data"
    file_name = "repertori_map.yaml"
    file_path = os.path.join(data_path, file_name)

    triplete = ("PZ", "CF", "VA")
    data = load_repertori(file_path)
    # Run the function
    df_result = generate_interactions_table(triplete, data)

    # Display
    print("Selected Repertori:", list(df_result.columns[:3]))
    print("-" * 60)
    print(df_result)

    # Export to HTML
    # print(df_result.to_html())

    # Analyze levels
    print("Levels analysis")
    print("-" * 60)
    interazioni = df_result["Interazione"]
    print(interazioni)
    perc_usages_interact(interazioni, data)
