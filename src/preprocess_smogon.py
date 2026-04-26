# preprocessor_smogon.py
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

def getAllSmogonBuilds(smogon_files: list):
    """Returns dict containing all pokemon and their respective smogons (Gen9 natdex @ lvl 100 )."""
    def getSmogonBuilds(name: str, file_name: list):
        """Returns smogon builds (one per pokemon) for given individual file."""
        builds = load_json(file_name)
        return builds

        
    builds = []
    pokemon_learnsets = dict()  # will contain (name : tier)

    for mon_name in pokemon_list:
        mon_LS = raw_data.get(mon_name).get('learnset')
        mon_LS_normalized = normalizeLearnset(mon_LS)
        pokemon_learnsets[mon_name] = mon_LS_normalized

    return pokemon_learnsets

def main() -> None:
    # Set our targeted file paths
    """
    The order is critical!
    Potentially most optimal builds are parsed first.
    The rest are only checked and included if nothing has yet been found.
    """
    input_file_dir = 'data/smogon/'
    input_files = [
        # Batch 1 -> The National Dex Comp. Standard
        'gen9nationaldex.json',
        'gen9nationaldexuu.json',
        'gen9nationaldexru.json',
        'gen9nationaldexmonotype.json',
        # Batch 2 -> The Baby Tiers
        'gen9nfe.json',
        'gen9lc.json',
        # Batch 3 -> Random Battle Safety Nets (ending with gen7 due to "dexit")
        'gen9randombattle.json',
        'gen8randombattle.json',
        'gen7randombattle.json'
    ]
    output_file = 'data/exported-smogon.json'

    # Process the data
    smogons = getAllSmogonBuilds(input_files)

    # Write the data to the output file!
    write_json(smogons, output_file)

    # Output debug data to console
    print(f'|-- Preprocessing complete! --|')
    print(f'...Total processed pokemon -> {len(pokemon_learnsets.keys())}')


if __name__ == "__main__":
    main()