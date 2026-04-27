"""
character.py - Character classes with inventory

Lab 3 Update: Characters now have inventories using ArrayList!
"""

import pygame
from character import Character
from inventory import Inventory
from item import *
import json
import os
import heapq
from settings import *
import datetime
from datastructures.array import ArrayList
from datastructures.patrol_path import PatrolPath

base_path = os.path.dirname(__file__)
json_path = os.path.join(base_path, 'characters.json')

with open(json_path, 'r') as f:
    CHAR_DATA = json.load(f)
# class Character1(Character):
#     def __init__(self, pos, groups, obstacle_sprites):
#         super().__init__(pos, groups, obstacle_sprites)
#         self.image = pygame.image.load('../graphics/characters/cleric/down/frame_000.png').convert_alpha()
#         self.rect = self.image.get_rect(topleft=pos)
#         self.hitbox = self.rect.inflate(0, -26)
#         self.character_name = "Cleric"
#         self.import_player_assets(animate=True)
    
#     @staticmethod
#     def get_display_name():
#         return "Cleric"
    
#     @staticmethod
#     def get_description():
#         return "First character class"
    
#     @staticmethod
#     def get_preview_image():
#         return '../graphics/characters/cleric/down/frame_000.png'


# class Character2(Character):
#     def __init__(self, pos, groups, obstacle_sprites):
#         super().__init__(pos, groups, obstacle_sprites)
#         self.image = pygame.image.load('../graphics/characters/hobbit/down/frame_000.png').convert_alpha()
#         self.rect = self.image.get_rect(topleft=pos)
#         self.hitbox = self.rect.inflate(0, -26)
#         self.character_name = "Hobbit"
#         self.import_player_assets(animate=True)
    
#     @staticmethod
#     def get_display_name():
#         return "Hobbit"
    
#     @staticmethod
#     def get_description():
#         return "Second character class"
    
#     @staticmethod
#     def get_preview_image():
#         return '../graphics/characters/hobbit/down/frame_000.png'


# class Character3(Character):
#     def __init__(self, pos, groups, obstacle_sprites):
#         super().__init__(pos, groups, obstacle_sprites)
#         self.image = pygame.image.load('../graphics/characters/thief/down/frame_000.png').convert_alpha()
#         self.rect = self.image.get_rect(topleft=pos)
#         self.hitbox = self.rect.inflate(0, -26)
#         self.character_name = "Thief"
#         self.import_player_assets(animate=True)
    
#     @staticmethod
#     def get_display_name():
#         return "Thief"
    
#     @staticmethod
#     def get_description():
#         return "Third character class"
    
#     @staticmethod
#     def get_preview_image():
#         return '../graphics/characters/thief/down/frame_000.png'


# class Character4(Character):
#     def __init__(self, pos, groups, obstacle_sprites):
#         super().__init__(pos, groups, obstacle_sprites)
#         self.image = pygame.image.load('../graphics/characters/wizard/down/frame_000.png').convert_alpha()
#         self.rect = self.image.get_rect(topleft=pos)
#         self.hitbox = self.rect.inflate(0, -26)
#         self.character_name = "Wizard"
#         self.import_player_assets(animate=False)
    
#     @staticmethod
#     def get_display_name():
#         return "Wizard"
    
#     @staticmethod
#     def get_description():
#         return "Fourth character class"
    
