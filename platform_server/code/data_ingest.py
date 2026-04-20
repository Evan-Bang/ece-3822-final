"""
Dataset loading and cleaning
""" 

import json
import sys
sys.path.append('../..')
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable


def load_leaderboard_data():
    """
    Load the raw JSON database of all users and extract leaderboard-relevant data.

    Returns:
        An ArrayList where each element is a tuple:
            (game_name, HashTable).
        - game_name: <str>
        - players_table: HashTable mapping username -> relevant_metric

        Example Structure:
            ArrayList [
                ("game1", HashTable {
                    "emmanuel": 456,
                    "manny": 123,
                    "emma": 789,
                    ...
                }),
                ("game2", HashTable {
                    "emmanuel": 987,
                    "emma": 321,
                    "leunamme": 654,
                    ...
                }),
                ...
            ]
    """
    with open('database.json', 'r') as f:
        raw_data = json.load(f)
    leaderboard_data = ArrayList()
    game_tables = HashTable()

    # iterate through each username in the raw data 
    for username in raw_data:
        username = user["username"]
        games = user["games"]
        
        # for each game, grab the relevant metric and insert it into the corresponding game table.
        for game_name in games:
            metric_data = games[game_name]

            # assuming the relevant metric for the leaderboard is either "score" or "playtime"
            if "score" in metric_data:
                metric = metric_data["score"]
            elif "playtime" in metric_data:
                metric = metric_data["playtime"]
            else:
                continue  # skip if no relevant metric is found
            
            # if the game doesn't have a table yet, create one
            if game_name not in game_tables:
                game_tables.insert(game_name, HashTable())
            
            players_table = game_tables[game_name]
            players_table.insert(username, metric)
    # format the data as an ArrayList of tuples (game_name, players_table)
    for game_name in game_tables:
        leaderboard_data.append((game_name, game_tables[game_name]))
    return leaderboard_data