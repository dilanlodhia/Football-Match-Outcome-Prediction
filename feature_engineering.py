#%%
# Concat all data into one dataframe.
import pandas as pd
import os

# Get paths to data files
data_path = '/Users/dilanlodhia/Documents/Python/Football/Football-Dataset/'
paths_to_files = []
for root, subdirectories, filenames in os.walk(data_path):
    paths_to_files.extend([root + '/' + filename for filename in filenames if filename.endswith('.csv')])

# Check that all files have the same column names
df = pd.read_csv(paths_to_files[0])
columns = list(df.columns)
column_names_are_the_same = True
for path in paths_to_files:
    df = pd.read_csv(path)
    if columns != list(df.columns):
        column_names_are_the_same = False
# print('The column names are the same: ', column_names_are_the_same)
dfs = [pd.read_csv(path) for path in paths_to_files]
df = pd.concat(dfs)

# Checks for and removes duplicates
df = df[~df.duplicated(keep='first', subset=['Link', 'Result'])]

# Check for missing values
df.isnull().sum()   # Checks for None or NaN values

# Checks and locates incorrect results
pd.Series(df['Result']).unique()
incorrect_results = ['1 (0-0) 1', '18 MAR', '17 JAN', '0 (0-0) 0', '3 (3-2) 2', '0 (0-1) 1']
df.loc[df['Result'].isin(incorrect_results)]

# Checks if most victories occur at home or away.
incorrect_results = ['1 (0-0) 1', '18 MAR', '17 JAN', '0 (0-0) 0', '3 (3-2) 2', '0 (0-1) 1']
# df_results_1 = df.drop(index = df[~df['Result'].isin(incorrect_results)].index)
df = df[~df['Result'].isin(incorrect_results)]
results = df['Result']
counter = 0
home_team_wins = 0
away_team_wins = 0
draws = 0

for result in results:
    split_result = result.split('-')
    if counter == 150:
        break
    if split_result[0] > split_result[1]:
        home_team_wins += 1
    elif split_result[0] < split_result[1]:
        away_team_wins += 1
    else:
        draws += 1
    
    # counter += 1

data = {'Home': [home_team_wins], 'Away': [away_team_wins], 'Draw': [draws]}
df_results = pd.DataFrame(data)

##%%
# Winning streak
# def add_streak_columns(df):
#     df.sort_values(by=['Season', 'League', 'Round'], inplace=True)
#     df['Streak_Home'] = 0
#     df['Streak_Away'] = 0
#     df.reset_index(drop=True, inplace=True)
#     teams = df['Home_Team'].append(df['Away_Team']).unique()
#     for j, team_name in enumerate(teams):
#         team_matches = df[(df['Home_Team'] == team_name) | (df['Away_Team'] == team_name)]
#         idxs = team_matches.index
#         for i, idx in enumerate(idxs):
#             if i!=0:
#                 prev_match = team_matches.loc[[idxs[i-1]]]
#                 curr_match = team_matches.loc[[idxs[i]]]
#                 if prev_match['Home_Team'].values[0] == team_name and prev_match['Winner'].values[0] == 'home':
#                     if curr_match['Home_Team'].values[0] == team_name:
#                         team_matches.at[idxs[i], 'Streak_Home'] = prev_match['Streak_Home'] + 1
#                     else:
#                         team_matches.at[idxs[i], 'Streak_Away'] = prev_match['Streak_Home'] + 1
#                 if prev_match['Away_Team'].values[0] == team_name and prev_match['Winner'].values[0] == 'away':
#                     if curr_match['Home_Team'].values[0] == team_name:
#                         team_matches.at[idxs[i], 'Streak_Home'] = prev_match['Streak_Away'] + 1
#                     else:
#                         team_matches.at[idxs[i], 'Streak_Away'] = prev_match['Streak_Away'] + 1
#         df.update(team_matches)
#         return df
# df = add_streak_columns(df)


##%%
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os

