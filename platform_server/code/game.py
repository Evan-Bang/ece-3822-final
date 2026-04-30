"""
game.py

Author: Owen Ringrose
Date: 4/23/2026

Game file for managing the different games
**** Revision History ****
-4/23/2026: file created
"""

from datastructures.array import ArrayList
from leaderboard import Leaderboard
from datastructures.hash_table import HashTable
import sys
import os

class Game:
    def __init__(self,filepath, title):
        self.title = title
        self.filepath = filepath
        self.score_leader_board = Leaderboard()
        self.time_leader_board = Leaderboard()

class Game_manager:
    def __init__(self, game_folder):
        # Key: Game Title (String), Value: Game Object
        self.games = HashTable()
        self.game_folder = game_folder
        self.load_games()

    def load_games(self):
        if not os.path.exists(self.game_folder):
            return

        for entry in os.listdir(self.game_folder):
            full_path = os.path.join(self.game_folder, entry)
            
            if os.path.isdir(full_path):
                # We use the folder name (entry) as the key
                new_game = Game(filepath=full_path, title=entry.lower())
                
                # Auto-load the leaderboard if the file exists
                score_file = os.path.join(full_path, "scores.json")
                if os.path.exists(score_file):
                    new_game.score_leader_board.load_from_json(score_file)
                
                # Store in dict
                self.games.set(entry, new_game)

    def get_game(self, title):
        return self.games.get(title.lower())
    
    def add_score_lb(self, game_name, value, user):
        if game_name.lower() in self.games:
            self.games.get(game_name.lower()).score_leader_board.add_score(user, value)
    
    def add_time_lb(self, game_name, time, user):
        if game_name.lower() in self.games:
            self.games.get(game_name.lower()).time_leader_board.add_score(user, time)

    
