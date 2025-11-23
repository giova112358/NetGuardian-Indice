from repertori import load_repertori
import pandas as pd


def generate_interactions_table(triplete, data):

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
        interaction_full = " - ".join(interaction_parts)

        # Add the interaction column to the row data
        row_data.append(interaction_full)
        table_rows.append(row_data)

    # Create DataFrame
    columns = selected_keys + ["Interazione fra Repertori"]
    # Capitalize index names for display (Minimo, Medio, etc.)
    index_labels = [l.capitalize().replace("_", "-") for l in levels]

    df = pd.read_json
    df = pd.DataFrame(table_rows, columns=columns, index=index_labels)

    return df


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
    print("-" * 30)
    print(df_result)

    # Optional: Export to HTML to see it formatted like the image in a browser/notebook
    print(df_result.to_html())