# # driver = webdriver.Chrome()
# football_dataset_dir = f'{os.getcwd()}/Football-Dataset'
# dir = [element for element in os.listdir(football_dataset_dir) if element != '.DS_Store']

# for league in dir:
#     league_path = football_dataset_dir + '/' + league
#     file_dir_list = os.listdir(league_path)
#     for file in file_dir_list:
#         file_path = league_path + '/' + file
#         print(file_path)

#         # with open(file_path, 'r') as csvfile:
#         #     pass

#%%
# Create pl2020.
pl2020 = df.loc[(df['League'] == 'premier_league') & (df['Season'] == 2020)].sort_index()
pl2020
#%%
# Create premier league dataframe for 2016-2020.
pl1620 = df.loc[(df['League'] == 'premier_league') & (df['Season'].between(2016, 2020))]
pl1620.sort_values(by=['Season', 'Round'], inplace=True)
pl1620
#%%
# # %%
# # Scrape total shots and shots on target for pl2020.
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import csv

# driver = webdriver.Chrome()
# path = f'{os.getcwd()}/Football-Dataset/premier_league/Results_2020_premier_league.csv'
# home_sot_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody//tr/td/div/div[1]/div[2]/span[1]'
# away_sot_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody//tr/td/div/div[2]/div[2]/span[2]'
# home_shots_off_xpaths = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody//tr/td/div/div[1]/div[1]/span[1]'
# away_shots_off_xpaths = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody//tr/td/div/div[2]/div[1]/span[2]'
# home_sot = []
# away_sot = []
# home_shots_off = []
# away_shots_off = []

# with open(path, 'r') as csvfile:
#     urls = [row[3] for row in csv.reader(csvfile) if row[0] != 'Home_Team']

# counter = 0
# for url in urls:
#     driver.get(url)
#     home_shots_off.append(driver.find_element(By.XPATH, home_shots_off_xpaths).text)
#     away_shots_off.append(driver.find_element(By.XPATH, away_shots_off_xpaths).text)
#     home_sot.append(driver.find_element(By.XPATH, home_sot_xpath).text)
#     away_sot.append(driver.find_element(By.XPATH, away_sot_xpath).text)
#     if counter == 5:
#         break
#     counter += 1

# print(home_shots_off)
# print(away_shots_off)
# print(home_sot)
# print(away_sot)

# #%%
# # Create pl2020 dataframe and creates new columns for home and away shots on target and off target.
# pl2020 = df.loc[(df['League'] == 'premier_league') & (df['Season'] == 2020)].sort_index()
# pl2020['Home_Shots_Off_Target'] = home_shots_off
# pl2020['Away_Shots_Off_Target'] = away_shots_off
# pl2020['Home_Team_SoT'] = home_sot
# pl2020['Away_Team_SoT'] = away_sot
# pl2020
# #%%
# # Converts home and away shots off target in pl2020 to integers.
# pl2020[['Home_Shots_Off_Target', 'Away_Shots_Off_Target', 'Home_Team_SoT', 'Away_Team_SoT']] = pl2020[['Home_Shots_Off_Target', 'Away_Shots_Off_Target', 'Home_Team_SoT', 'Away_Team_SoT']].astype(int)

# # #%%
# # Create new colunns in pl2020 for home and away total shots by summing on target and off target shots.
# pl2020['Home_Shots'] = pl2020.loc[0:,['Home_Team_SoT', 'Home_Shots_Off_Target']].sum(axis=1)
# pl2020['Away_Shots'] = pl2020.loc[0:,['Away_Team_SoT', 'Away_Shots_Off_Target']].sum(axis=1)
# pl2020

# #%%
# # Removes home and away shots off target columns from pl2020
# pl2020.drop(['Home_Shots_Off_Target', 'Away_Shots_Off_Target'], axis=1, inplace=True)

# #%%
# # Creates new columns in pl2020 home and away shot accuracy by dividing on target and total shots.
# pl2020['Home_Shot_Accuracy'] = pl2020['Home_Team_SoT'] / pl2020['Home_Shots']
# pl2020['Away_Shot_Accuracy'] = pl2020['Away_Team_SoT'] / pl2020['Away_Shots']
# pl2020

