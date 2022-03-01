# %%
import pandas as pd
import os
import numpy as np

def df_edit():
    data = pd.read_csv(f'{os.getcwd()}/PL2020_2.csv')

    home_away_wins = []
    data_ha = data[['Home_Win', 'Away_Win']].set_index('Home_Win')
    for home, away in data_ha.itertuples():
        if home == '1':
            home_away_wins.append('H')
        elif away == '1':
            home_away_wins.append('A')
        else:
            home_away_wins.append('D')

    data['Winner'] = home_away_wins

    return data

# %%
