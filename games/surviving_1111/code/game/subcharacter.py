"""
character.py - Character classes with inventory

Lab 3 Update: Characters now have inventories using ArrayList!
"""

import pygame
import random
from character import Character

class Vibe_Coder(Character):
    """
    Vibe Coder character class
    """
    def __init__(self, pos = (0, 0), groups = None, obstacle_sprites = None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, is_local)
        
        # Set character image
        self.image = pygame.image.load('../../graphics/characters/vibe_coder_64x64.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # Set stats
        self.character_name = "Vibe Coder"
        self._max_hp = 75
        self.hp = 75
        self._attack = 10
        self._defense = 3
        self._speed = 8
       

    
    def special_ability(self):
        """Boost damage greatly but has a chance to backfire"""
        boost_chance = random.random()
        if boost_chance < 0.5:
            # two second buff to attack
            self.apply_buff(stat_name='attack', amount=15, duration_in_frames=120)
        else:
            self.take_damage(10)
        return True
      
    
    @staticmethod
    def get_display_name():
        """Return character name"""
        return "Vibe Coder"
    
    @staticmethod
    def get_description():
        """Return character description"""
        return "While weaker in stats, the Vibe Coder can call upon AI to boost their stats in battle"
    
    @staticmethod
    def get_preview_image():
        """Return path to character preview image"""
        return '../../graphics/characters/vibe_coder.png'


class Debugger(Character):
    """
    Debugger character class
    """
    def __init__(self, pos = (0, 0), groups = None, obstacle_sprites = None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, is_local)
        
        # Set character image
        self.image = pygame.image.load('../../graphics/characters/debugger_64x64.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # Set stats
        self.character_name = "Debugger"
        self._max_hp = 90
        self.hp = 90
        self._attack = 5
        self._defense = 5
        self._speed = 5

    def special_ability(self):
        """Restore a significant amount of health"""
        self.heal(40)
        return True
    
    @staticmethod
    def get_display_name():
        """Return character name"""
        return "Debugger"
    
    # @staticmethod
    def get_description():
        """Return character description"""
        return "The Debugger can find and fix bugs in their code, restoring health"
    @staticmethod
    def get_description():
        """Return character description"""
        return "The Debugger can find and fix bugs in their code, restoring health"
    @staticmethod
    def get_preview_image():
        """Return path to character preview image"""
        return '../../graphics/characters/debugger.png'
    

class IO_Specialist(Character):
    """
    Implement I/O Specialist class
    """
    def __init__(self, pos = (0, 0), groups = None, obstacle_sprites = None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, is_local)
        
        # Set character image
        self.image = pygame.image.load('../../graphics/characters/IO_specialist_64x64.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # Set stats
        self.character_name = "I/O Specialist"
        self.hp = 90 
        self._max_hp = 90
        self._attack = 6
        self._defense = 5
        self._speed = 5
        self.saved_hp = None
        self.state_saved = False
    
    def special_ability(self):
        """Saves state to be restored later"""
        if self.state_saved == False:
            # Don't use buffed HP since that could be abused
            self.saved_hp = self.hp
            self.state_saved = True
        else:
            self.hp = self.saved_hp
            self.state_saved = False
        return True
    
    @staticmethod
    def get_display_name():
        """Return character name"""
        return "I/O Specialist"
    
    @staticmethod
    def get_description():
        """Return character description"""
        return "The I/O Specialist can save their state and restore it later in battle"
    
    @staticmethod
    def get_preview_image():
        """Return path to character preview image"""
        return '../../graphics/characters/io_specialist.png'
    
class C_Specialist(Character):
    """
    Implement C Specialist class

    """
    def __init__(self, pos = (0, 0), groups = None, obstacle_sprites = None, is_local=True):
        super().__init__(pos, groups, obstacle_sprites, is_local)
        
        # Set character image
        self.image = pygame.image.load('../../graphics/characters/C_specialist_64x64.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # Set stats
        self.character_name = "C Specialist"
        self._max_hp = 50
        self.hp = 50
        self._attack = 17
        self._defense = 3
        self._speed = 8
    

    def special_ability(self):
        """Ability: compile, boosts speed and attack temporarily but takes time to compile"""
        self.apply_buff(stat_name='speed', amount=-100, duration_in_frames=30) # stun for 30 frames
        self.apply_buff(stat_name='speed', amount=5, duration_in_frames=120)
        self.apply_buff(stat_name='attack', amount=5, duration_in_frames=120)
        
    
    @staticmethod
    def get_display_name():
        """Return character name"""
        return "C Specialist"
    
    @staticmethod
    def get_description():
        """Return character description"""
        return "High attack and speed, but low health. The C Specialist can compile code to boost stats temporarily"
    
    @staticmethod
    def get_preview_image():
        """Return path to character preview image"""
        return '../../graphics/characters/c_specialist.png'


# ============================================
# CHARACTER REGISTRY (Auto-discovery)
# ============================================

def get_all_character_classes():
    """
    Automatically discover all character classes
    Returns list of character classes (not instances)
    """
    # Get all subclasses of Character
    character_classes = []
    
    for cls in Character.__subclasses__():
        # Skip the base Character class
        if cls.__name__ != 'Character':
            character_classes.append(cls)
    
    return character_classes