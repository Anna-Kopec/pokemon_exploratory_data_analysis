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

def isMega(mon_name):
    try:
        mon_name.index('-mega')
        return True
    except:
        return False

def getNonMegaName(mon_name):
    # trivial short-circuit
    if not isMega(mon_name):
        return 'ERROR_INPUT_MUST_BE_MEGA'
    mega_tag_index = mon_name.index('-mega')
    non_mega_name = mon_name[0:mega_tag_index]
    return non_mega_name

def hasNonMega(mega_name:str, pokemon_learnsets:dict) -> bool:
        return getNonMegaName(mega_name) in pokemon_learnsets.keys()

def addMegaLearnsets(pokemon_learnsets: dict):
    # We'll pull from the exported tiers from the other preprocessor to find our list of megas
    tiers = load_json('data/exported-tiers.json')
    for mon in tiers:
        if isMega(mon) and hasNonMega(mon, pokemon_learnsets):
            pokemon_learnsets[mon] = pokemon_learnsets[getNonMegaName(mon)]

def removeInvalidLearnsets(pokemon_learnsets:dict):
    hitlist = []  # track which to remove
    for mon in pokemon_learnsets.keys():
        if 'NO_VALID_LEARNSET' in pokemon_learnsets[mon]:
            hitlist.append(mon)
    for mon in hitlist:
        pokemon_learnsets.pop(mon)
    

def main() -> None:
    # Set our targeted file paths
    input_file = 'data/learnsets.json'
    output_file = 'data/exported-learnsets.json'

    # Process the data
    raw_data = load_json(input_file)
    pokemon_learnsets = getLearnsets(raw_data)

    # At this point we're still missing the megas, so lets add those in here
    addMegaLearnsets(pokemon_learnsets)

    # Lastly, we remove the entries without valid learnsets
    removeInvalidLearnsets(pokemon_learnsets)

    # Write the data to the output file!
    write_json(pokemon_learnsets, output_file)

    # Output debug data to console
    print(f'|-- Preprocessing complete! --|')
    print(f'...Total processed pokemon -> {len(pokemon_learnsets.keys())}')


if __name__ == "__main__":
    main()