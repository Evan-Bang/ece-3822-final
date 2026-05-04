"""
Player accounts and authentication.
Create account / login: Dictionary with keys as usernames and passwords stored as encrypted hashes
View player profile: provide information about play times, games played, scores, etc. from the json database, depending on which stats are public public via flags
"""
import sys
import os
from datetime import date as dt_date
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, root_path)
user_data_path = os.path.join(root_path, "user_data")
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable
from datastructures.prefix_tree import prefix_tree
import os
import hashlib
import json
import random

class Profile:
    """Profile class to store user data and game history. This is what is loaded into memory when a user logs in. It is also responsible for saving data to disk when changes are made."""
    def __init__(self, username, user_id_table):
        self.username = username
        self.sessions = ArrayList()
        if username not in user_id_table:
            raise ValueError("User does not exist")
        else:
            self.user_id = user_id_table.get(username)
        self.data_file = f'{user_data_path}/{self.user_id}.json'
        self.next_session_id = 1
        self.password = None
        self.initialize_data()

    def add_session(self, session):
        """ Add's session to the profile's game data. only used internally"""
        self.sessions.append(session)

    def create_session(self, game, time_played, score, date = None):
        """ function to create a session and add it to the profile also handles ID's"""
        session = Session(game, self.username, time_played, score, self.next_session_id, date)
        self.add_session(session)
        self.next_session_id += 1
        return session
    
    def build_session(self, summary, date = None):
        """ Builds session from a JSON message from the client. This is used when a session is sent from the client to be added to the profile. It extracts the relevant information from the JSON and creates a session object."""
        game = summary.get('game_name', 'Unknown Game')
        time_played = summary.get('playtime', 0) # Default to 0 seconds
        score = summary.get('score', 0)
        session = self.create_session(game,time_played,score, date)
        return session
    
    def initialize_data(self):
        """ Loads data from a json file."""
        # Load user data from file or create new file if it doesn't exist
        if self.user_id:
            self.data_file = f"{user_data_path}/{self.user_id}.json"
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    max_id = 0
                    for session_key, session in data['GAME_HISTORY'].items():
                        # Extract the actual ID from the key "SESSION_X"
                        current_id = int(session_key.split('_')[1])
                        session_data = Session(
                          session.get('GAME', 'Unknown'),
                            self.username,
                            session.get('PLAYTIME', 0),
                            session.get('SCORE', 0),
                            current_id,
                            session.get('DATE', None)
                        )
                        self.sessions.append(session_data)
                        if current_id >= max_id:
                            max_id = current_id + 1
                    self.next_session_id = max_id
                    self.password = data['PASSWORD_HASH']
            except FileNotFoundError:
                if self.user_id is not None:
                    self.save_data()   
    def save_data(self):
        """ Saves the profile data to a json file. It overwrites the existing file with the new data."""
        # save user data to file
        data = {}
        sessions = {}
        for session_data in self.sessions:
            sessions[f'SESSION_{session_data.id}'] = session_data.encode()
        data['USERNAME'] = self.username
        data['PASSWORD_HASH'] = self.password
        data['GAME_HISTORY'] = sessions
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def __eq__(self, other):
        if not hasattr(other, 'username') or not hasattr(other, 'user_id'):
            return False
        if ((self.username == other.username) and (self.user_id == other.user_id)):
            return True
        return False

class Session:
    """ Session class to store information from game history"""
    def __init__(self, game, username, time_played, score, id, date = None):
        self.game = game
        self.username = username
        self.time_played = time_played
        self.score = score
        self.id = id
        if isinstance(date, str):
            self.date = date
        elif date is None:
            self.date = dt_date.today().isoformat()
        else:
            # This handles cases where a date object is passed directly
            self.date = str(date)
    def encode(self):
        return {"GAME":self.game,"USERNAME":self.username,"PLAYTIME":self.time_played,"SCORE":self.score, "DATE": self.date}

class AccountManager:
    """
    Account manager created in server.py. Handles the accounts for the server. This is where the bulk of data is stored for our server
    """
    def __init__(self):
        self.players = ArrayList()
        self.usernames = prefix_tree()
        self.accounts = HashTable()
        self.ids = HashTable()
        try:
            with open(f"{user_data_path}/name_id.json", "r") as f:
                data = json.load(f)
                for username, user_id in data.items():
                    self.ids.set(username, user_id)
                    self.usernames.add_word(username)
        except FileNotFoundError:
            pass
        
    def create_account(self, username, password):
        """
        Create a new account with the given username and password
         - Check if username is already taken
         - If not, create a new Player and add to the list of players
         - If account was created successfully, return True, else False
        """
        if username not in self.usernames:
            # Generate salt
            self.usernames.add_word(username)
            salt = os.urandom(16)
            user_id = None
            i = 0
            while user_id is None:
                random_val = str(random.randint(1,99999)).zfill(5)

                if random_val not in self.ids:
                    user_id = random_val
                else:
                    i += 1
                    if i >= 100000:
                        return False
            self.ids.set(username, user_id)
            self.accounts.set(username, Profile(username, self.ids))
            data_file = f"{user_data_path}/{user_id}.json"
            # Hash password
            hashed = hashlib.sha256(salt + password.encode()).hexdigest()

            # Store as salt:hash
            password_storage = salt.hex() + ":" + hashed

            user_data = {
                "USERNAME": username,
                "PASSWORD_HASH": password_storage,
                "GAME_HISTORY": {}
            }
            with open(f"{user_data_path}/name_id.json", "r") as d:
                data = json.load(d)
            with open(f"{user_data_path}/name_id.json","w") as w:
                data[username] = user_id
                json.dump(data, w, indent=4)
            with open(data_file, "w") as f:
                json.dump(user_data, f, indent=4)
            self.accounts.set(username, Profile(username, self.ids))
            return ('True', "Account created successfully")
        else:
            return 'False'

    def authenticate(self, username, password):
        """
        Authenticate a user with the given username and password
         - Check if username exists and password matches
         - If authentication is successful return True, else False
        """
        with open(f"{user_data_path}/name_id.json","r") as d:
            name_id_data = json.load(d)
        if username not in name_id_data:
            return False
        else:
            user_id = name_id_data[username]
        data_file = f"{user_data_path}/{user_id}.json"
        with open(data_file, "r") as f:
            user_data = json.load(f)

        stored = user_data["PASSWORD_HASH"]
        salt_hex, stored_hash = stored.split(":")

        salt = bytes.fromhex(salt_hex)

        # Hash entered password with same salt
        new_hash = hashlib.sha256(salt + password.encode()).hexdigest()

        if new_hash == stored_hash:
            self.accounts.set(username, Profile(username, self.ids))
            return ('True','Login successful')
        else:
            return False
    def prefix_search_account(self, prefix):
        if self.usernames.is_prefix(prefix):
            return self.usernames.find_words(prefix)
        else:
            return ArrayList()
    def get_profile(self, username):
        # Check if they are already in the "active" memory
        account = self.accounts.get(username)
        if account:
            return account
            
        # If not, check if they exist in our ID registry
        if username in self.ids:
            # Load the profile from the disk into the HashTable
            new_profile = Profile(username, self.ids)
            self.accounts.set(username, new_profile)
            return new_profile
            
        return None
    
# test to initlialize our acounts so we can log in.
if __name__ == "__main__":
    username1 = "tuf08092"
    username2 = "tut69764"
    password = "nullptr"
    manager = AccountManager()
    account = manager.create_account(username1,password)
    account2 = manager.create_account(username2,password)



    
