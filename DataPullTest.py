'''
Created on Mar 16, 2016

@author: Alex
'''
import numpy as np
import scipy as sp
import matplotlib
import csv as csv
import urllib2
from bs4 import BeautifulSoup, SoupStrainer
import requests
from requests.auth import HTTPBasicAuth
import django
import re


"""r = requests.get('http://api.sportsdatabase.com/nfl/query.json?sdql=date%2Cpoints%40team%3DBears%20and%20season%3D2011&output=json&api_key=guest')
print(r.status_code)
print(r.text)"""


"""player_page_links = []
for i in range(0, 26):
    response = urllib2.urlopen('http://www.basketball-reference.com/players/' + chr(i + 97))
    soup = BeautifulSoup(response.read(), 'html.parser', parseOnlyThese=SoupStrainer('strong'))
    for link in soup.find_all('a'):
        player_page_links.append(str('http://www.basketball-reference.com' + link['href']))
    print(player_page_links)
"""

def scrape_rosters():
    """Scrapes the rosters of every team for individual player stats, returns
    dict of numpy arrays"""
    all_rosters = {}
    franchise_codes = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN',
                       'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
                       'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO',
                       'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    for code in franchise_codes:
        url = 'http://www.basketball-reference.com/teams/' + code +\
            '/2015.html#totals::none'
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response.read(), 'html.parser',
                             parse_only=SoupStrainer(id='all_totals'))
        all_stats = []
        for td in soup.findAll('td'):
            all_stats.append(td.string)
        partitioned = []
        for i in range(0, len(all_stats), 28):
            partitioned.append(all_stats[i:i+28])
        roster_array = np.array(partitioned)
        all_rosters[code] = roster_array
    return all_rosters
    pass


def scrape_rivalry_history(team_code, opponent_code):
"""Scrapes history of team v. team. Results returned as numpy 2D array with date 
    and pt difference. 
    E.g. BOS wins by 7 pts against NOH on 4/3/16: [[u'Sun, Apr 3, 2016' u'+7']...]"""
    url = 'http://www.basketball-reference.com/play-index/rivals.cgi?request=1'\
        + '&team_id=' + team_code + '&opp_id=' + opponent_code +'&is_playoffs='
    response = urllib2.urlopen(url)
    soup = BeautifulSoup(response.read(), 'html.parser',
                         parse_only=SoupStrainer('tbody'))
    raw_strings = []
    for td in soup.findAll('td'):
        raw_strings.append(td.string)
    date_diff_tuples = []
    for i in range(1, len(raw_strings), 16):
        date_diff_tuples.append((raw_strings[i], raw_strings[i + 10]))
    return np.array(date_diff_tuples)
    pass

