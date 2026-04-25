import pandas as pd
import os
from pathlib import Path


# create column for evolutionary stage of the pokemon



# cols to delete: pkdex num, name, hidden ability, flavor_text, sprite_url


#df = pd.read_csv(file_path)


def parse_abilities(df, n):
    # abilities are formatted as 'ability1|ability2', change this to a list 
    # then one-hot encode once you know all the unique abilities

    df['abilities']= df['abilities'].astype(str).str.split('|').apply(tuple)
    abilities = [item for sublist in df['abilities'].unique() for item in sublist]
    a = set(abilities)
    print(len(a))

        

    

def one_hot_encode(df, column):
    pd.get_dummies()

if __name__ == '__main__':
    pkmn_df = pd.read_csv('data\pokemon_complete.csv')
    n = len(pkmn_df)

    parse_abilities(pkmn_df, n)
    print(pkmn_df.head()['abilities'])