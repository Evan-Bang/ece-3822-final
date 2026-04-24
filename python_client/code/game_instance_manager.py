import pygame
import sys
import subprocess
import time
from datetime import date
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from datastructures.array import ArrayList
class GameInstanceManager:
    def __init__(self):
        self.instances = ArrayList()
    def add_instance(self, instance):
        self.instances.append(instance)
    def remove_instance(self, instance):
        self.instances.remove(instance)
class RunInstance:
    def __init__(self, username, game):
        self.running = False
        self.current_instance = None
        self.singleplayer = True
        self.username = username
        # self.start_time = None
        # self.end_time = None
        # self.date = None
    def get_assigned_port(self):
        with open("../../Ports.txt", "r") as f:
            for line in f:
                if line.startswith(self.current_instance):
                    return int(line.split('=')[1].strip())
        return None
    def run(self, game):
        self.current_instance = game
        game_file = f"../../games/{self.current_instance}/code/game/main.py"
        self.assigned_port = self.get_assigned_port()
        if self.singleplayer:
            subprocess.Popen(["python", game_file, self.username])
        else:
            self.port_forward(self.current_instance)
            subprocess.Popen(["python", game_file, self.username, '--port', '8000'])
        self.running = True
        
        # self.start_time = time.time()
        # self.end_time = None
        # self.date = date.today()
    def port_forward(self):
        subprocess.Popen(['ssh', '-L', f'8000:localhost:{self.assigned_port}', f'{self.username}@ece-000.eng.temple.edu', '-N'])
        
    def stop(self):
        self.running = False
        self.current_instance = None
        # self.end_time = time.time()
    def is_running(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
    # def get_runtime(self):
    #     return self.end_time - self.start_time if self.end_time and self.start_time else None