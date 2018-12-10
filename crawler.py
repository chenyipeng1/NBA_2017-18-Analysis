import requests
import json
import sys
import bs4
from bs4 import BeautifulSoup
from bs4 import Comment

CACHE_NAME_1 = 'team.json'
CACHE_NAME_2 = 'player.json'

def get_team_cache_data():
    try:
        with open(CACHE_NAME_1, 'r') as cache_file:
            cache_contents = cache_file.read()
            CACHE_DICTION = json.loads(cache_contents)
    except:
        CACHE_DICTION = {}
    
    return CACHE_DICTION

def get_player_cache_data():
    try:
        with open(CACHE_NAME_2, 'r') as cache_file:
            cache_contents = cache_file.read()
            CACHE_DICTION = json.loads(cache_contents)
    except:
        CACHE_DICTION = {}
    
    return CACHE_DICTION


def get_data():
    #get team_data
    team_data = get_team_cache_data()
    if not team_data:
        print("get new team data")
        base_url = "https://www.basketball-reference.com/leagues/NBA_2018.html#all_team-stats-per_game"
        page_request = requests.get(base_url).text
        team_data = BeautifulSoup(page_request, 'html.parser')
        with open(CACHE_NAME_1, 'w') as cache_file:
            cache_file.write(json.dumps(page_request, indent = 4))
    
    #get player_data
    player_data = get_player_cache_data()

    if not player_data:
        print("get new player data")
        base_url = "https://www.basketball-reference.com/leagues/NBA_2018_per_game.html"
        page_request = requests.get(base_url).text
        player_data = BeautifulSoup(page_request, 'html.parser')
        with open(CACHE_NAME_2, 'w') as cache_file:
            cache_file.write(json.dumps(page_request, indent = 4))

    return team_data, player_data
    