# #%%
# # Removes on target and total shots from pl2020.
# pl2020.drop(['Home_Team_SoT', 'Away_Team_SoT', 'Away_Shots', 'Home_Shots'], axis=1, inplace=True)
# pl2020

# #%%
# # Converts lists of on and off target shots to integers and creates new lists of total shots for home and away.
# home_shots_off_int = [int(i) for i in home_shots_off]
# home_sot_int = [int(i) for i in home_sot]
# away_shots_off_int = [int(i) for i in away_shots_off]
# away_sot_int = [int(i) for i in away_sot]

# home_shots = [x + y for x, y in zip(home_sot_int, home_shots_off_int)]
# away_shots = [x + y for x, y in zip(away_sot_int, away_shots_off_int)]

# print(home_shots)
# print(away_shots)

# #%%
# # Creates new columns for home and away total shots in pl2020.
# pl2020['Home_Shots'] = home_shots
# pl2020['Away_Shots'] = away_shots
# pl2020
# # %%
# # Features: shots on target, shots total | tackles won, fouls drawn, yellow cards.

# # %%
# # Creates new lists home_win and away_win containing 1s and 0s depending on if the team won or lost.
# # Then creates columns in pl2020 for home win and away win. 

# # pl2020 = df.loc[(df['League'] == 'premier_league') & (df['Season'] == 2020)].sort_index()

# home_win = []
# away_win = []

# for index, home_team, away_team, result, link, season, round, league, Home_Team_ELO, Away_Team_ELO, Home_Shots, Away_Shots, Home_Shot_Accuracy, Away_Shot_Accuracy, Home_Total_Passes, Away_Total_Passes, Home_Successful_Pass_Avg, Away_Successful_Pass_Avg, Home_Win, Away_Win in pl2020.itertuples():
#     result_split = result.split('-')
#     if result_split[0] > result_split[1]:
#         home_win.append(1)
#         away_win.append(0)
#     elif result_split[0] < result_split[1]:
#         home_win.append(0)
#         away_win.append(1)
#     else:
#         home_win.append('-')
#         away_win.append('-')

# print(home_win)
# print(away_win)

# pl2020['Home_Win'] = home_win
# pl2020['Away_Win'] = away_win

# pl2020
# # %%
# # Create series of teams that won at home.
# home_wins = pl2020.loc[pl2020['Home_Win'] == 1]
# home_wins

# #%%
# # Find average shot accuracy for all home winning teams.
# home_wins_shot_acc_avg = home_wins.loc[0:, ['Home_Shot_Accuracy']].sum(axis=0) / len(home_wins)
# home_wins_shot_acc_avg

# # %%
# # Create series of teams that won away.
# away_wins = pl2020.loc[pl2020['Away_Win'] == 1]
# away_wins
# # %%
# # Find average shot accuracy for all home winning teams.
# away_win_shot_acc_avg = away_wins.loc[0:, ['Away_Shot_Accuracy']].sum(axis=0) / len(away_wins)
# away_win_shot_acc_avg

# # %%
# # Find average shot accuracy of winning teams home OR away.
# winning_team_shot_acc = home_wins_shot_acc_avg.add(away_win_shot_acc_avg, fill_value=0).sum() / 2
# winning_team_shot_acc

# # %%
# # Find average shot accuracy for losing teams at home and away.
# home_loss_shot_acc = away_wins.loc[0:, ['Home_Shot_Accuracy']].sum(axis=0) / len(away_wins)
# home_loss_shot_acc
# away_loss_shot_acc = home_wins.loc[0:, ['Away_Shot_Accuracy']].sum(axis=0) / len(home_wins)
# away_loss_shot_acc
# # %%
# # Find average shot accuracy of losing teams home OR away.
# losing_team_shot_acc = home_loss_shot_acc.add(away_loss_shot_acc, fill_value=0).sum() / 2
# losing_team_shot_acc

