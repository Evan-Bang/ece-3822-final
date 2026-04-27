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
class ServerHandler:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = IP_ADDRESS
        self.port = SERVER_PORT
        self.connected = False
    def connect(self, username):
        self.port_forward(username)
        self.client_socket.connect((self.ip_address, self.port))
        try:
            message = "Connecting to server..."
            self.client_socket.sendall(message.encode('utf-8'))
            response = self.client_socket.recv(1024)
            if response.decode('utf-8') == "Connection successful":
                self.connected = True
                print("Connected to server successfully.")
        except Exception as e:
            print(f"Error occurred while connecting to server: {e}")
            self.client_socket.close()
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
        self.client_socket.send(json.dumps(request.to_dict()).encode())
        response = self.client_socket.recv(BUFFER_SIZE)
        return json.loads(response.decode('utf-8'))
    def port_forward(self, username):
        subprocess.Popen(['ssh', '-L', f'8080:localhost:{SERVER_PORT}', f'{username}@ece-000.eng.temple.edu', '-N'])
        

class UserData:
    def __init__(self, handler):
        self.handler = handler
        self.user_id = None
        self.game_history = ArrayList()
        self.data_file = None
        self.logged_in = False

    def create_account(self, username, password):
        self.handler.connect(username)
        request = HashTable()
        request.set('type', 'create_account')
        request.set('username', username)
        request.set('password', password)
        response = self.handler.process_request(request)
        return response
    def login(self, username, password):
        self.handler.connect(username)
        request = HashTable()
        request.set('type', 'login')
        request.set('username', username)
        request.set('password', password)
        response = self.handler.process_request(request)
        if response:
            self.logged_in = response.get('success')
            self.user_id = response.get('user_id')
    def get_user_data(self, target_username):
        request = HashTable()
        request.set('type','get_user_data')
        request.set('username',target_username)
        response = self.handler.process_request(request)  
        return response      
    
    def get_id(self, username):
        request = HashTable()
        request.set('type', 'get_user_id')
        request.set('username', username)
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