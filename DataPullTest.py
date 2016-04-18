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
from sklearn import decomposition
from sklearn import datasets

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
    print "got here"
    all_rosters = {}
    franchise_codes = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN',
                       'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
                       'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO',
                       'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    for code in franchise_codes:
        print "got here"
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
    print all_rosters
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

def create_matrix():
    franchise_codes = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN',
                       'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA',
                       'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO',
                       'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    franchise_numbers = [float(i) for i in xrange(31)]
    # create dictionary of franchise codes to numbers
    code_to_number = dict(zip(franchise_codes, franchise_numbers))
    url = "http://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2016&year_max=2016&team_id=&opp_id=&is_range=N&is_playoffs=N&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=blk&c1comp=gt&c1val=0&c2stat=orb&c2comp=gt&c2val=0&c3stat=opp_off_rtg&c3comp=gt&c3val=0&c4stat=off_rtg&c4comp=gt&c4val=0&order_by=pts&order_by_asc=&offset=0"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    games = soup.findAll("tr", class_=[u''])[2:]
    list_of_game_stats = []
    target = []
    for game in games:
#         For some reason <tr class=" thead"> satisfies class_=[u''] even though 
#         "" != " thead" so I filter those out here. If you can figure out a fix
#         so that those classes don't get picked up in games then please implement.
        if game["class"] == [u'', u'thead']:
            continue
        raw_game_stats = game.find_all("td")
        # convert the franchise codes to numbers
        team1_id = code_to_number[raw_game_stats[2].get_text()]
        team2_id = code_to_number[raw_game_stats[4].get_text()]
        # create a single row of the matrix with stats for one game
        game_stats = [team1_id] + [team2_id] + \
            [float(raw_game_stats[i].get_text()) for i in xrange(6, 61)]
        # add row to list of rows to be made into numpy array
        list_of_game_stats.append(game_stats)
        # set binary vector target data by comparing points scored
        outcome = 1 if game_stats[15] > game_stats[42] else 0
        target.append(outcome)
        
    target = np.array(target)
    data = np.array(list_of_game_stats)
    # do PCA stuff
    X = data
    print X
    y = target
    pca = decomposition.PCA(n_components=10)
    pca.fit(X)
    X = pca.transform(X)
    print X


def main():
   create_matrix()

if __name__ == "__main__":
    main()

