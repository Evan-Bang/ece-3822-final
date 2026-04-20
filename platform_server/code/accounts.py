"""
Player accounts and authentication.
Create account / login: Dictionary with keys as usernames and passwords stored as encrypted hashes
View player profile: provide information about play times, games played, scores, etc. from the json database, depending on which stats are public public via flags
"""
import sys
sys.path.append('../..')
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable


class Profile:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class AccountManager:
    def __init__(self):
        self.players = ArrayList()

    def create_account(self, username, password):
        """
        Create a new account with the given username and password
         - Check if username is already taken
         - If not, create a new Player and add to the list of players
         - If account was created successfully, return True, else False
        """
        pass

    def authenticate(self, username, password):
        """
        Authenticate a user with the given username and password
         - Check if username exists and password matches
         - If authentication is successful return True, else False
        """
        pass
