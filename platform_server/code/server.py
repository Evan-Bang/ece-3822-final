"""
Python server for the Arcade
"""

import socket
import asyncio
import json
import time
import sys
sys.path.append('../..')
import leaderboard as lb
import data_ingest as di
import accounts as acc
from datastructures.array import ArrayList
class PlatformServer:
    def __init__(self, host='localhost', port=50074):
        self.host = host
        self.port = port

        # Main features:
        self.accounts = acc.AccountManager()
        self.leaderboard = lb.Leaderboard()
        self.time_lb = lb.Leaderboard()
        self.chat = None # arcade chat Class
        self.games = None # multiplayer game server hosting Class

        # Clients
        self.clients = ArrayList() # list of connected clients

    async def start_server(self): # starts the server and listens for incoming connections
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f'Server started on {self.host}:{self.port} at {time.ctime()}')

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
                data = await reader.read(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                response = await self.process_message(message)

                if response is not None:
                    writer.write(json.dumps(response).encode())
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
            game_name = message.get('game_name', 'default_game') # Fallback if not sent

            print(f"Received summary from C++: {username} scored {score}")

            # 1. Update the score leaderboard
            self.leaderboard.add_score(username, score)
            
            # 2. Update the time leaderboard
            self.time_lb.add_score(username, playtime)
            print(f"top 5 scores : {self.leaderboard.get_top_n(5)}")
            print(f"top 5 playtimes: {self.time_lb.get_top_n(5)}")
            return {'success': True, 'message': 'Summary processed'}

        elif request_type == 'create_account':
            username = message.get('username')
            password = message.get('password')
            success, message = self.accounts.create_account(username, password)
            return {'success': success, 'message': message}
        
        # Leaderboard
        elif request_type == 'leaderboard_query':
            game_name = message.get('game_name')
            leaderboard_data = self.leaderboard.get_leaderboard(game_name)
            return {'success': True, 'leaderboard': leaderboard_data}
        
        # Chat

        # Game hosting

        # Other request types
        
        else:
            return {'success': False, 'message': 'Unknown request type'}


if __name__ == "__main__":
    server = PlatformServer()
    asyncio.run(server.start_server())