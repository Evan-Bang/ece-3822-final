import pygame
from datastructures.array import ArrayList
import subprocess
import time
from datetime import date
class GameInstanceManager:
    def __init__(self):
        self.instances = ArrayList()
    def add_instance(self, instance):
        self.instances.append(instance)
    def remove_instance(self, instance):
        self.instances.remove(instance)
class RunInstance:
    def __init__(self, username):
        self.running = False
        self.current_instance = None
        self.singleplayer = True
        self.username = username
        # self.start_time = None
        # self.end_time = None
        # self.date = None
    def run(self, game):
        game_file = f"../../games/{game}/code/game/main.py"
        if self.singleplayer:
            subprocess.Popen(["python", game_file, self.username])
        else:
            self.port_forward(game)
            subprocess.Popen(["python", game_file, self.username, '--port', '8000'])
        self.running = True
        self.current_instance = game
        # self.start_time = time.time()
        # self.end_time = None
        # self.date = date.today()
    def port_forward(self, game):
        if game == "Surviving 1111":
            subprocess.Popen(['ssh', '-L', '8000:localhost:80078', f'{self.username}@ece-000.eng.temple.edu', '-N'])
        elif game == "Thellusoma":
            subprocess.Popen(['ssh', '-L', '8000:localhost:80061', f'{self.username}@ece-000.eng.temple.edu', '-N'])
        elif game == "Lizzies Adventure":
            subprocess.Popen(['ssh', '-L', '8000:localhost:80074', f'{self.username}@ece-000.eng.temple.edu', '-N'])
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