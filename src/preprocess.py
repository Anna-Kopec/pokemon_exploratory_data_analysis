import pandas as pd
import os
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import numpy as np
import json

def label_encode_ordinal(df, column, ordered_list):
    """
    Standardizes ordinal encoding for a specific order and ensures lowercase title.
    """
    mapping = {val: i for i, val in enumerate(ordered_list)}
    df[column] = df[column].map(mapping).fillna(0).astype(int)
    df.columns = df.columns.str.lower()
    return df

def multi_hot_encode(df, column, prefix):
    """
    Replaces a column of piped strings with individual binary columns.
    Ensures all new column titles are lowercase.
    """
    item_lists = df[column].astype(str).str.split('|').apply(
        lambda x: [item.strip().lower() for item in x if item.strip().lower() not in ['none', 'nan', '']]
    )

    mlb = MultiLabelBinarizer()
    binary_matrix = mlb.fit_transform(item_lists)
    
    # Generate names and immediately lowercase them
    col_names = [f'{prefix}_{c}'.lower() for c in mlb.classes_]
    binary_df = pd.DataFrame(binary_matrix, columns=col_names, dtype=int)
    
    df = pd.concat([df.drop(columns=[column]).reset_index(drop=True), binary_df], axis=1)
    return df

def one_hot_encode(df, columns):
    """
    one-hot encode cat data w/out order.
    Forces all generated column names to lowercase.
    """
    df = pd.get_dummies(df, columns=columns, prefix=columns, dtype=int)
    df.columns = df.columns.str.lower()
    return df


if __name__ == '__main__':
    data_path = Path('data/pokemon_complete.csv')
    if not data_path.exists():
        raise FileNotFoundError(f"Could not find {data_path}")
        
    pkmn_df = pd.read_csv(data_path)
    # Standardize initial column names to lowercase
    pkmn_df.columns = pkmn_df.columns.str.lower()

    # --- 1. MULTI-HOT ENCODE --- 
    # abilities
    pkmn_df = multi_hot_encode(pkmn_df, 'abilities', 'ability')

    # movepools
    movepool_path = 'data/learnsets.json'
    with open(movepool_path, 'r') as f:
        movepool_mapping = json.load(f)
    




    # UNIFY TYPES: Join type1 and type2 then multi-hot encode
    pkmn_df['temp_types'] = pkmn_df['type_1'].astype(str) + '|' + pkmn_df['type_2'].astype(str)
    pkmn_df = multi_hot_encode(pkmn_df, 'temp_types', 'type')
    pkmn_df = pkmn_df.drop(columns=['type_1', 'type_2'])

    # --- 2. ONE-HOT ENCODE ---
    pkmn_df = one_hot_encode(pkmn_df, ['habitat', 'shape', 'color'])

    # --- 3. ORDINAL LABEL ENCODING ---
    gens = ['gen-i','gen-ii','gen-iii','gen-iv','gen-v','gen-vi', 'gen-vii', 'gen-viii', 'gen-ix']
    pkmn_df = label_encode_ordinal(pkmn_df, 'generation', gens)

    growth_order = ['fast', 'medium', 'fast-then-very-slow', 'medium-slow', 'slow', 'slow-then-very-fast']
    pkmn_df = label_encode_ordinal(pkmn_df, 'growth_rate', growth_order)

    # Competitive Tiers
    tier_path = Path('data/exported-tiers.json')
    if tier_path.exists():
        with open(tier_path, 'r') as f:
            tier_mapping = json.load(f)

        pkmn_df['name_clean'] = pkmn_df['name'].str.replace('-', '', regex=False).str.lower()
        pkmn_df['tier'] = pkmn_df['name_clean'].map(tier_mapping)
        
        tier_order = ['LC', 'NFE', 'RU', 'UU', 'OU', 'Uber', 'AG']
        
        pkmn_df = pkmn_df[pkmn_df['tier'].isin(tier_order)].copy()
        pkmn_df = label_encode_ordinal(pkmn_df, 'tier', tier_order)

    # --- 4. BOOLS->INT + CALCULATED EVO STAGES --
    pkmn_df['evolution_stage'] = pkmn_df.groupby('evolution_chain_id').cumcount() + 1
    pkmn_df.loc[pkmn_df['is_baby'] == 1, 'evolution_stage'] = 0

    bool_cols = ['is_legendary', 'is_mythical', 'is_baby']
    for col in bool_cols:
        if col in pkmn_df.columns:
            pkmn_df[col] = pkmn_df[col].astype(int)

    # --- 5. CLEANUP & EXPORT --- 
    cols_to_delete = ['pokedex_number', 'name', 'name_clean', 'hidden_ability', 
                      'flavor_text', 'sprite_url', 'genus', 'evolution_chain_id', 'egg_groups']
    
    pkmn_df = pkmn_df.drop(columns=[c for c in cols_to_delete if c in pkmn_df.columns])
    
    # Final global lowercase check before saving
    pkmn_df.columns = pkmn_df.columns.str.lower()
    
    output_path = Path('data/preprocessed_pokemon_data.csv')
    pkmn_df.to_csv(output_path, index=False)
    print(f"Successfully saved to {output_path}; {len(pkmn_df.columns)} cols")