# # %%
# # Create dataframe of shot accuracies
# shot_acc_dict_2 = {'Home Win': [home_wins_shot_acc_avg.values[0]], 'Away Win': [away_win_shot_acc_avg.values[0]], 'Home Loss': [home_loss_shot_acc.values[0]], 'Away Loss': [away_loss_shot_acc.values[0]], 'Win Average': [winning_team_shot_acc], 'Loss Average': [losing_team_shot_acc]}
# shot_accuracy = pd.DataFrame(shot_acc_dict_2)
# shot_accuracy
# # %%
# import matplotlib.pyplot as plt

# plt.xlabel('Categories')
# plt.ylabel('Shot Accuracy')
# plt.plot(shot_accuracy)
# plt.show()

# # %%
# # Scrape ELO for PL2020 teams
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import csv
# import os

# driver = webdriver.Chrome()
# path = f'{os.getcwd()}/Football-Dataset/premier_league/Results_2020_premier_league.csv'
# home_elo_xpath = '/html/body/main/section[2]/div/div[3]/div/div/div/table/tbody/tr[2]/td[1]/span'
# away_elo_xpath = '/html/body/main/section[2]/div/div[3]/div/div/div/table/tbody/tr[2]/td[3]/span'
# home_elo_list = []
# away_elo_list = []

# with open(path, 'r') as csvfile:
#     urls = [row[3] for row in csv.reader(csvfile) if row[0] != 'Home_Team']
# counter = 0

# for url in urls:
#     analysis_url = url + '/analysis'
#     driver.get(analysis_url)
#     home_elo_list.append(driver.find_element(By.XPATH, home_elo_xpath).text)
#     away_elo_list.append(driver.find_element(By.XPATH, away_elo_xpath).text)

#     if counter == 3:
#         break
    
#     counter += 1

# print(home_elo_list)
# print(away_elo_list)


# # %%
# # Add elo ratings to pl2020 dataframe.
# pl2020['Home_Team_ELO'] = home_elo_list
# pl2020['Away_Team_ELO'] = away_elo_list
# pl2020

# #%%
# # Scrape total passes and successful passes for pl2020.
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import csv
# import os
# import re

# driver = webdriver.Chrome()
# path = f'{os.getcwd()}/Football-Dataset/premier_league/Results_2020_premier_league.csv'
# all_match_stats_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody/tr'
# home_total_passes = []
# away_total_passes = []
# home_successful_passes = []
# away_successful_passes = []

# with open(path, 'r') as csvfile:
#     urls = [row[3] for row in csv.reader(csvfile) if row[0] != 'Home_Team']

# counter = 0
# for url in urls:
#     driver.get(url)
#     info_list = driver.find_elements(By.XPATH, all_match_stats_xpath)
#     distribution_info = []
#     for info_1 in info_list:
#         split_info = re.split(' |\n', str(info_1.text))
#         for s in split_info:
#             if s == 'DISTRIBUTION':
#                 distribution_info.append([])
#             if distribution_info: distribution_info[-1].append(s)
#     counter += 1
#     if counter == 5:
#         break

#     for list_1 in distribution_info:
#         home_total_passes.append(list_1[1])
#         away_total_passes.append(list_1[4])
#         home_successful_passes.append(list_1[5])
#         away_successful_passes.append(list_1[8])

# print(home_total_passes)
# print(away_total_passes)
# print(home_successful_passes)
# print(away_successful_passes)

# # %%
# # Create new in pl2020 columns for total passes, home and away.
# pl2020['Home Total Passes'] = home_total_passes
# pl2020['Away Total Passes'] = away_total_passes

# # %%
# # Create new lists for average succesful passes.
# home_successful_pass_avg = [int(t) / int(s) for t, s in zip(home_successful_passes, home_total_passes)]
# away_successful_pass_avg = [int(v) / int(w) for v, w in zip(away_successful_passes, away_total_passes)]
# print(home_successful_pass_avg)
# print(away_successful_pass_avg)

