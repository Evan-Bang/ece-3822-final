"""
Python server for the Arcade
"""

import socket
import asyncio
from pathlib import Path
import json
import time
import os
import sys
from urllib import response
sys.path.append('../..')
import leaderboard as lb
import data_ingest as di
from game_server_launcher import game_server_launcher
from game import Game_manager
import accounts as acc
from datastructures.array import ArrayList

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

class PlatformServer:
    def __init__(self, host='localhost', port=50074):
        self.host = host
        self.port = port

        games_dir = ROOT / "games"
        server_bin = ROOT / "game_server" / "server_text_smoother"
        ports_file = ROOT / "ports.txt"

        # Main features:
        self.accounts = acc.AccountManager()

        self.gm = Game_manager(str(games_dir))
        self.gsm = game_server_launcher(
            str(games_dir),
            str(server_bin),
            str(ports_file)
        )
        
        # Clients
        self.clients = ArrayList() # list of connected clients

    async def start_server(self): # starts the server and listens for incoming connections
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f'Server started on {self.host}:{self.port} at {time.ctime()}')
        self.gsm.launch_servers()
        async with server:
            await server.serve_forever() # keeps the server running
    
    # Process client requests and provide appropriate responses based on the request type (e.g., login, account creation, leaderboard queries, etc.)
    async def handle_client(self, reader, writer):
        client_socket = writer.get_extra_info('socket')
        # SAVE THE NAME HERE while the connection is active
        addr = writer.get_extra_info('peername') 
        
        self.clients.append(client_socket)
        print(f'New client connected: {addr} at {time.ctime()}') 

        while True:
            try:
                data = await reader.readline()
                if not data:
                    break
                message = json.loads(data.decode().strip())
                response = await self.process_message(message)

                if response is not None:
                    writer.write((json.dumps(response) + "\n").encode())
                    print("Received:", message)
                    print("Sending:", response)
                    await writer.drain()
            
            except Exception as e:
                print(f'Oops, something broke: {e}')
                break

        # USE THE SAVED ADDR HERE instead of client_socket.getpeername()
        print(f'Client disconnected: {addr} at {time.ctime()}')
        
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            
        writer.close()
        await writer.wait_closed()
    
    async def process_message(self, message): # processes incoming client messages and generates appropriate responses
        request_type = message.get('type')
        
        # Aunthentication and account management
        if request_type == 'login':
            username = message.get('username')
            password = message.get('password')
            success, message = self.accounts.authenticate(username, password) # authenticate the user and return success status and message
            return {'success': success, 'message': message}
        
        elif request_type == 'game_summary':
            username = message.get('username')
            score = message.get('score')
            playtime = message.get('playtime')
            game_name = message.get('game_name', 'default_game') 
            username = message.get('username')
            account = self.accounts.accounts.get(username)
            account.build_session(message)
            print(f"Received summary from C++: {username} scored {score} in {game_name}")

            # Update the score leaderboard
            self.gm.add_score_lb(game_name, score, username)
            
            # Update the time leaderboard
            self.gm.add_time_lb(game_name, playtime, username)

            # This is just for debugging
            print(f"top 5 scores for {game_name} : {self.gm.games.get(game_name).score_leader_board.get_top_n(5)}")
            print(f"top 5 playtimes for {game_name}: {self.gm.games.get(game_name).time_leader_board.get_top_n(5)}")
            return {'success': True, 'message': 'Summary processed'}

        elif request_type == 'create_account':
            username = message.get('username')
            password = message.get('password')
            success, message = self.accounts.create_account(username, password)
            return {'success': success, 'message': message}
        
        # get sessions
        elif request_type == 'get_sessions':
            username = message.get('username')
            account = self.accounts.accounts.get(username)
            sessions = [session for session in account.sessions]
            return {'success': True, 'sessions': sessions}
        elif request_type == 'get_leaderboard':
            game_name = message.get('game_name')
            score_lb = self.gm.games.get(game_name).score_leader_board.get_top_n(10)
            time_lb = self.gm.games.get(game_name).time_leader_board.get_top_n(10)
            return {'success': True, 'score_leaderboard': score_lb, 'time_leaderboard': time_lb}
        elif request_type == 'get_user_data':
            username = message.get('username')
            account = self.accounts.accounts.get(username)
            if account:
                user_data = {
                    'username': account.username,
                    'sessions': [session.encode() for session in account.sessions]
                }
                return {'success': True, 'user_data': user_data}
            else:
                return {'success': False, 'message': 'User not found'}
        elif request_type == 'prefix_search':
            prefix = message.get('prefix')

            results = self.accounts.prefix_search_account(prefix)

            if results is None:
                results = []

            return {
                'success': True,
                'results': results
            }

        # Chat

        # Game hosting

        # Other request types
        
        else:
            return {'success': False, 'message': 'Unknown request type'}


if __name__ == "__main__":
    server = PlatformServer()
    asyncio.run(server.start_server())
   