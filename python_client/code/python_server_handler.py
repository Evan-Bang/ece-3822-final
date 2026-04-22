from datastructures.array import ArrayList
from datastructures.hash_table import HashTable
import json
from settings import *
import socket
import subprocess
class ServerHandler:
    def __init__(self, server):
        self.server = server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = IP_ADDRESS
        self.port = SERVER_PORT
        self.connected = False
    def connect(self):
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
        response = self.process_request(request)
        return response
    def process_request(self, request, client):
        # This method should be overridden by subclasses to handle specific request types
        pass
    def port_forward(self, username):
        subprocess.Popen(['ssh', '-L', f'8080:localhost:{SERVER_PORT}', f'{username}@ece-000.eng.temple.edu', '-N'])
        
class LoginHandler(ServerHandler):
    def process_request(self, request, client):
        # Handle login request and return response
        client.send(json.dumps(request).encode())
        response = client.recv(BUFFER_SIZE)
        data = json.loads(response.decode('utf-8'))
        return data.get('success')
class CreateHandler(ServerHandler):
    def process_request(self, request, client):
        # Handle account creation request and return response
        client.send(json.dumps(request).encode())
        response = client.recv(BUFFER_SIZE)
        data = json.loads(response.decode('utf-8'))
        if data.get('success'):
            return data.get('user_id')
        else:
            return None
class PlayerDataHandler(ServerHandler):
    def process_request(self, request, client):
        # Handle player data request and return response
        client.send(json.dumps(request).encode())
        response = client.recv(BUFFER_SIZE)
        data = json.loads(response.decode('utf-8'))
        return data
class GameDataHandler(ServerHandler):
    def process_request(self, request, client):
        # Handle game data request and return response
        self.leaderboard = request.get('game_name')
        client.send(json.dumps(request).encode())
        response = client.recv(BUFFER_SIZE)
        self.data = json.loads(response.decode('utf-8'))
        return self.data
class UserData:
    def __init__(self, username):
        self.username = username
        self.user_id = self.get_id(username)
        self.game_history = ArrayList()
        self.data_file = f"userdata/{self.user_id}.json"
        self.logged_in = False
        self.initialize_data()
    def initialize_data(self):
        # Load user data from file or create new file if it doesn't exist
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.game_history = ArrayList(data.get('game_history', []))
        except FileNotFoundError:
            self.save_data()
    def create_account(self, username, password):
        request = HashTable()
        request.set('type', 'create_account')
        request.set('username', username)
        request.set('password', password)
        self.user_id = CreateHandler().process_request(request)
        pass
    def login(self, username, password):
        request = HashTable()
        request.set('type', 'login')
        request.set('username', username)
        request.set('password', password)
        self.logged_in = LoginHandler().process_request(request)
    def save_data(self):
        data = HashTable()
        data.set('username', self.username)
        data.set('user_id', self.user_id)
        data.set('game_history', self.game_history)
        with open(self.data_file, 'w') as f:
            json.dump(data, f)
    def get_id(self, username):
        request = HashTable()
        request.set('type', 'get_user_id')
        request.set('username', username)
        return PlayerDataHandler().process_request(request)
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
        self.game_data = GameDataHandler().process_request(request)
        return self.game_data
    def get_leaderboard(self):
        request = HashTable()
        request.set('type','leaderboard_query')
        request.set('game_name', self.game_name)
        self.leaderboard = ArrayList(GameDataHandler().process_request(request))
        return self.leaderboard