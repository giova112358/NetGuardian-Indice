import yaml
import os
from backend.config import REPERTORI_FILE, MOMENTO_DIALOGICO_FILE


def load_repertori():
    """
    Load the data in the repertori file as a dictionary

    Args:
        path: the file_path for the file with the list of rep
    Returns:
        rep dictionary
    """
    path = REPERTORI_FILE
    # Check if file exists first to avoid crashing
    if not os.path.exists(path):
        print(f"Error: The file '{path}' was not found.")
        return None

    with open(path, "r", encoding="utf-8") as file:
        try:
            # Load the YAML file content
            data = yaml.safe_load(file)
            return data.get("repertori")
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")
            return None
        
def load_momento_dialogico():
    """
    Load the data in the momento dialogico file as a dictionary

    Returns:
        momento dialogico dictionary
    """
    path = MOMENTO_DIALOGICO_FILE
    # Check if file exists first to avoid crashing
    if not os.path.exists(path):
        print(f"Error: The file '{path}' was not found.")
        return None

    with open(path, "r", encoding="utf-8") as file:
        try:
            # Load the YAML file content
            data = yaml.safe_load(file)
            return data.get("momento_dialogico")
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML: {exc}")
            return None


if __name__ == "__main__":

    print("\n--- Iterating Items ---")
    repertori = load_repertori()
    for key, value in repertori.items():
        # Handle cases where 'usage' is None (null in YAML)
        has_usage = "Yes" if value["usage"] else "No"
        # print(f"Key: {key} | Type: {value['type']} | Has Usage Data: {has_usage}")
        print(key)
