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
    def __init__(self):
        self.running = False
        self.game = None
        self.current_instance = None
        self.start_time = None
        self.end_time = None
        self.date = None
    def run(self, game, username):
        game_file = f"../../games/{game}/code/game/main.py"
        subprocess.Popen(["python", game_file, username])
        self.game = game
        self.running = True
        self.current_instance = game
        self.start_time = time.time()
        self.date = date.today()
    def stop(self):
        self.running = False
        self.current_instance = None
        self.end_time = time.time()
    def is_running(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
    def get_runtime(self):
        return self.end_time - self.start_time if self.end_time and self.start_time else None