#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import re
import pandas as pd
from feature_engineering import pl2020
import time

start = time.perf_counter()

class Scraper_PL2020:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.path = f'{os.getcwd()}/Football-Dataset/premier_league/Results_2020_premier_league.csv'
        self._xpaths()
        # self._home_away_win()

        with open(self.path, 'r') as csvfile:
            self.urls = [row[3] for row in csv.reader(csvfile) if row[0] != 'Home_Team']
    
        self.home_elo_list = []
        self.away_elo_list = []
        self.home_sot = []
        self.away_sot = []
        self.home_shots_off = []
        self.away_shots_off = []
        self.home_total_passes = []
        self.away_total_passes = []
        self.home_successful_passes = []
        self.away_successful_passes = []
        self.home_possession = []
        self.away_possession = []

    def _xpaths(self):
        self.home_elo_xpath = '/html/body/main/section[2]/div/div[3]/div/div/div/table/tbody/tr[2]/td[1]/span'
        self.away_elo_xpath = '/html/body/main/section[2]/div/div[3]/div/div/div/table/tbody/tr[2]/td[3]/span'
        self.home_sot_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody//tr/td/div/div[1]/div[2]/span[1]'
        self.away_sot_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody//tr/td/div/div[2]/div[2]/span[2]'
        self.home_shots_off_xpaths = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody//tr/td/div/div[1]/div[1]/span[1]'
        self.away_shots_off_xpaths = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody//tr/td/div/div[2]/div[1]/span[2]'
        self.all_match_stats_xpath = '/html/body/main/section[2]/div/div[4]/div/div[2]/table/tbody/tr'

    def _scrape_elo(self, url):
        analysis_url = url + '/analysis'
        self.driver.get(analysis_url)
        self.home_elo_list.append(self.driver.find_element(By.XPATH, self.home_elo_xpath).text)
        self.away_elo_list.append(self.driver.find_element(By.XPATH, self.away_elo_xpath).text)

        print('home elo list: ', self.home_elo_list)
        print('away elo list; ', self.away_elo_list)
        return self.home_elo_list, self.away_elo_list

    def _scrape_shots(self, url):
        self.driver.get(url)
        self.home_shots_off.append(self.driver.find_element(By.XPATH, self.home_shots_off_xpaths).text)
        self.away_shots_off.append(self.driver.find_element(By.XPATH, self.away_shots_off_xpaths).text)
        self.home_sot.append(self.driver.find_element(By.XPATH, self.home_sot_xpath).text)
        self.away_sot.append(self.driver.find_element(By.XPATH, self.away_sot_xpath).text)

        print('Home shots off: ', self.home_shots_off)
        print('away shots off: ', self.away_shots_off)
        print('home sot: ', self.home_sot)
        print('away sot: ', self.away_sot)
        return self.home_sot, self.away_sot, self.home_shots_off, self.away_shots_off

    def _scrape_possession_passes(self, url):
        self.driver.get(url)
        self.distribution_info = []
        self.home_possession_1 = []
        self.away_possession_1 = []
        info_list = self.driver.find_elements(By.XPATH, self.all_match_stats_xpath)
        self.home_possession.append('0')
        self.away_possession.append('0')
        for info_1 in info_list:
            self.split_info = re.split(' |\n', str(info_1.text))
            for s in self.split_info:
                if s == 'DISTRIBUTION':
                    self.distribution_info.append([])
                if self.distribution_info: self.distribution_info[-1].append(s)
                if 'Possession' in s:
                    self.home_possession[-1] = self.split_info[1]
                    self.away_possession[-1] = self.split_info[2]
        hp_split = [h for hp in self.home_possession if hp != 0 for h in hp.split('%') if h != '']
        ap_split = [a for ap in self.away_possession if ap != 0 for a in ap.split('%') if a != '']
        for i, j in zip(hp_split, ap_split):
            self.home_possession_1.append(int(i)/100)
            self.away_possession_1.append(int(j)/100)

        for list_1 in self.distribution_info:
            self.home_total_passes.append(list_1[1])
            self.away_total_passes.append(list_1[4])
            self.home_successful_passes.append(list_1[5])
            self.away_successful_passes.append(list_1[8])
        
        print('Home_Possession_1: ', self.home_possession_1)
        print('Away_Possession_1: ', self.away_possession_1)
        print('Distribution info: ', self.distribution_info)
        print('home total passes: ', self.home_total_passes)
        print('away total passes: ', self.away_total_passes)
        print('home succ passes: ', self.home_successful_passes)
        print('away succ passes: ', self.away_successful_passes)
        return self.home_total_passes, self.away_total_passes, self.home_successful_passes, self.away_successful_passes

    def _home_away_win(self):
        self.home_win = []
        self.away_win = []
        pl2020_result = pl2020[['Result', 'Round']].set_index('Result')
        for result, round in pl2020_result.itertuples():
            result_split = result.split('-')
            if result_split[0] > result_split[1]:
                self.home_win.append(1)
                self.away_win.append(0)
            elif result_split[0] < result_split[1]:
                self.home_win.append(0)
                self.away_win.append(1)
            else:
                self.home_win.append('-')
                self.away_win.append('-')
        pl2020['Home_Win'] = self.home_win
        pl2020['Away_Win'] = self.away_win

        print('Home_Win:' , self.home_win)
        print('Away_Win: ', self.away_win)

    def _pandas(self):
        pl2020['Home_Team_ELO'] = self.home_elo_list
        pl2020['Away_Team_ELO'] = self.away_elo_list
        home_shots = [int(x) + int(y) for x, y in zip(self.home_sot, self.home_shots_off)]
        away_shots = [int(x) + int(y) for x, y in zip(self.away_sot, self.away_shots_off)]
        pl2020['Home_Shots'] = home_shots
        pl2020['Away_Shots'] = away_shots
        home_shot_acc = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(self.home_sot, home_shots)]
        away_shot_acc = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(self.away_sot, away_shots)]
        pl2020['Home_Shot_Accuracy'] = home_shot_acc
        pl2020['Away_Shot_Accuracy'] = away_shot_acc
        pl2020['Home_Possession'] = self.home_possession_1
        pl2020['Away_Possession'] = self.away_possession_1
        pl2020['Home_Total_Passes'] = self.home_total_passes
        pl2020['Away_Total_Passes'] = self.away_total_passes
        home_successful_pass_avg = [int(t) / int(s) if int(s) != 0 else 0 for t, s in zip(self.home_successful_passes, self.home_total_passes)]
        away_successful_pass_avg = [int(v) / int(w) if int(w) != 0 else 0 for v, w in zip(self.away_successful_passes, self.away_total_passes)]
        pl2020['Home_Successful_Pass_Avg'] = home_successful_pass_avg
        pl2020['Away_Successful_Pass_Avg'] = away_successful_pass_avg

    def _to_csv(self):
        pl2020.to_csv(f'{os.getcwd()}/PL2020_2.csv', sep=',', index=False)

    def scrape(self):
        counter = 0
        for url in self.urls:
            self._scrape_elo(url)
            self._scrape_shots(url)
            self._scrape_possession_passes(url)

            counter += 1

            if counter == 3:
                break

        # self._pandas()
        # self._to_csv()

if __name__ == '__main__':
    scraper = Scraper_PL2020()
    scraper.scrape()
    pl2020
    finish = time.perf_counter()
    print(f'Time taken: {finish-start}')


# %%