# #%%
# # Create new columns in pl2020 for avg successful passes home and away
# pl2020['Home_Successful_Pass_Avg'] = home_successful_pass_avg
# pl2020['Away_Successful_Pass_Avg'] = away_successful_pass_avg
# pl2020

# # %%
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import csv
# import os
# import re

# driver = webdriver.Chrome()
# path = f'{os.getcwd()}/Football-Dataset/premier_league/Results_2020_premier_league.csv'
# all_match_stats_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody/tr'

# with open(path, 'r') as csvfile:
#     urls = [row[3] for row in csv.reader(csvfile) if row[0] != 'Home_Team']

# # home_offsides = []
# # away_offsides = []
# # home_aerial_balls_won = []
# # away_aerial_balls_won = []
# home_possession = []
# away_possession = []

# counter = 0
# for url in urls:
#     driver.get(url)
#     info_list = driver.find_elements(By.XPATH, all_match_stats_xpath)
#     distribution_info = []
#     for info_1 in info_list:
#         split_info = re.split(' |\n', str(info_1.text))
#         print(split_info)
#         for l in split_info:
#             if 'Possession' in l:
#                 home_possession.append(split_info[1])
#                 away_possession.append(split_info[2])
#         #     if 'Offsides' in l:
#         #         home_offsides.append(split_info[0])
#         #         away_offsides.append(split_info[2])
#         #     elif 'Aerial' in l:
#         #         home_aerial_balls_won.append(split_info[0])
#         #         away_aerial_balls_won.append(split_info[4])
#     if counter == 3:
#         break
#     counter += 1
# print(home_possession)
# print(away_possession)
# #%%
# print(len(home_possession))
# print(len(away_possession))
# #%%
# home_possession_1 = []
# away_possession_1 = []
# for hp, ap in zip(home_possession, away_possession):
#     hp_split = hp.split('%')
#     ap_split = ap.split('%')
#     hp_split = [h for h in hp_split if h != '']
#     ap_split = [a for a in ap_split if a != '']
#     for i, j in zip(hp_split, ap_split):
#         home_possession_1.append(int(i))
#         away_possession_1.append(int(j))
# home_possession_2 = [k/100 for k in home_possession_1]
# away_possession_2 = [k/100 for k in away_possession_1]


# print(home_possession_2)
# print(away_possession_2)
# print(len(home_possession_2))
# print(len(away_possession_2))

# #%%
# pl2020['Home_Possession'] = home_possession_2
# pl2020['Away_Possession'] = away_possession_2

# #%%    
# # print(home_offsides)
# # print(away_offsides)
# # print(home_aerial_balls_won)
# # print(away_aerial_balls_won)
# # print()

# # %%
# import pandas as pd
# pl2020_path = f'{os.getcwd()}/PL2020.csv'
# pl2020 = pd.read_csv(pl2020_path)
# pl2020
# # %%
# pl2020['Home_Aerial_Balls_Won'] = home_aerial_balls_won
# pl2020['Away_Aerial_Balls_Won'] = away_aerial_balls_won
# pl2020
# # %%
# # pl2020['Home_Offsides'] = home_offsides
# # pl2020['Away_Offsides'] = away_offsides
# print(len(home_offsides))
# print(len(away_offsides))



# # %%
# import itertools
# list_2 = ['4']
# list_1 = ['3']
# list_3 = ['5']
# ab = itertools.chain(list_1, list_2, list_3)
# list(ab)
# # %%
# pl2020
# # %%
# home_pos_series = pl2020.loc[pl2020['Home_Win'] == '1', 'Home_Possession']
# home_pos_series
# home_pos_avg = home_pos_series.sum(axis=0) / len(home_pos_series)
# home_pos_avg
# #%%%
# away_pos_series = pl2020.loc[pl2020['Away_Win'] == '1', 'Away_Possession']
# away_pos_series
# away_pos_avg = away_pos_series.sum(axis=0) / len(home_pos_series)
# away_pos_avg

