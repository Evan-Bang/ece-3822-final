"""
subcharacter.py - Character classes

Different character types that players can choose from
"""

import pygame
from character import Character

class Chharacter1(Character):
    """Cleric - Healing specialist"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Cleric"
        self.hp, self.max_hp = 120, 120
        self.attack, self.defense = 8, 7
        
        # Load image for remote players or as fallback
        try:
            self.image = pygame.image.load('../../graphics/characters/cleric/down/frame_000.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass
            
        # Load animations for local player
        if is_local:
            self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        return "Cleric"
    
    @staticmethod
    def get_description():
        return "Healing specialist with high HP"
    
    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/cleric/down/frame_000.png'


class Chharacter2(Character):
    """Hobbit - Sneaky and fast"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Hobbit"
        self.hp, self.max_hp = 80, 80
        self.attack, self.defense = 12, 4
        self.speed = 6  # Faster than others
        
        try:
            self.image = pygame.image.load('../../graphics/characters/hobbit/down/frame_000.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass
            
        if is_local:
            self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        return "Hobbit"
    
    @staticmethod
    def get_description():
        return "Fast and sneaky"
    
    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/hobbit/down/frame_000.png'


class Chharacter3(Character):
    """Thief - High attack, low defense"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Thief"
        self.hp, self.max_hp = 90, 90
        self.attack, self.defense = 15, 3
        
        try:
            self.image = pygame.image.load('../../graphics/characters/thief/down/frame_000.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass
            
        if is_local:
            self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        return "Thief"
    
    @staticmethod
    def get_description():
        return "Glass cannon - high attack"
    
    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/thief/down/frame_000.png'


class Chharacter4(Character):
    """Wizard - Magical powerhouse"""
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Wizard"
        self.hp, self.max_hp = 100, 100
        self.attack, self.defense = 10, 5
        
        try:
            self.image = pygame.image.load('../../graphics/characters/wizard/down/frame_000.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass
            
        if is_local:
            self.import_player_assets(animate=True)
    
    @staticmethod
    def get_display_name():
        return "Wizard"
    
    @staticmethod
    def get_description():
        return "Balanced mage with special abilities"
    
    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/wizard/down/frame_000.png'

class CharacterAdventurer(Character):
    """
    Starter class
    """
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Adventurer"
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.speed = 10

        try:
            self.image = pygame.image.load('../../graphics/characters/adventurer.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        if is_local:
            self.import_player_assets(animate=False)


    def special_ability(self):
        """
        Rest: Slowly heals
        """
        self.heal(5)
    
    @staticmethod
    def get_display_name():
        return "Adventurer"
    
    @staticmethod
    def get_description():
        return "Base starting class. Has no special ability."
    
    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/adventurer.png'

class CharacterSquire(Character):
    """
    Evolution of Adventurer
    """
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Squire"
        self.hp = 120
        self.max_hp = 120
        self.attack = 12
        self.defense = 6
        self.speed = 11

        try:
            self.image = pygame.image.load('../../graphics/characters/squire.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        if is_local:
            self.import_player_assets(animate=False)

    def special_ability(self):
        """
        Zoomies: small speed boost
        """
        self.speed += 2
    
    @staticmethod
    def get_display_name():
        return "Squire"
    
    @staticmethod
    def get_description():
        return "An experienced adventurer on its way to nobility"
    
    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/squire.png'
    
class CharacterKnight(Character):
    """
    Evolution of Squire
    """
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Knight"
        self.hp = 140
        self.max_hp = 140
        self.attack = 15
        self.defense = 7
        self.speed = 12

        try:
            self.image = pygame.image.load('../../graphics/characters/knight.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        if is_local:
            self.import_player_assets(animate=False)

    def special_ability(self):
        """
        Sniffer: small defense boost
        """
        self.defense += 5
    
    @staticmethod
    def get_display_name():
        return "Knight"
    
    @staticmethod
    def get_description():
        return "An experienced Squire that's earned its spot among nobles"
    
    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/knight.png'

class CharacterPrincess(Character):
    """
    Evolution of Knight
    """
    def __init__(self, pos, groups, obstacle_sprites, player_id=None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, player_id, is_local)
        self.character_name = "Princess"
        self.hp = 160
        self.max_hp = 160
        self.attack = 17
        self.defense = 8
        self.speed = 13

        try:
            self.image = pygame.image.load('../../graphics/characters/princess.png').convert_alpha()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -26)
        except:
            pass

        if is_local:
            self.import_player_assets(animate=False)

    def special_ability(self):
        """
        Bark: Powerful attack buff
        """
        self.attack += 10
    
    @staticmethod
    def get_display_name():
        return "Princess"
    
    @staticmethod
    def get_description():
        return "A former Knight that has become a candidate for royalty"
    
    @staticmethod
    def get_preview_image():
        return '../../graphics/characters/princess.png'

def get_all_character_classes():
    """Auto-discover all character classes"""
    character_classes = []
    for cls in Character.__subclasses__():
        if cls.__name__ != 'Character' and cls.__name__.startswith('Character'):
            character_classes.append(cls)
    return character_classes
