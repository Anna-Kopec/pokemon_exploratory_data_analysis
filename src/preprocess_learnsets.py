# preprocessor_learnsets.py
# B. Deutsch (4/26/26)

# Library imports
import json

# Helper functions
def load_json(file_path: str):
    """Loads and returns the JSON data from the specified file path."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}.")
        return None

def write_json(data: dict, file_path: str):
    """Dumps the dict as JSON data into the specified file path."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}.")
        return None

def getLearnsets(raw_data):
    """Returns dict containing all pokemon and their respective learnsets (Gen9 natdex @ lvl 100 ). """
    def normalizeLearnset(learnset):
        """ Returns learnset without data pertaining to level or acq. method. """
        try:
            return list(learnset.keys())
        except:
            return ['NO_VALID_LEARNSET']
        
    pokemon_list = raw_data.keys()
    pokemon_learnsets = dict()  # will contain (name : tier)

    for mon_name in pokemon_list:
        mon_LS = raw_data.get(mon_name).get('learnset')
        mon_LS_normalized = normalizeLearnset(mon_LS)
        pokemon_learnsets[mon_name] = mon_LS_normalized

    return pokemon_learnsets

def main() -> None:
    # Set our targeted file paths
    input_file = 'data/learnsets.json'
    output_file = 'data/exported-learnsets.json'

    # Process the data
    raw_data = load_json(input_file)
    pokemon_learnsets = getLearnsets(raw_data)

    # Write the data to the output file!
    write_json(pokemon_learnsets, output_file)


if __name__ == "__main__":
    main()