# # %%
# home_aerial = pl2020.loc[pl2020['Home_Win'] == '1', 'Home_Aerial_Balls_Won']
# home_aerial
# home_aerial_avg = home_aerial.sum(axis=0) / len(home_aerial)
# print('Home_Win_Aerial: ', home_aerial_avg)

# #%%
# away_aerial = pl2020.loc[pl2020['Away_Win'] == '1', 'Away_Aerial_Balls_Won']
# away_aerial_avg = away_aerial.sum(axis=0) / len(away_aerial)
# print('Away_Win_Aerial: ', away_aerial_avg)
# # %%
# pl2020[['Home_Aerial_Balls_Won', 'Away_Aerial_Balls_Won']] = pl2020[['Home_Aerial_Balls_Won', 'Away_Aerial_Balls_Won']].astype(int)
# pl2020.info()
# # %%
# home_loss_aerial = pl2020.loc[pl2020['Home_Win'] == '0', 'Home_Aerial_Balls_Won']
# home_loss_aerial
# home_loss_aerial_avg = home_loss_aerial.sum(axis=0) / len(home_loss_aerial)
# print('Home_Loss_Aerial: ', home_loss_aerial_avg)
# # %%
# away_loss_aerial = pl2020.loc[pl2020['Away_Win'] == '0', 'Away_Aerial_Balls_Won']
# away_loss_aerial
# away_loss_aerial_avg = away_loss_aerial.sum(axis=0) / len(away_loss_aerial)
# print('Away_Loss_Aerial: ', away_loss_aerial_avg)
# # %%
# pl2020
# # %%
# import pandas as pd
# # Winning streak
# def winner(score):
#     scores = score.split('-')
#     if int(scores[0]) > int(scores[1]):
#         return 'home'
#     elif int(scores[0]) < int(scores[1]):
#         return 'away'
#     else:
#         return 'draw'

# df['Winner'] = df.apply(lambda row: winner(row.Result), axis=1)

# def add_streak_columns(df):
#     df.sort_values(by=['Season', 'League', 'Round'], inplace=True)
#     df['Streak_Home'] = 0
#     df['Streak_Away'] = 0
#     df.reset_index(drop=True, inplace=True)
#     teams = df['Home_Team'].append(df['Away_Team']).unique()
#     teams
#     for j, team_name in enumerate(teams):
#         team_matches = df[(df['Home_Team'] == team_name) | (df['Away_Team'] == team_name)]
#         idxs = team_matches.index
#         for i, idx in enumerate(idxs):
#             if i!=0:
#                 prev_match = team_matches.loc[[idxs[i-1]]]
#                 curr_match = team_matches.loc[[idxs[i]]]
#                 if prev_match['Home_Team'].values[0] == team_name and prev_match['Winner'].values[0] == 'home':
#                     if curr_match['Home_Team'].values[0] == team_name:
#                         team_matches.at[idxs[i], 'Streak_Home'] = prev_match['Streak_Home'] + 1
#                     else:
#                         team_matches.at[idxs[i], 'Streak_Away'] = prev_match['Streak_Home'] + 1
#                 if prev_match['Away_Team'].values[0] == team_name and prev_match['Winner'].values[0] == 'away':
#                     if curr_match['Home_Team'].values[0] == team_name:
#                         team_matches.at[idxs[i], 'Streak_Home'] = prev_match['Streak_Away'] + 1
#                     else:
#                         team_matches.at[idxs[i], 'Streak_Away'] = prev_match['Streak_Away'] + 1
#         df.update(team_matches)
#     return df
# df = add_streak_columns(df)
# df
# # %%
# import pandas as pd
# # Winning streak
# # def add_streak_columns(df):
# pl2020.sort_values(by=['Season', 'League', 'Round'], inplace=True)
# pl2020['Streak_Home'] = 0   # create column of zeros called 'Streak_Home'
# pl2020['Streak_Away'] = 0   # create column of zeros called 'Streak_Away'
# pl2020.reset_index(drop=True, inplace=True)
# teams = pl2020['Home_Team'].append(pl2020['Away_Team']).unique()    # combine 'Home_team' and 'away_team' into one series and return each value once (unique)
# teams

