import pygame
from settings import *
from support import import_folder
from inventory import Inventory
from character import *
import json
from subcharacter import *
from datastructures.array import ArrayList
from datastructures.patrol_path import PatrolPath
from datastructures.waypoint import Waypoint
with open ("encounters.json","r") as f:
    ENCOUNTER_DATA = json.load(f)
class TurnOrder(ArrayList):
    def __init__(self, characters=None, initial_capacity=10):
        super().__init__(initial_capacity)
        self.characters = characters
    def peek(self):
        """
        Return the top item without removing it.
        
        Returns:
            The item on top of the queue, or None if empty
        """
        index = self._size - 1
        data = self._data[index]
        return data
    def push(self,character, index=0):
        if self._size == self._capacity:
            self._capacity *= 2
            new_data = [None] * self._capacity
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = character
        self._size += 1
        pass
    def pop(self):
        """
        Remove and return the top item from the queue.
        
        Returns:
            The item that was on top of the queue, or None if empty
        """
        index = self._size - 1
        data = self._data[index]
        self.remove(self._data[index])
        return data
    def get_turn_order(self):
        return self._data
class Battle:
    def __init__(self,player,characters):
        self.characters = characters
        self.turn_order = TurnOrder(characters)
        self.battle_map = BattleMap(player)

    def turn_cycle(self):
        for entity in self.turn_order:
            current_character = entity
            current_character.take_turn()
            self.pop()
    def create_turn_order(self):
        sorted_chars = sorted(self.characters, key=lambda c: c.agility, reverse=True)
        for char in sorted_chars:
            if char not in self.turn_order:
                self.turn_order.push(char)

class BattleUI:
    def __init__(self):
        self.map_rect = pygame.Rect(0, 0, WIDTH, MAP_HEIGHT)
        self.ui_rect  = pygame.Rect(0, MAP_HEIGHT, WIDTH, UI_HEIGHT)
    def draw_ui(self, screen, player):
        pygame.draw.rect(screen, (30, 30, 30), self.ui_rect)

        font = pygame.font.SysFont("consolas", 24)


        hp_text = font.render(f"HP: {player.hp}/{player.hp_max}", True, (200, 50, 50))
        screen.blit(hp_text, (20, MAP_HEIGHT + 20))


        ap_text = font.render(f"AP: {player.ap}", True, (50, 200, 50))
        screen.blit(ap_text, (20, MAP_HEIGHT + 60))


        weapon_text = font.render(f"Weapon: {player.weapon.name}", True, (200, 200, 200))
        screen.blit(weapon_text, (250, MAP_HEIGHT + 20))
class BattleMap:
    def __init__(self, level, center_character, width=50, height=50):
        self.level = level
        self.width = width
        self.height = height
        self.center_character = center_character


        player_x, player_y = center_character.tile_x, center_character.tile_y
        top_left_x = max(player_x - width // 2, 0)
        top_left_y = max(player_y - height // 2, 0)

        top_left_x = min(top_left_x, level.width_tiles - width)
        top_left_y = min(top_left_y, level.height_tiles - height)
        self.top_left_tile = (top_left_x, top_left_y)


        self.tiles = [
            [
                level.get_tile(x, y)
                for x in range(top_left_x, top_left_x + width)
            ]
            for y in range(top_left_y, top_left_y + height)
        ]

        self.characters = []
    def create_encounter(self, encounter_number, encounter_type, level=1):
        if encounter_type == "RANDOM":
            encounter_instance = ENCOUNTER_DATA[encounter_type][level][encounter_number]
        else:
            encounter_instance = ENCOUNTER_DATA[encounter_type][encounter_number]
        return encounter_instance
    def create_encounter_characters(self, encounter_instance):
        enemies = ArrayList()
        for character in encounter_instance:
            if character["TYPE"] == "MELEE":
                enemies.append(Melee(character))
            elif character["TYPE"] == "RANGED":
                enemies.append(Ranged(character))
            else:
                enemies.append(Enemy(character))
        return enemies
            
    def add_character(self, character):
        """Add a character to the battle map and adjust tile coordinates relative to map"""
        local_x = character.tile_x - self.top_left_tile[0]
        local_y = character.tile_y - self.top_left_tile[1]
        character.battle_x = local_x
        character.battle_y = local_y
        self.characters.append(character)

    def get_blocked_tiles(self):
        """Return a list of blocked tiles within this battle map (local coordinates)"""
        blocked = []
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile and tile.is_blocked:
                    blocked.append((x, y))
        return blocked

    def in_bounds(self, x, y):
        """Check if a local tile coordinate is inside this battle map"""
        return 0 <= x < self.width and 0 <= y < self.height