# preprocessor_tiers.py
# B. Deutsch (4/25/26)

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

def getTiers(raw_data):
    """Returns dict containing all pokemon and their respective nat-dex tiers. """
    def getNatDexTier(mon_tiers):
        """ Finds netional-dex tier for a given pokemon. """
        if ('natDexTier' in mon_tiers.keys()):  # has specific natDexTier
            return mon_tiers['natDexTier']
        elif ('tier' in mon_tiers.keys()):  # does not have specified natDexTier
            return mon_tiers['tier']
        else:
            return 'NO_TIER_DEFINED'
        
    pokemon_list = raw_data.keys()
    pokemon_tiers = dict()  # will contain (name : tier)

    for mon_name in pokemon_list:
        mon_tiers = raw_data.get(mon_name)
        mon_natDexTier = getNatDexTier(mon_tiers)
        pokemon_tiers[mon_name] = mon_natDexTier

    return pokemon_tiers

def main() -> None:
    # Set our targeted file paths
    input_file = 'data/formats-data.json'
    output_file = 'data/exported-tiers.json'

    # Process the data
    raw_data = load_json(input_file)
    pokemon_tiers = getTiers(raw_data)
    
    # Write the data to the output file!
    write_json(pokemon_tiers, output_file)


if __name__ == "__main__":
    main()