# #%%
# for j, team_name in enumerate(teams):
#     team_matches = pl2020[(pl2020['Home_Team'] == team_name) | (pl2020['Away_Team'] == team_name)]
#     print(team_matches)

# # %%
# list1 = [2, 3, 4, 5, 6, 7, 8]
# list2 = [5, 6, 2, 7, 8, 5, 2]
# list3 = [5, 6, 8, 5, 6, 8, 9]
# list4 = [6, 5, 3, 5, 7, 8, 9]
# list5 = [8, 4, 3, 6, 7, 5, 3]

# test_df = pd.DataFrame(zip(list1, list2))
# test_df['column3'] = list3

# # %%
# test_df = test_df.rename(columns={0: 'column_1'})
# test_df = test_df.rename(columns={1: 'column_2'})
# # %%
# test_df = test_df.rename(columns={'column3': 'column_3'})
# # %%
# list4 = [6, 5, 3, 5, 7, 8, 9]
# list5 = [8, 4, 3, 6, 7, 5, 3]

# test_df['column_4'] = list4
# test_df['column_5'] = list5
# test_df
# # %%
# test_df.sort_values(by=['column_1', 'column_2'], inplace=True)
# test_df
# # %%
# test_df['Streak_Home'] = 0
# test_df['Streak_Away'] = 0

# # %%
# test_df.reset_index(drop=True, inplace=True)
# # %%
# teams_1 = test_df['column_1'].append(test_df['column_2']).unique()
# # %%
# df
# # %%

# # %%
# # Scrape possession
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import csv
# import os
# import re

# driver = webdriver.Chrome()
# path = f'{os.getcwd()}/Football-Dataset/premier_league/Results_2020_premier_league.csv'
# all_match_stats_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody/tr'

# with open(path, 'r') as csvfile:
#     urls = [row[3] for row in csv.reader(csvfile) if row[0] != 'Home_Team']

# home_possession = []
# away_possession = []

# counter = 0
# for url in urls:
#     driver.get(url)
#     info_list = driver.find_elements(By.XPATH, all_match_stats_xpath)
#     distribution_info = []
#     home_possession.append('0')
#     away_possession.append('0')
#     for info_1 in info_list:
#         split_info = re.split(' |\n', str(info_1.text))
#         possession_found = False
#         #home_poss.... .append(0)
#         for l in split_info:
#             if 'Possessionn' in l:
#                 home_possession[-1] = split_info[1]
#                 away_possession[-1] = split_info[2]
#                 # possession_found = True
#                 # home_possession.append(split_info[1])
#                 # away_possession.append(split_info[2])
#         # if not possession_found:    
#         #     home_possession.append(0)
#         #     away_possession.append(0)
#         print(split_info)
#     if counter == 2:
#         break
#     counter += 1

# print('Home_possession: ', home_possession)
# print('Away Possession: ', away_possession)
# print(len(home_possession))
# print(len(away_possession))

# home_possession_1 = []
# away_possession_1 = []
# # for hp, ap in zip(home_possession, away_possession):
# #     hp_split = hp.split('%')
# #     ap_split = ap.split('%')
# #     hp_split = [h for h in hp_split if h != '']
# #     ap_split = [a for a in ap_split if a != '']
# hp_split = [h for hp in home_possession for h in hp.split('%') if h != '']  # could potentially use list comprehensions
# ap_split = [a for ap in away_possession for a in ap.split('%') if a != '']

# for i, j in zip(hp_split, ap_split):
#     home_possession_1.append(int(i)/100)
#     away_possession_1.append(int(j)/100)
# # # # home_possession_2 = [k/100 for k in home_possession_1]
# # # # away_possession_2 = [k/100 for k in away_possession_1]

# print('home_possession: ', home_possession_1)
# print('away_possession: ', away_possession_1)
# print(len(home_possession_1))
# print(len(away_possession_1))

