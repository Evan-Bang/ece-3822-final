import sys
import os
import json
from settings import *
import socket
import subprocess
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable
import time
class ServerHandler:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)

        self.ip_address = IP_ADDRESS
        self.port = PLATFORM_SERVER
        self.connected = False

        self.tunnel_started = False

    def start_tunnel(self, username):
        if self.tunnel_started:
            return

        subprocess.Popen([
            'ssh',
            '-N',
            '-L', f'50074:localhost:{self.port}',
            f'{username}@ece-000.eng.temple.edu'
        ])

        self.tunnel_started = True
    def connect(self, username):
        self.start_tunnel(username)

        if self.connected:
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)

        for _ in range(5):
            try:
                self.client_socket.connect((self.ip_address, 50074))
                self.connected = True
                return
            except (ConnectionRefusedError, OSError):
                time.sleep(1)

        raise Exception("Could not connect to server")
    def disconnect(self):
        if self.connected:
            self.client_socket.close()
            self.connected = False
            print("Disconnected from server.")
    def handle_request(self, request):
        # Process the incoming request
        if not self.connected:
            print("ERROR: Not connected to server")
            return None
        response = self.process_request(request)
        return response
    def process_request(self, request):
        try:
            if not self.connected:
                return None

            data = json.dumps(request).encode('utf-8')
            self.client_socket.sendall(data)

            response = self.client_socket.recv(BUFFER_SIZE)
            return json.loads(response.decode('utf-8'))

        except socket.timeout:
            print("Server timeout")
            return None
        except BrokenPipeError:
            print("Connection broken")
            self.connected = False
            return None
    def search_usernames(self, prefix):
        request = {'type': 'prefix_search', 'prefix': prefix}
        response = self.process_request(request)
        return response.get('results', [])
      
class UserData:
    def __init__(self, handler):
        self.handler = handler
        self.user_id = None
        self.game_history = ArrayList()
        self.data_file = None
        self.logged_in = False

    def create_account(self, username, password):
        self.handler.connect(username)
        request = {'type': 'create_account', 'username': username, 'password': password}
        response = self.handler.process_request(request)
        return response
    def login(self, username, password):
        self.handler.connect(username)
        request = {'type': 'login', 'username': username, 'password': password}
        response = self.handler.process_request(request)
        if response:
            self.logged_in = response.get('success')
            self.user_id = response.get('user_id')
    def get_user_data(self, target_username):
        request = {'type': 'get_user_data', 'username': target_username}
        response = self.handler.process_request(request)  
        return response      
    
    def get_id(self, username):
        request = {'type': 'get_user_id', 'username': username}
        response = self.handler.process_request(request)
        return response.get('user_id')
        
    def add_game_history(self, game, play_time, date):
        self.game_history.append((game, play_time, date))
    def get_game_history(self):
        return self.game_history
class GameData:
    def __init__(self, game_name):
        self.game_name = game_name
        self.leaderboard = ArrayList()
    def get_game_data(self):
        request = HashTable()
        request.set('type', 'get_game_data')
        request.set('game_name', self.game_name)

        return self.game_data
    def get_leaderboard(self):
        request = HashTable()
        request.set('type','leaderboard_query')
        request.set('game_name', self.game_name)

        return self.leaderboard