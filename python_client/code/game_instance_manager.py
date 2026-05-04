"""
Handles running the games for the client. This includes launching the game processes and managing them.
This also handles setting up SSH tunnels to the game servers 
"""

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
    def stop_all_instances(self):
        for instance in self.instances:
            instance.stop()
        self.instances = ArrayList()
class RunInstance:
    def __init__(self, username):
        self.username = username
        self.current_game = None
        self.process = None
        self.running = False
        self.singleplayer = False
        self.assigned_port = None

        # Base path for reliability
        self.base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../")
        )

    # -----------------------------
    # Load port from Ports.txt
    # -----------------------------
    def get_assigned_port(self):
        ports_file = os.path.join(self.base_path, "ports.txt")

        try:
            with open(ports_file, "r") as f:
                lines = f.readlines()
                print(f"Ports.txt contents: {lines}")
                print(f"Looking for: 'GAME_{self.current_game.upper()}'")
                for line in lines:
                    print(f"  Checking line: {repr(line)}")
                    if line.startswith("GAME_" + self.current_game.upper()):
                        return int(line.split("=")[1].strip())
        except FileNotFoundError:
            print(f"Ports.txt not found at: {ports_file}")

        return None

    # -----------------------------
    # Launch the game
    # -----------------------------
    def run(self, game):
        self.current_game = game
        self.assigned_port = self.get_assigned_port()
        print(f"Assigned port for {game}: {self.assigned_port}")
        game_dir = os.path.join(self.base_path, "games", self.current_game, "code", "game")


        game_file = os.path.join(
            self.base_path,
            "games",
            self.current_game,
            "code",
            "game",
            "main.py"
        )

        if not os.path.exists(game_file):
            print(f"Game file not found: {game_file}")
            return

        # Start game process
        if self.singleplayer:
            self.process = subprocess.Popen([
                "python3",
                game_file,
                self.username
            ],
            cwd=game_dir
            )
        else:
            self.start_port_forward()

            self.process = subprocess.Popen([
                "python3",
                game_file,
                self.username,
                "--port",
                str(self.assigned_port)
            ],
            cwd=game_dir
            )

        self.running = True

    # -----------------------------
    # SSH tunnel setup
    # -----------------------------
    def start_port_forward(self):
        if not self.assigned_port:
            print("No port assigned for game")
            return

        subprocess.Popen([
            "ssh",
            "-L",
            f"{self.assigned_port}:localhost:{self.assigned_port}",
            f"{self.username}@ece-000.eng.temple.edu",
            "-N"
        ])

    # -----------------------------
    # Stop game process
    # -----------------------------
    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

        self.running = False
        self.current_game = None

    # -----------------------------
    # Check if still running
    # -----------------------------
    def is_running(self):
        return self.process is not None and self.process.poll() is None