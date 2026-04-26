"""
Player accounts and authentication.
Create account / login: Dictionary with keys as usernames and passwords stored as encrypted hashes
View player profile: provide information about play times, games played, scores, etc. from the json database, depending on which stats are public public via flags
"""
import sys
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, root_path)
user_data_path = os.path.join(root_path, "user_data")
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable
import os
import hashlib
import json
import random
class Profile:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class AccountManager:
    def __init__(self):
        self.players = ArrayList()
        self.usernames = ArrayList()
        self.ids = ArrayList()
    def create_account(self, username, password):
        """
        Create a new account with the given username and password
         - Check if username is already taken
         - If not, create a new Player and add to the list of players
         - If account was created successfully, return True, else False
        """

        # Load existing usernames and ids
        with open(f"{user_data_path}/name_id.json", "r") as d:
            data = json.load(d)
        # Check if username already exists on name_id.json
        if username in data:
            return False # username has already been taken

        if username not in self.usernames:
            # Generate salt
            self.usernames.append(username)
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
            self.ids.append(user_id)
            data_file = f"{user_data_path}/{user_id}.json"
            # Hash password
            hashed = hashlib.sha256(salt + password.encode()).hexdigest()

            # Store as salt:hash
            password_storage = salt.hex() + ":" + hashed

            user_data = {
                "USERNAME": username,
                "PASSWORD_HASH": password_storage,
                "GAME_DATA": {
                    "SURVIVING_1111": {"PLAY_TIME": "", "SESSIONS": {}, "SCORE": ""},
                    "THELLUSOMA": {"PLAY_TIME": "", "SESSIONS": {}, "SCORE": ""},
                    "LIZZIES_ADVENTURE": {"PLAY_TIME": "", "SESSIONS": {}, "SCORE": ""}
                }
            }
            with open(f"{user_data_path}/name_id.json", "r") as d:
                data = json.load(d)
            with open(f"{user_data_path}/name_id.json","w") as w:
                data[username] = user_id
                json.dump(data, w, indent=4)
            with open(data_file, "w") as f:
                json.dump(user_data, f, indent=4)
            return True
        else:
            return False

    def authenticate(self, username, password):
        """
        Authenticate a user with the given username and password
         - Check if username exists and password matches
         - If authentication is successful return True, else False
        """
        with open(f"{user_data_path}/name_id.json","r") as d:
            name_id_data = json.load(d)
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
            return True
        else:
            return False
            