# #%%
# pl2020['Home_Possession'] = home_possession_2
# pl2020['Away_Possession'] = away_possession_2

# # %%
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import os
# import csv

# # driver = webdriver.Chrome()
# football_dataset_dir = f'{os.getcwd()}/Football-Dataset'
# dir = [element for element in os.listdir(football_dataset_dir) if element == 'premier_league']
# pl_list = []
# for league in dir:
#     league_path = football_dataset_dir + '/' + league
#     for file in sorted(os.listdir(league_path)):
#         file_path = league_path + '/' + file
#         if 2016 <= int(file_path.split('_')[2]) <= 2020:
#             pl_list.append(file_path)

# urls = []
# for path in pl_list:
#     with open(path, 'r') as csvfile:
#         for row in csv.reader(csvfile):
#             if row[0] != 'Home_Team':
#                 urls.append(row[3])

# print(len(urls))

# %%
# %%
# Scrape possession for pl1620.
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import re

driver = webdriver.Chrome()
path = f'{os.getcwd()}/Football-Dataset/premier_league/Results_2020_premier_league.csv'

# football_dataset_dir = f'{os.getcwd()}/Football-Dataset'
# dir = [element for element in os.listdir(football_dataset_dir) if element == 'premier_league']
# pl_list = []
# for league in dir:
#     league_path = football_dataset_dir + '/' + league
#     for file in sorted(os.listdir(league_path)):
#         file_path = league_path + '/' + file
#         if 2016 <= int(file_path.split('_')[2]) <= 2020:
#             pl_list.append(file_path)

# urls = []
# for path in pl_list:
#     with open(path, 'r') as csvfile:
#         for row in csv.reader(csvfile):
#             if row[0] != 'Home_Team':
#                 urls.append(row[3])

with open(path, 'r') as csvfile:
    urls = [row[3] for row in csv.reader(csvfile) if row[0] != 'Home_Team']

all_match_stats_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody/tr'

distribution_info = []
home_possession = []
away_possession = []
home_total_passes = []
away_total_passes = []
home_successful_passes = []
away_successful_passes = []
home_possession_1 = []
away_possession_1 = []
distribution_info = []
match_info = []
counter = 0
for url in urls:
    driver.get(url)
    info_list = driver.find_elements(By.XPATH, all_match_stats_xpath)
    home_possession.append('0')
    away_possession.append('0')
    for info_1 in info_list:
        split_info = re.split(' |\n', str(info_1.text))
        print('Split_info: ', split_info)
        for s in split_info:
            match_info.append(s)
            if 'DISTRIBUTION' not in match_info:
                pass
            if s == 'DISTRIBUTION':
                distribution_info.append([])
            if distribution_info: distribution_info[-1].append(s)
            if 'Possession' in s:
                home_possession[-1] = split_info[1]
                away_possession[-1] = split_info[2]

    if counter == 1:
        break
    counter += 1

hp_split = [h for hp in home_possession if hp != 0 for h in hp.split('%') if h != '']
ap_split = [a for ap in away_possession if ap != 0 for a in ap.split('%') if a != '']
for i, j in zip(hp_split, ap_split):
    home_possession_1.append(int(i)/100)
    away_possession_1.append(int(j)/100)

for list_1 in distribution_info:
    home_total_passes.append(list_1[1])
    away_total_passes.append(list_1[4])
    home_successful_passes.append(list_1[5])
    away_successful_passes.append(list_1[8])

print('distribution_info: ', distribution_info)
print('Home_possession: ', home_possession)
print('Away Possession: ', away_possession)
print(len(home_possession))
print(len(away_possession))
print('home_possession: ', home_possession_1)
print('away_possession: ', away_possession_1)
print(len(home_possession_1))
print(len(away_possession_1))
print('Distribution info: ', distribution_info)
print('home total passes: ', home_total_passes)
print('away total passes: ', away_total_passes)
print('home succ passes: ', home_successful_passes)
print('away succ passes: ', away_successful_passes)
# %%

# %%
