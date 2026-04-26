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
        """ Finds national-dex tier for a given pokemon. """
        if ('natDexTier' in mon_tiers.keys()):  # has specific natDexTier
            return mon_tiers['natDexTier']
        elif ('tier' in mon_tiers.keys()):  # does not have specified natDexTier
            return mon_tiers['tier']
        else:
            return 'Illegal'
        
    pokemon_list = raw_data.keys()
    pokemon_tiers = dict()  # will contain (name : tier)

    for mon_name in pokemon_list:
        mon_tiers = raw_data.get(mon_name)
        mon_natDexTier = getNatDexTier(mon_tiers)
        pokemon_tiers[mon_name] = mon_natDexTier

    return pokemon_tiers

def roundUpTiers(pokemon_tiers):
    """ Round up borderline tiers... ex: UUBL becomes OU """
    tier_roundups = {
        'Unreleased': 'Illegal',
        'AG': 'Illegal',
        'CAP': 'Illegal',
        'CAP LC': 'Illegal',
        'CAP NFE': 'Illegal',
        '(OU)': 'OU',
        'UUBL': 'OU',
        'RUBL': 'UU',
        'NUBL': 'RU',
        'PUBL': 'NU',
        'ZUBL': 'PU'
    }
    for mon_name in pokemon_tiers.keys():
        curr_tier = pokemon_tiers[mon_name]
        if curr_tier in tier_roundups.keys():
            pokemon_tiers[mon_name] = tier_roundups[curr_tier]
    return pokemon_tiers

def isMegaBadFormat(name:str):
    return (
        name != 'yanmega' and  # yes hardcoding this edge case is bad but it's literally the only instance of a base pokemon with a name that ends in mega, so suck it up buttercup
        len(name) > 5 and
        (name.endswith('mega') or name.endswith('megax') or name.endswith('megay'))
    )

def fixMegaNameFormat(name:str) -> str:
    if not isMegaBadFormat(name):
        return 'ERR_PROVIDE_BAD_FORMAT_MEGA'
    if name.endswith('mega'):
        return f'{name[:-4]}-mega'
    if name.endswith('megax'):
        return f'{name[:-5]}-megax'
    if name.endswith('megay'):
        return f'{name[:-5]}-megay'
    return 'ERR_PROVIDE_BAD_FORMAT_MEGA'

def formatMegas(pokemon_tiers:dict) -> dict:
    new_pokemon_tiers = dict()
    for mon in pokemon_tiers.keys():
        if isMegaBadFormat(mon):
            fixed_name = fixMegaNameFormat(mon)
            new_pokemon_tiers[fixed_name] = pokemon_tiers[mon]
        else:
            new_pokemon_tiers[mon] = pokemon_tiers[mon]
    return new_pokemon_tiers


def main() -> None:
    # Set our targeted file paths
    input_file = 'data/formats-data.json'
    output_file = 'data/exported-tiers.json'

    # Process the data
    raw_data = load_json(input_file)
    pokemon_tiers = getTiers(raw_data)
    
    # Round up borderline tiers... ex: UUBL becomes OU
    pokemon_tiers = roundUpTiers(pokemon_tiers)

    # Add the dash in the name for mega pokemon
    pokemon_tiers = formatMegas(pokemon_tiers)

    # Write the data to the output file!
    write_json(pokemon_tiers, output_file)

    # Output debug data to console
    print(f'|-- Preprocessing complete! --|')
    print(f'...Total processed pokemon -> {len(pokemon_tiers.keys())}')

    # DEBUG ... keep commented
    # countIllegal = 0
    # for mon in pokemon_tiers.keys():
    #     if pokemon_tiers[mon] == 'Illegal':
    #         countIllegal += 1
    #         print(f'{mon} -> {pokemon_tiers[mon]}')


if __name__ == "__main__":
    main()