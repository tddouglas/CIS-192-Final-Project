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
print(all_rosters)


