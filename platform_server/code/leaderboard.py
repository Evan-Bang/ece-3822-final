"""
Leaderboard manager
"""

import json
from data_ingest import load_leaderboard_data as load_data
from datastructures.BST import BST

class Leaderboard:
    """
    A binary search tree stores (score, username) tuples for each game.
    The tree is sorted by score, with username as a tiebreaker.
    """
    def __init__(self):
        self.leaderboards = ArrayList() # list of BSTs, one for each game
        

    def update_scores(self, game, username, score):
        """
        update scores on the leaderboard for the given game and username
        """
        pass

    def get_top_scores(self, game,n=10):
        """
        return the top n sorted(scores) for the given game
        """
        pass
        
    def get_player_scores(self, game, username):
        """
        return scores for the given game and username
        """
        pass
    
    def load_leaderboard(self):
        """
        load the leaderboard data from the json database and populate the BSTs
        """
        self.data = load_data()
        # for each game, create a BST and insert the scores
        for (game_name, players_table) in self.data:
            bst = BST()
            for username in players_table:
                metric = players_table[username]
                # insert score and username as a tuple. sort based on score, but username would be tiebreaker
                bst.insert((metric, username)) 
            self.leaderboards.append(bst)
