"""
Dataset loading and cleaning
""" 

import json
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
    pass