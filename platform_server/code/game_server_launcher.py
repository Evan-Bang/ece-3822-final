"""
game_server_launcher.py

Author: Owen Ringrose
Date: 4/25/2026

game server launcher.
**** Revision History ****
-4/25/2026: file created
"""
import os
import subprocess
import sys
import time
sys.path.append('../..')
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable

class game_server_launcher:
    """
    Class to manage the launching of the C++ game servers, gets ports from a file, gets games from folder.
    """
    def __init__(self, games_folder, server_bin, ports_file):
        self.games = ArrayList()
        self.ports = HashTable() # port numbers keyed based on game_name
        self.procesess = ArrayList()
        self.running = False
        self.games_folder = games_folder
        self.server_bin = server_bin
        self.ports_file = ports_file
        self._game_names_from_file()
        self._ports_from_file()

    def _game_names_from_file(self):
        """Helper function to load game names into array"""
        if not os.path.exists(self.games_folder):
            raise FileNotFoundError
        for folder in os.listdir(self.games_folder):
            self.games.append(folder)
        
    
    def _ports_from_file(self):
        """Helper function to load ports into dict"""
        if not os.path.exists(self.ports_file):
            raise FileNotFoundError
        with open(self.ports_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("GAME_") and "_PORT=" in line:
                    try:
                        parts = line.split('=')
                        folder_name = parts[0].replace("GAME_", "").replace("_PORT", "").strip()
                        port = parts[1].strip()
                        self.ports.set(folder_name.lower(), port)
                        print(f"{folder_name.lower()} : {port}")
                    except Exception:
                        continue
    
        
    def launch_servers(self):
        """
        Launches server binaries
        """
        # send server output here so we dont spam stdout
        output_dest = subprocess.DEVNULL 
        if not os.path.exists(self.server_bin):
            raise FileNotFoundError
        for game in self.games:
            proc = subprocess.Popen(
                            [self.server_bin, "--port", self.ports.get(game), "-n", game],
                            stdout=output_dest)
            self.procesess.append(proc)

    def stop_servers(self):
         """
         terminates the running servers
         """
         for proc in self.procesess:
                proc.terminate()

        




gsl = game_server_launcher("../../Games", "../../game_server/server_text_smoother", "../../ports.txt")
gsl.launch_servers()
print(gsl.games)
time.sleep(10)
gsl.stop_servers()
