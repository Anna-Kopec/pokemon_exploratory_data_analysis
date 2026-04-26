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

def getFirstKey(d: dict):
    """Returns first key of given dict. Will be messy, don't read into it too deep. :|"""
    return list((d.keys()))[0]

def getFirstValue(d: dict):
    """Returns first value of given dict. Will be messy, don't read into it too deep. :|"""
    return d[list((d.keys()))[0]]

def normalizeRandomBattles(file_names: list):
    for fname in file_names:
        pokemon_builds = load_json(fname)
        # First check if this file was already normalized
        first_mon_name = getFirstKey(pokemon_builds)
        first_mon = pokemon_builds[first_mon_name]
        if 'level' not in first_mon:
            continue  # skip this file; don't change it
        # From here, we know the file must be wrong
        new_pokemon_builds = dict()
        for name in pokemon_builds.keys():
            new_pokemon_builds[name] = {'DefaultBuild' : pokemon_builds[name]}
        write_json(new_pokemon_builds, fname)

def getAllSmogonBuilds(smogon_files: list):
    """Returns dict containing all pokemon and their respective smogons (Gen9 natdex @ lvl 100 )."""
    def getSmogonBuilds(file_name: list):
        """Returns smogon builds (one per pokemon) for given individual file."""
        builds = dict()
        mons = load_json(file_name)
        # Now we need to scrap all the named builds and just return one per pokemon
        for mon in mons.keys():
            # Get first build; if there's only one, grabs only build
            curr_options = mons[mon]
            selected_option = getFirstValue(curr_options)
            # Add this build into builds under the current pokemon name
            builds[mon] = selected_option
        return builds

    builds = dict()
    # Parse each smogon file
    for fname in smogon_files:
        # Pull smogons from the file
        new_builds = getSmogonBuilds(fname)
        # Add all pokemon from this smogon file that we haven't already seen
        for mon_name in new_builds.keys():
            if mon_name not in builds.keys():
                builds[mon_name] = new_builds[mon_name]
    return builds

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

    # Prepend directory for all input data file names
    for i in range(len(input_files)):
        input_files[i] = input_file_dir + input_files[i]

    # Pre-pre-process the random battle files by nesting their builds the way the rest are formatted.
    normalizeRandomBattles(input_files[-3:])

    # Process the data
    smogon_builds = getAllSmogonBuilds(input_files)

    # Normalize casing for all pokemon names
    smogon_builds = {k.lower(): v for k, v in smogon_builds.items()}
    
    # Write the data to the output file!
    write_json(smogon_builds, output_file)

    # Output debug data to console
    print(f'|-- Preprocessing complete! --|')
    print(f'...Total processed pokemon -> {len(smogon_builds.keys())}')


if __name__ == "__main__":
    main()