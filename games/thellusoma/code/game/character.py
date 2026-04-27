"""
character.py - Character classes with inventory

Lab 3 Update: Characters now have inventories using ArrayList!
"""

import pygame
from settings import *
from support import import_folder
import random
from inventory import Inventory
from datastructures.patrol_path import PatrolPath
from datastructures.waypoint import Waypoint
import json
import heapq
from item import *
class Character(pygame.sprite.Sprite):
    """Base Character class with inventory"""
    
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        
        # self.image = pygame.Surface((64, 64))
        # self.image.fill((255, 0, 255))
        # self.rect = self.image.get_rect(topleft=pos)
        # self.hitbox = self.rect.inflate(0, -26)
        
        # # Stats
        # self.character_name = "Unknown"
        # self.hp, self.max_hp = 100, 100
        # self.attack, self.defense, self.speed = 10, 5, 5
        
        # # graphics setup
        # self.status = 'down'
        # self.frame_index = 0
        # self.animation_speed = 0.15

        # # Movement
        # self.direction = pygame.math.Vector2()
        # self.speed = 5
        # self.attacking = False
        # self.attack_cooldown = 400
        # self.attack_time = None
        # self.obstacle_sprites = obstacle_sprites
        
        # # NEW: Inventory using ArrayList!
        # self.inventory = Inventory(max_size=20)
        # Stats (override in subclasses)
        self.character_name = "Unknown"
        self._diff_mult = 1
        self.hp = 1
        self.hp_max = self.hp
        self.max_hp = self.hp_max  # backward compat for legacy callers
        self.strength = 1
        self.agility = 1
        self.endurance = 1
        self.intelligence = 1
        self.charisma = 1
        self.level = 1
        self.ap = 1
        self.ap_max = 1
        self.ms = 1
        self.av = 1
        self.speed = 5
        self.status = []
        self.alive = True
        self.image = pygame.Surface((64, 64))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.inventory = Inventory(max_size=20)
        self.attacking = False
        self.moving = False
        self.gamestatus = 'down'
        self.animations = {
            'up': [pygame.image.load('../../graphics/characters/player/dir/north.png').convert_alpha()],
            'down': [pygame.image.load('../../graphics/characters/player/dir/south.png').convert_alpha()],
            'left': [pygame.image.load('../../graphics/characters/player/dir/west.png').convert_alpha()],
            'right': [pygame.image.load('../../graphics/characters/player/dir/east.png').convert_alpha()],
        }
        self.frame_index = 0
        self.animation_speed = 0.15
        # Movement
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.in_battle = False
    @property
    def tile_x(self):
        return self.hitbox.x // TILESIZE
    @property
    def tile_y(self):
        return self.hitbox.y // TILESIZE
    def move_to_tile(self, tile_x, tile_y):
        self.hitbox.x = tile_x * TILESIZE
        self.hitbox.y = tile_y * TILESIZE
        self.rect.center = self.hitbox.center
    def astar(self, start, goal, blocked_tiles, grid_width, grid_height):
        """A* pathfinding from start to goal avoiding blocked_tiles"""
        import heapq
        path = PatrolPath("one_way")
        def heuristic(a, b):
            # Chebyshev distance for 8-directional movement
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

        # Directions: 8-way movement
        neighbors = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        closed_set = set()

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                # Reconstruct path into a PatrolPath
                reversed_path = []
                while current in came_from:
                    reversed_path.append(current)
                    current = came_from[current]
                reversed_path.reverse()

                for coord in reversed_path:
                    path.add_waypoint(coord[0], coord[1])
                return path

            closed_set.add(current)

            for dx, dy in neighbors:
                neighbor = (current[0] + dx, current[1] + dy)

                # Check bounds
                if not (0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height):
                    continue
                # Skip blocked tiles
                if neighbor in blocked_tiles:
                    continue
                # Skip already evaluated
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, neighbor))

        return path
    def input(self):
        """Handle player input"""
        if not self.attacking:
            keys = pygame.key.get_pressed()

			# movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.gamestatus = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.gamestatus = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.gamestatus = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.gamestatus = 'left'
            else:
                self.direction.x = 0

			# attack input 
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                #print('attack')

			# magic input 
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                #print('magic')

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and not self.attacking:
            if not self.gamestatus.endswith('_idle'):
                self.gamestatus = self.gamestatus.split('_')[0] + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not self.gamestatus.endswith('_attack'):
                self.gamestatus = self.gamestatus.split('_')[0] + '_attack'
        elif self.gamestatus.endswith('_attack') and not self.attacking:
            self.gamestatus = self.gamestatus.replace('_attack','')
    
    def move(self, speed):
        """Move the character"""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):
        """Handle collision with obstacles"""
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # Check if sprite has hitbox attribute
                sprite_box = sprite.hitbox if hasattr(sprite, 'hitbox') else sprite.rect
                if sprite_box.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite_box.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite_box.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                sprite_box = sprite.hitbox if hasattr(sprite, 'hitbox') else sprite.rect
                if sprite_box.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite_box.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite_box.bottom
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.gamestatus.replace("_idle", "").replace("_attack", "")]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
    def update(self):
        """Update character each frame"""
        if not self.in_battle:
            self.input()
            self.move(self.speed)
            self.get_status()
            self.animate()
    def battle_turn(self, battle):
        pass
    def special_ability(self):
        """Special ability - override in subclasses"""
        pass
    def distance(self,enemy):
        #chebyshev distance
        enemy_distance = max(abs(self.tile_x-enemy.tile_x),abs(self.tile_y-enemy.tile_y))
        return enemy_distance
    def calc_stats(self):
        """Handle calculated stats"""
        self.hp_max = 100 + (30*self.endurance)
        self.max_hp = self.hp_max  # keep both names in sync
        self.ap_max = 5 + (self.agility//2)
        self.ms = self.agility/2
        self.ab = self.armor.ab+self.agility/2
    def _add_status(self, effect):
        """Add a status effect. Protected since it is only used by characters"""
        self.status.append(effect)
    def _remove_status(self, effect):
        """Removes a status effect. Protected for the same reason"""
        self.status.remove(effect)
    def take_damage(self, damage):
        """Method that reduces target hp when it takes damage"""
        hp = self.hp-damage
        if hp <= 0:
            self.hp = 0
            self.alive=False
        else:
            self.hp = hp
        return self.hp
    def heal(self,value):
        """Method that heals the target's hp"""
        if (self.hp+value)<=self.hp_max:
            self.hp=self.hp+value
        else:
            self.hp = self.hp_max
        return self.hp
    def is_alive(self):
        """Method to check if the target is alive"""
        if self.hp > 0:
            self.alive=True
        else:
            self.alive=False
        return self.alive
    def __attack_roll(self):
        roll = random.randint(1, 20)
        return roll
    def attack(self, target, weapon=None):
        """Method to handle attacking in basic combat"""
        if weapon is None:
            weapon = Weapon(self.inventory.weapon,1)
            # check what kind of data the ammo requirement of the weapon is
            if not self.weapon.ammo:
                ammo_req=[]
            elif isinstance(self.weapon.ammo,dict):
                ammo_req = [self.weapon.ammo]
            elif isinstance(self.weapon.ammo, list):
                ammo_req = self.weapon.ammo
            # check if user has enough ammo in their inventory
            for req in ammo_req:
                for ammo_type, ammo_cost in req.items():
                    if ammo_type not in self.inventory:
                        print(f"Not enough {ammo_type}!")
                        return 0
                    if self.inventory.ammo < ammo_cost:
                        print(f"Not enough {ammo_type}!")
                        return 0
        else:
            die = weapon.dice_val
            dice_num = weapon.dice_num
            bonus = weapon.bonus_mult
            cost = weapon.ap_cost
            display = weapon.display_name
            ammo_req = None   
        # roll however many dice that are specified in items.json and the type of die in the file     
        base_damage = sum(random.randint(1, die) for _ in range(dice_num))
        max_base_damage = dice_num*die
        if weapon.weapon_type == "RANGED":
            bonus_stat = self.agility
        elif weapon.weapon_type == "MELEE":
            bonus_stat = self.strength
        else:
            bonus_stat = 0        
        bonus_damage = bonus_stat * bonus
        attackroll = self.__attack_roll()
        if "Aim" in self.status:
            # essentially rolling with advantage (taking the max of two rolls) when using Aim
            attackroll = max(attackroll,self.__attack_roll())
        damage = 0
        # remove ammo required from inventory
        if self.ap >= cost:
            if ammo_req:
                for req in ammo_req:
                    for ammo_type, ammo_cost in req.items():
                        self.inventory.ammo -= ammo_cost
            if attackroll == 20:
                damage = (max_base_damage+bonus_damage)*target._diff_mult
                if "Brace" in target.status:
                    damage = damage/2
                target.take_damage(damage)
                print(f"[ROLL: {attackroll}] A critical hit! {self.character_name} hit {target.character_name} with  {display} for {damage} hp!")
                self.ap = max(self.ap - cost,0)
                return damage
            elif attackroll > target.av:
                damage = (base_damage+bonus_damage)*target._diff_mult
                if "Brace" in target.status:
                    damage = damage/2
                target.take_damage(damage)
                print(f"[ROLL: {attackroll}] {self.character_name} hit {target.character_name} with {display} for {damage} hp!")
                self.ap = max(self.ap - cost,0)
                return damage
            elif attackroll == 1:
                self.ap = max(self.ap - 2,0)
                print(f"[ROLL: {attackroll}] A critical failure! {self.character_name} lost 2 AP!")
                damage = 0
                self.ap = max(self.ap - cost,0)
                return damage
            else:
                print(f"[ROLL: {attackroll}] {self.character_name} tried to attack {target.character_name} but missed!")
                damage = 0
                self.ap = max(self.ap - cost,0)
                return damage
                
        else:
            print(f"{self.character_name} doesn't have enough AP to attack!")

        return damage
    def throw(self, item, target):
        """Method to handle throwing items in basic combat"""
        attackroll = self.__attack_roll()
        if "Aim" in self.status:
            # essentially rolling with advantage (taking the max of two rolls) when using Aim
            attackroll = max(attackroll,self.__attack_roll())
        damage = 0
        if item.type == "weapon":
            if self.ap >= item.apcost:
                if attackroll == 20:
                    damage = (item.max_base_damage+item.bonus_damage)*target._diff_mult
                    if "Brace" in target.status:
                        damage = damage/2
                    target.take_damage(damage)
                    print(f"[ROLL: {attackroll}] A critical hit! {self.character_name} hit {target.character_name} with  {item.display_name} for {damage} hp!")
                    self.ap = self.ap - item.apcost
                    
                elif attackroll > target.av:
                    damage = (item.base_damage+item.bonus_damage)*target._diff_mult
                    if "Brace" in target.status:
                        damage = damage/2
                    target.take_damage(damage)
                    print(f"[ROLL: {attackroll}] {self.character_name} hit {target.character_name} with {item.display_name} for {damage} hp!")
                    self.ap = self.ap - item.apcost
                    
                elif attackroll == 1:
                    self.ap = max(self.ap - 2,0)
                    print(f"[ROLL: {attackroll}] A critical failure! {self.character_name} lost 2 AP!")
                    damage = 0
                    self.ap = self.ap - item.apcost
                    
                else:
                    print(f"[ROLL: {attackroll}] {self.character_name} tried to attack {target.character_name} but missed!")
                    damage = 0
                    self.ap = self.ap - item.apcost
            else:
                print(f"{self.character_name} doesn't have enough AP to throw {item.display_name}!")
                return 0
                    
        if item.effect and attackroll > target.av:
            if self.ap >= item.apcost:
                self.ap -= item.apcost
                target._add_status(item.effect)
                print(f"{self.character_name} used {item.display_name} on {target.character_name}!")    
            else:
                print(f"{self.character_name} doesn't have enough AP to use {item.display_name}!")
                    
        elif item.type == "buff":
            if self.ap >= item.apcost:
                target._add_status(item.effect)
                self.ap -= item.apcost
                print(f"{self.character_name} used {item.display_name} on {target.character_name}!")
            else:
                print(f"{self.character_name} doesn't have enough AP to use {item.display_name}!")
        elif item.type == "heal":
            if self.ap >= item.apcost:
                self.ap -= item.apcost
                target.heal(item.effect_amount)
                print(f"{self.character_name} healed {target.character_name} for {item.effect_amount} hp!")
            else:
                print(f"{self.character_name} doesn't have enough AP to use {item.display_name}!")
        else:
           print(f"{item.display_name} is not a throwable item!")

    def import_player_assets(self, animate=True,scale=(128,128)):
        
        character_path = '../../graphics/characters/' + self.character_name.lower() + "/"
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            
            }

        for animation in self.animations.keys():
            full_path = character_path + animation
            if animate:
                self.animations[animation] = import_folder(full_path)
            else: 
                path = '../../graphics/characters/' + self.character_name.lower() + '.png'
                self.animations[animation] = [pygame.image.load(path).convert_alpha()]
        print("self.animations[animation]",  self.animations)




    def special_ability(self):
        """Special ability - override in subclasses"""
        pass
    

    def get_display_name(self):
        return "Unknown"
    

    def get_description(self):
        return "A mysterious character"
    

    def get_preview_image(self):
        return '../graphics/test/player.png'
