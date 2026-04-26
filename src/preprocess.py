import pandas as pd
import os
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
import numpy as np

#TODO

# 1. reformat names such that all names are lowercase without any '-' connecting them, so that they can be compared directly w names from smogon dataset

# OPTIONAL stuff 
# 1. create column for evolutionary stage of the pokemon - use the fact that evolutionary chain is ordered by pokedex entry
# only exception is baby pokemon, so check for is_baby flag 


def multi_group_encode(df, column, n):
    '''
    df -> dataframe
    column -> column that will be split into n encoded cols
    n -> int, max # of possibilities for a given property a pokemon can have (e.g. 3 possible abilities max)
    
    abilities and egg groups (for example) are formatted as "ability1|ability2", 
    change this such that there are n columns, one for each possibility, 
    where each col contains an int encoding of the pokemon's property for each entry,
    an entry of 0 represents None'''


    # convert one long string of possibilities into tuple of strings
    df[column]= df[column].astype(str).str.split('|').apply(tuple)
    unique_values = set([item for sublist in df[column].unique() for item in sublist])

    # create dict to store n entries for the given property for each pokemon
    columns = {f'{column}_{i}':[] for i in range(1,n+1)}
    col_names = list(columns.keys())

    # encoder
    le = LabelEncoder()
    le.fit(list(unique_values))

    for index, row in df.iterrows():
        # list of possibile properties that the current pokemon can have
        possibilities = sorted(row[column])
        encoded_possibilities = le.transform(possibilities)
        m = len(possibilities)

        # add 1 to all encoded values to account for the fact that we want 0 to = None, but in our encoder, 0 = first possible ability

        for i in range(n):
            if i == 0:
                columns[col_names[0]].append(encoded_possibilities[0] + 1)
            else: 
                if m > i:
                    columns[col_names[i]].append(encoded_possibilities[i] + 1)
                else:
                    columns[col_names[i]].append(0)

    df = df.drop(columns=[column])
    for name in col_names:
        df[name] = columns[name]

    return df
 

def label_encode(df, column, values):
    '''
    df-> input df
    column -> str, col we are encoding
    values -> set of unique values from col we are encoding, should not have duplicates
    treat 'None' as a possible value, alter encoding such that actual values start with 1 rather than 0 (None=0) for interpretability
    '''
    # Remove any actual NaNs from our values list
    values = [x for x in values if pd.notna(x) and x != 'None']
    
    # sort elements alphabetically
    values.sort()

    le = LabelEncoder()

    # Force 'None' to index 0
    final_values = ['None'] + values

    # We manually set the classes so LE doesn't re-sort them alphabetically
    le.classes_ = np.array(final_values)
    
    # Update the actual column to replace NaNs with the string 'None'
    df[column] = df[column].fillna('None')

    # Transform the column and overwrite it
    df[column] = le.transform(df[column])

    # print({label: i for i, label in enumerate(le.classes_)})

    return df


if __name__ == '__main__':
    pkmn_df = pd.read_csv('data\pokemon_complete.csv')
    n = len(pkmn_df)

    # encode abilities
    pkmn_df = multi_group_encode(pkmn_df, 'abilities', 3)

    # encode egg_groups
    pkmn_df = multi_group_encode(pkmn_df, 'egg_groups', 2)

    # encode habitat
    habitats = pkmn_df['habitat'].unique()
    pkmn_df = label_encode(pkmn_df, 'habitat', habitats)

    # encode shape
    shapes = pkmn_df['shape'].unique()
    pkmn_df = label_encode(pkmn_df, 'shape', shapes)

    # encode color
    colors = pkmn_df['color'].unique()
    pkmn_df = label_encode(pkmn_df, 'color', colors)

    # encode generation
    gens = pkmn_df['generation'].unique()
    pkmn_df = label_encode(pkmn_df, 'generation', gens)

    # encode types
    types = pd.unique(pkmn_df[['type_1', 'type_2']].values.ravel())
    pkmn_df = label_encode(pkmn_df, 'type_1', types)
    pkmn_df = label_encode(pkmn_df, 'type_2', types)

    bool_cols = ['is_legendary', 'is_mythical', 'is_baby']
    pkmn_df[bool_cols] = pkmn_df[bool_cols].astype(int)

    cols_to_delete = ['pokedex_number', 'name', 'hidden_ability', 'flavor_text', 'sprite_url', 'genus']
    pkmn_df = pkmn_df.drop(columns=cols_to_delete)

    # encode growth rate (special because it's ordinal)
    growth_order = {'fast':1, 'medium':2, 'fast-then-very-slow':3, 'medium-slow':4, 'slow':5, 'slow-then-very-fast':6}
    pkmn_df['growth_rate'] = pkmn_df['growth_rate'].map(growth_order)

    # Save to data folder
    pkmn_df.to_csv('data/preprocessed_pokemon_data.csv', index=False)


    


