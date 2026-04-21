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
    async def handle_client(self, reader, writer): # reader and writer are asyncio streams for communication with the client
        client_socket = writer.get_extra_info('socket') # get the underlying socket object for the client connection
        self.clients.append(client_socket) # add the incoming client socket to the ArrayList of connected clients
        print(f'New client connected: {client_socket.getpeername()} at {time.ctime()}') 

        while True:
            try:
                data = await reader.read(1024) # read data from client
                if not data:
                    break
                message = json.loads(data.decode()) # decode and parse JSON message
                response = await self.process_message(message) # process the message and generate a response

                if response is not None:
                    writer.write(json.dumps(response).encode()) # send response back to client
                    await writer.drain() # ensure data is sent
            
            except Exception as e:
                print(f'Oops, something broke: {e}')
                break
        print(f'Client disconnected: {client_socket.getpeername()} at {time.ctime()}')
        self.clients.remove(client_socket) # remove the client socket from the list of connected clients
        writer.close() # close the connection with the client
        await writer.wait_closed() # wait until the connection is fully closed
    
    async def process_message(self, message): # processes incoming client messages and generates appropriate responses
        request_type = message.get('type')
        
        # Aunthentication and account management
        if request_type == 'login':
            username = message.get('username')
            password = message.get('password')
            success, message = self.accounts.authenticate(username, password) # authenticate the user and return success status and message
            return {'success': success, 'message': message}
        
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