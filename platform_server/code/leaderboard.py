"""
leaderboard.py

Author: Owen Ringrose
Date: 4/23/2026

leaderboard class using BST and Hashtable
**** Revision History ****
-4/23/2026: file created
"""
import sys
import json
sys.path.append('../..')
from datastructures.BST import BST
from datastructures.leaderboard_member import leaderboard_member
from datastructures.hash_table import HashTable
from datastructures.array import ArrayList

class Leaderboard:
    """
    A binary search tree stores leaderboard objects as nodes, compared first by score and then userid as tiebreaker
    Uses a hashmap for constant time acess to an individual's score
    """
    def __init__(self):
        self.score_tree = BST()
        self.score_table = HashTable() #Score table keyed by uuid

    def add_score(self, uuid, score):
        """
        Adds a score to the leaderboard
        If the user is already in leaderboard then check if the new score is higher, if so replace, if not return false
        """
        # Instantiate object for leaderboard
        if uuid in self.score_table:
            prev_score = self.score_table.get(uuid)
            if score >= prev_score:
                self.score_tree.delete(leaderboard_member(uuid, prev_score))
                self.score_table.set(uuid, score)
                score_object = leaderboard_member(uuid, score)
                self.score_tree.insert(score_object)
                return True
            return False
        else:
            self.score_table.set(uuid, score)
            score_object = leaderboard_member(uuid, score)
            self.score_tree.insert(score_object)
        
            return True
    
    def get_top_n(self,n):
        """
        returns the top n players. 
        returned in tuples as (uuid, score)
        """
        result = ArrayList()
        top_n = self.score_tree.get_top_n(n)
        for l_object in top_n:
            unpacked = (l_object.uuid, l_object.score)
            result.append(unpacked)
        return result
    
    def ranged_query(self, bot_score, top_score):
        """
        returns the players between a range. 
        returned in tuples as (uuid, score)
        """
        # we have to make fake members for comparisons to work
        bot_object = leaderboard_member(0, bot_score)
        top_object = leaderboard_member(0, top_score)

        result = ArrayList()
        between = self.score_tree.range_query(bot_object, top_object)

        for l_object in between:
            unpacked = (l_object.uuid, l_object.score)
            result.append(unpacked)
        return result


    def get_all_sorted(self): 
        """
        returns the players sorted low to high
        returned as a list of tuples as (uuid, score)
        """
        result = ArrayList()
        sorted = self.score_tree.get_elements_sorted()
        for l_object in sorted:
            unpacked = (l_object.uuid, l_object.score)
            result.append(unpacked)
        return result

    def get_player_score(self, uuid):
        """
        returns a given players score
        """
        return self.score_table.get(uuid)


    def load_from_json(self, file_path):
        """
        Loads scores from a JSON file and adds them to the leaderboard.
        Expected JSON format: {"uuid1": score_1, "uuid2": score_2}
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            # There is a python built in here but I think its fine as we are calling from library.
            for uuid, score in data.items():
                self.add_score(uuid, int(score))
                
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {file_path}.")


    def save_to_json(self, file_path):
        """
        Saves the current scores to a JSON file using the BST and ArrayList.
        """
        try:
            all_data = self.get_all_sorted()
            
            # Build the JSON
            json_output = "{\n"
            
            for i in range(len(all_data)):
                uuid, score = all_data[i]
                # Format: "uuid": score
                line = f'    "{uuid}": {score}'
                
                # Add a comma if it's not the last element
                if i < len(all_data) - 1:
                    line += ","
                
                json_output += line + "\n"
            
            json_output += "}"

            with open(file_path, 'w') as f:
                f.write(json_output)
                
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False

    def __len__(self):
        return self.score_table.size()