#     @staticmethod
#     def get_preview_image():
#         return '../graphics/characters/wizard/down/frame_000.png'
class Player(Character):
    """
    TODO: Implement class
    
    """
    is_playable = True
    def __init__(self, pos, groups, obstacle_sprites,save_slot, is_local=True, player_id=None):
        super().__init__(pos, groups, obstacle_sprites)
        self.is_local = is_local
        self.player_id = player_id
        self.load(save_slot)
        # TODO: Set character image
        if self.sprite:
            try:   
                self.image = pygame.image.load(self.get_preview_image()).convert_alpha()
                    
            except Exception:
                self.image = pygame.Surface((64, 64))
                self.image.fill((255, 0, 255))
        else:
            self.image = pygame.Surface((64, 64))
            self.image.fill((255, 0, 255))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        self.animations = {
            'up': [pygame.image.load('../../graphics/characters/player/dir/north.png').convert_alpha()],
            'down': [pygame.image.load('../../graphics/characters/player/dir/south.png').convert_alpha()],
            'left': [pygame.image.load('../../graphics/characters/player/dir/west.png').convert_alpha()],
            'right': [pygame.image.load('../../graphics/characters/player/dir/east.png').convert_alpha()],
        }
    def special_ability(self):
        """Get special ability"""
        return self.ability        
    def brace(self):
        """Brace special ability: halves incoming damage"""
        self._add_status("Brace")
        self.ap -=2
        print(f"{self.character_name} braced {self.object}self!")
    
    def aim(self):
        """Aim special ability: roll with advantage"""
        self._add_status("Aim")
        self.ap -=2
        print(f"{self.character_name} took aim!")
    def update(self):
        """Update player each frame"""
        if not self.in_battle:
            if self.is_local:
                self.input()
            self.move(self.speed)
            self.get_status()
            self.animate()
    def take_turn(self):
        """Turn based combat turn logic. Called by Battle during battle turns."""
        self.display_available_actions(screen)
    def available_tiles(self):
        """Get list of available tiles to move to based on current AP"""
        tiles = []
        max_distance = self.ap * TILES_PER_AP
        for dx in range(-max_distance, max_distance + 1):
            for dy in range(-max_distance, max_distance + 1):
                if abs(dx) + abs(dy) <= max_distance:
                    tx = self.tile_x + dx
                    ty = self.tile_y + dy
                    if 0 <= tx < self.current_area.width_tiles and 0 <= ty < self.current_area.height_tiles:
                        tiles.append((tx, ty))
        return tiles
    def display_available_tiles(self, screen):
        """Highlight available tiles on the screen during player's turn"""
        if self.in_battle:
            for tx, ty in self.available_tiles():
                rect = pygame.Rect(tx * TILESIZE, ty * TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, (50, 200, 50, 100), rect, 2)
    def select_tile(self, mouse_pos):
        """Select a tile based on mouse position during player's turn"""
        if self.in_battle:
            tx = mouse_pos[0] // TILESIZE
            ty = mouse_pos[1] // TILESIZE
            if (tx, ty) in self.available_tiles():
                return (tx, ty)
        return None
    def move_to_tile(self, tx, ty):
        """Move player from tile to tile during player's turn"""
        if self.in_battle:
            self.tile_x = tx
            self.tile_y = ty
            self.rect.topleft = (tx * TILESIZE, ty * TILESIZE)
    def move_to_target(self, target):
        """Move player towards a target tile, consuming AP accordingly"""
        if self.in_battle:
            path = self.astar((self.tile_x, self.tile_y), (target[0], target[1]), self.get_blocked_tiles(self.current_area), self.current_area.width_tiles, self.current_area.height_tiles)
            movement = 0
            if movement == 0:
                movement = TILES_PER_AP
                self.ap -= 1
            if path and len(path) > 0:       
                for waypoint in path:
                    if movement <= 0:
                        if self.ap <= 0:
                            movement = 3
                            self.ap -= 1
                        else:
                            break
                    self.move_to_tile(waypoint.x, waypoint.y)
                    movement -= 1
    def attack_action(self, target):
        """Attack a target during player's turn"""
        if self.in_battle:
            if self.distance(target) <= self.weapon.range:
                if self.ap >= self.weapon.ap_cost:
                    self.attack(target)
    def available_actions(self):
        """Get list of available actions based on current AP and enemy positions"""
        actions = ["Attack","Move","Item"]
        for ability in self.ability:
            actions.append(ability)
        return actions
    def display_available_actions(self, screen):
        """Display available actions on the screen during player's turn"""
        font = pygame.font.SysFont("consolas", 24)
        actions = self.available_actions()
        for i, action in enumerate(actions):
            action_text = font.render(action, True, (200, 200, 200))
            screen.blit(action_text, (WIDTH - 150, HEIGHT + 20 + i * 40))
    def select_action(self, mouse_pos):
        """Select an action based on mouse position during player's turn"""
        font = pygame.font.SysFont("consolas", 24)
        actions = self.available_actions()
        for i, action in enumerate(actions):
            text_rect = pygame.Rect(WIDTH - 150, HEIGHT + 20 + i * 40, 100, 30)
            if self.action_is_available(action) and text_rect.collidepoint(mouse_pos):
                return action
        return None
    def action_is_available(self, action):
        if action == "Attack":
            return self.ap >= self.weapon.ap_cost
        elif action == "Move":
            return self.ap > 0 and len(self.available_tiles()) > 0
        elif action == "Item":
            return len(self.inventory.items) > 0
        else:
            return action in self.ability and self.ap >= 2
    ### TODO: Uncomment and implement these
    @classmethod
    def get_display_name(cls):
        return cls.character_name

    @classmethod
    def get_description(cls):
        return cls.character_description

    @classmethod
    def get_preview_image(cls):
        return cls.sprite
        
    def get_in_game_image(self):
        """Get in game sprite"""
        return self.game_sprite
    def to_dict(self):
        return {
            "AMMO": dict(self.ammo),
            "ARMOR": ArrayList(self.armor),
            "WEAPONS": ArrayList(self.weapons),
            "CONSUMABLE": dict(self.consumables),
            "KEY": ArrayList(self.keys)
        }

    def save(self, slot=1, filepath="save.json"):
        player_stats = {
            "STR": self.strength,
            "AGL": self.agility,
            "END": self.endurance,
            "INT": self.intelligence,
            "CHR": self.charisma,
            "CURRENT_HP": self.hp,
            "CURRENT_AP": self.ap
        }

        player_equipment = {
            "ARMOR": self.armor.name if self.armor else None,
            "WEAPON": self.weapon.name if self.weapon else None
        }

        position = {
            "AREA": self.current_area,
            "X": self.x,
            "Y": self.y
        }

        game_state = {
            "PLAYER_NAME": self.character_name,
            "PLAYER_DESCRIPTION": self.character_description,
            "PLAYER_SPRITE": self.sprite,
            "PLAYER_GAME_SPRITE": self.game_sprite,
            "DIFFICULTY": self.difficulty,
            "DIFF_MULT": self._diff_mult,
            "PLAYER_LEVEL": self.level,
            "PLAYER_STATS": player_stats,
            "GENDER": self.gender,
            "GENDERED_NOUNS": self.gendered_nouns,
            "AB": self.ab,
            "STATUS": ArrayList(self.status),
            "ALIVE": self.alive,
            "PLAYER_EQUIPMENT": player_equipment,
            "INVENTORY": self.inventory.to_dict(),
            "ABILITY": ArrayList(self.abilities),
            "HAS_PORT_ATMO": self.has_port_atmo,
            "PARTY_NUM": self.party_num,
            "QUESTS": ArrayList(self.quests),
            "POSITION": position
        }

        save_data = {
            "SAVE": {
                str(slot): {
                    "GAME_STATE": game_state,
                    "METADATA": {
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                }
            }
        }

        with open(filepath, "w") as f:
            json.dump(save_data, f, indent=4)

        print(f"Game saved to slot {slot}.")

    def load(self,save):
        with open('state.json','r') as f:
            self.data = json.load(f)
            self.slot = self.data["SAVE"][str(save)]
            self.game_state = self.slot["GAME_STATE"]
            self.difficulty = self.game_state["DIFFICULTY"]
            self._diff_mult = self.game_state["DIFF_MULT"]
            self.gender = self.game_state["GENDER"]
            # core identity
            self.character_name = self.game_state["PLAYER_NAME"]
            self.character_description = self.game_state["PLAYER_DESCRIPTION"]
            self.sprite = self.game_state["PLAYER_SPRITE"]
            self.game_sprite = self.game_state["PLAYER_GAME_SPRITE"]
            self._equipment = self.game_state["PLAYER_EQUIPMENT"]
            self.weapon = Weapon(self._equipment["WEAPON"])
            self.armor = Armor(self._equipment["ARMOR"])
            self._inventory = self.game_state["INVENTORY"]
            for weapon_name in self._inventory.get("WEAPONS", []):
                self.inventory.add_item(Weapon(weapon_name))

            for ammo_type, qty in self._inventory.get("AMMO", {}).items():
                self.inventory.add_item(Item(ammo_type, "AMMO", qty))

            for cons_name, qty in self._inventory.get("CONSUMABLE", {}).items():
                self.inventory.add_item(Item(cons_name, "CONSUMABLE", qty))
            for armor_name in self._inventory.get("ARMOR",[]):
                self.inventory.add_item(Armor(armor_name))
            for key_item in self._inventory.get("KEY",[]):
                self.inventory.add_item(QuestItem(key_item))
            self.ammo = self._inventory.get("AMMO", {})
            self.gendered_nouns = self.game_state["GENDERED_NOUNS"]
            self.object = self.gendered_nouns["object"]
            self.subject = self.gendered_nouns["subject"]
            # stats
            self.level = self.game_state["PLAYER_LEVEL"]
            self.stats = self.game_state["PLAYER_STATS"]
            self.strength = self.stats["STR"]
            self.agility = self.stats["AGL"]
            self.endurance = self.stats["END"]
            self.intelligence = self.stats["INT"]
            self.charisma = self.stats["CHR"]
            self.hp = self.stats["CURRENT_HP"]
            self.ap = self.stats["CURRENT_AP"]
            self.av = self.game_state["AB"]+(self.endurance//2)
            self.ability = self.game_state["ABILITY"]
            self.calc_stats()
            self.status = self.game_state["STATUS"]
            
class NPC(Character):
    is_playable = False
    def __init__(self, pos, groups, obstacle_sprites, character):
        super().__init__(pos, groups, obstacle_sprites)
        data = CHAR_DATA
        npc_root = data["NPCS"][character]
        self.character_name = npc_root["DISPLAY_NAME"]
        self.description = npc_root.get("DESCRIPTION", "")
        self.sprite = npc_root.get("SPRITE", "")  
        self.behavior = npc_root["BEHAVIOR"]
        self.affiliation = npc_root.get("AFFILIATION","")
        self.quests = self.behavior.get("QUESTS","")             
class Enemy(Character):
    """
    TODO: Implement class
    
    """
    is_playable = False

    def __init__(self, pos, groups, obstacle_sprites, character, type, level):
        super().__init__(pos, groups, obstacle_sprites)

        data = CHAR_DATA
        enemy_root = data["ENEMIES"]["TYPE"][type][character]
        level_data = enemy_root["LEVEL"][level]

        # core identity
        self.character_name = level_data["DISPLAY_NAME"]
        self.description = enemy_root.get("DESCRIPTION", "")
        self.sprite = enemy_root.get("SPRITE", "")

        # stats
        self.strength = level_data["STR"]
        self.agility = level_data["AGL"]
        self.endurance = level_data["END"]
        self.intelligence = level_data["INT"]
        self.charisma = level_data["CHR"]
        self.status = []
        self.calc_stats()
        self.hp = self.hp_max
        self.ap = self.ap_max
        self.av = level_data.get("AB", 0) + (self.endurance // 2)
        self._equipment = level_data["EQUIPMENT"]
        self.weapon = Weapon(self._equipment["WEAPON"])
        self.armor = Armor(self._equipment["ARMOR"])
        self.ability = level_data.get("ABILITY", [])
        self._inventory = level_data["INVENTORY"]
        self.inventory = Inventory(self._inventory)
        if self.sprite:
            try:
                self.image = pygame.image.load(self.get_preview_image()).convert_alpha()
                
            except Exception:
                self.image = pygame.Surface((64, 64))
                self.image.fill((255, 0, 255))
        else:
            self.image = pygame.Surface((64, 64))
            self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Turn-based movement state
        self.turn_path = None
        self.turn_target = None

    def special_ability(self):
        """Get special ability"""
        return self.ability
    def get_display_name(self):
        """Get character name"""
        return self.character_name


    def get_description(self):
        """Get description"""
        return self.description


    def get_preview_image(self):
        """Get preview image"""
        return self.sprite
    def get_blocked_tiles(self, level):
        """Return all blocked tile coordinates in the level"""
        blocked = []
        for sprite in level.obstacle_sprites:
            blocked.append((sprite.tile_x, sprite.tile_y))
        # Also block other characters
        for sprite in level.visible_sprites:
            if sprite != self:
                blocked.append((sprite.tile_x, sprite.tile_y))
        return blocked

    def set_turn_path(self, path):
        """Set a tile-by-tile turn path and prepare the first waypoint."""
        self.turn_path = path
        if self.turn_path and len(self.turn_path) > 0:
            self.turn_path.reset()
            self.turn_target = self.turn_path.get_next_waypoint()
        else:
            self.turn_target = None

    def advance_turn_waypoint(self):
        """Move toward the current turn waypoint using direction and move()."""
        if not self.turn_target:
            return False

        target_x = self.turn_target.x * TILESIZE
        target_y = self.turn_target.y * TILESIZE

        while True:
            dx = target_x - self.hitbox.x
            dy = target_y - self.hitbox.y

            # If we are essentially at the target tile, snap to it and finish.
            if abs(dx) <= self.speed and abs(dy) <= self.speed:
                self.move_to_tile(self.turn_target.x, self.turn_target.y)
                break

            self.direction.x = dx
            self.direction.y = dy
            self.move(self.speed)

            # If movement put us exactly on the target, stop.
            if self.hitbox.x == target_x and self.hitbox.y == target_y:
                break

        self.direction.x = 0
        self.direction.y = 0
        self.turn_target = self.turn_path.get_next_waypoint() if self.turn_path else None
        return True

    def has_turn_path(self):
        return self.turn_path is not None and len(self.turn_path) > 0

    def find_path_to_weapon_range(self, level, target):
        """
        Finds a path to the closest tile within weapon range of the target.
        Returns a PatrolPath containing one tile waypoint per step.
        """
        weapon_range = self.weapon.range
        blocked_tiles = self.get_blocked_tiles(level)
        start_tile = (self.tile_x, self.tile_y)

        # Generate candidate goal tiles within weapon range
        goal_tiles = []
        for dx in range(-weapon_range, weapon_range + 1):
            for dy in range(-weapon_range, weapon_range + 1):
                if max(abs(dx), abs(dy)) <= weapon_range:  # Chebyshev distance
                    tx = target.tile_x + dx
                    ty = target.tile_y + dy
                    # Check bounds
                    if 0 <= tx < level.width_tiles and 0 <= ty < level.height_tiles:
                        if (tx, ty) not in blocked_tiles:
                            goal_tiles.append((tx, ty))

        if not goal_tiles:
            return []  # No reachable tiles

        # Choose closest goal tile to self
        goal_tile = min(goal_tiles, key=lambda t: max(abs(t[0]-start_tile[0]), abs(t[1]-start_tile[1])))

        # Compute path
        path = self.astar(start_tile, goal_tile, blocked_tiles,level.width_tiles, level.height_tiles)
        return path
    def find_enemy(self, enemies):
        closest = enemies[0]
        for enemy in enemies:
            if self.distance(enemy) < self.distance(closest):
                closest = enemy
        enemy_in_range = self.distance(closest) <= self.weapon.range
        return closest,enemy_in_range
    


class Ranged(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, character, type, level):
        super().__init__(pos, groups, obstacle_sprites, character, type, level)
        self.is_ranged = True
        # TODO LATER: Implement enemy ai based on type (Ranged or Melee)
        ###########################################################
        #                       AI mockup                         #
        ###########################################################
        # if enemy turn
            # if hp > 30 percent
                # if healing items in inventory
                    # heal
            # if player is within 3 meters
                # if enemy is ranged
                    # move in opposite direction
                    # if within weapon range
                        # use points to fire weapon at player
                    # else
                        # try to move into range and use rest of points to fire weapon
                # else if enemy is melee
                    # if within weapon range
                        # use points to attack with weapon
                    #else
                        # try to move into range and use rest of points to attack
        # else
            # wait for turn
    def aim(self):
        """Aim special ability: roll with advantage"""
        self._add_status("Aim")
        self.ap -= 2
        print(f"{self.character_name} took aim!")
    def take_turn(self, enemies, level):
        """AI turn logic. Works on any level dynamically."""
        count = 0
        while self.ap > 0:
            # --- 1. Use healing items if low HP ---
            for item in self.inventory.items:
                if self.hp / self.hp_max < 0.3 and getattr(item, "effect_type", None) == "heal":
                    if self.ap >= getattr(item, "ap_cost", 0):
                        item.use()
                        break  # Only use one item per turn

            # --- 2. Find nearest enemy ---
            target, enemy_in_range = self.find_enemy(enemies)
            if target is None:
                return  # No enemies left

            # --- 3. Check if enemy is in weapon range ---
            if enemy_in_range:
                while self.ap >= self.weapon.ap_cost:
                    self.attack(target)
                return  # End turn after attack

            # --- 4. Move towards a tile within weapon range ---
            path = self.find_path_to_weapon_range(level, target)

            if path and len(path) > 0:
                self.set_turn_path(path)
                tiles_remaining = 0
                while self.ap > 0 and self.turn_target:
                    if tiles_remaining <= 0:
                        self.ap -= 1
                        if self.ap < 0:
                            break
                        tiles_remaining = TILES_PER_AP

                    self.advance_turn_waypoint()
                    tiles_remaining -= 1

                # Recheck if target is in range after moving
                _, enemy_in_range = self.find_enemy(enemies)
                while self.ap >= self.weapon.ap_cost:
                    if enemy_in_range:
                        self.attack(target)
                    else:
                        break
                return
            else:
                # No path to a reachable tile — skip turn
                return
    def battle_turn(self, battle):
        self.take_turn(battle.enemies, battle.level)

                


class Melee(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, character, type, level):
        super().__init__(pos, groups, obstacle_sprites, character, type, level)
        self.is_ranged = False
    def brace(self):
        """Brace special ability: halve incoming damage"""
        self._add_status("Brace")
        self.ap -= 2
        print(f"{self.character_name} braced themself!")
    def take_turn(self, enemies, level):
        """AI turn logic. Works on any level dynamically."""
        count = 0
        while self.ap > 0:
            # --- 1. Use healing items if low HP ---
            for item in self.inventory.items:
                if self.hp / self.hp_max < 0.3 and getattr(item, "effect_type", None) == "heal":
                    if self.ap >= getattr(item, "ap_cost", 0):
                        item.use()
                        break  # Only use one item per turn

            # --- 2. Find nearest enemy ---
            target, enemy_in_range = self.find_enemy(enemies)
            if target is None:
                return  # No enemies left

            # --- 3. Check if enemy is in weapon range ---
            if enemy_in_range:
                if self.ap >= self.weapon.ap_cost:
                    self.attack(target)
                return  # End turn after attack

            # --- 4. Move towards a tile within weapon range ---
            path = self.find_path_to_weapon_range(level, target)

            if path and len(path) > 0:
                self.set_turn_path(path)
                tiles_remaining = 0
                while self.ap > 0 and self.turn_target:
                    if tiles_remaining <= 0:
                        self.ap -= 1
                        if self.ap < 0:
                            break
                        tiles_remaining = TILES_PER_AP

                    self.advance_turn_waypoint()
                    tiles_remaining -= 1

                # Recheck if target is in range after moving
                _, enemy_in_range = self.find_enemy(enemies)
                if self.ap >= self.weapon.ap_cost and enemy_in_range:
                    self.attack(target)
                return
            else:
                # No path to a reachable tile — skip turn
                return


def get_all_character_classes():
    """Auto-discover all character classes"""
    character_classes = []
    for cls in Character.__subclasses__():
        if cls.__name__ != 'Character':
            if getattr(cls, 'is_playable', False):
                character_classes.append(cls)
    return character_classes