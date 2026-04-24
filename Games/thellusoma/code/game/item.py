"""
item.py - Item class for inventory system

Defines items that can be collected and stored in inventory.
Create your own items based on Lab 1 designs.

Author: [Student Name]
Date: [Date]
Lab: Lab 3 - Inventory System
"""

import json
import pygame
with open("items.json", "r") as f:
    ITEMS_DATA = json.load(f)
class Item:
    """
    Base class for all items in the game.
    
    Items can be weapons, consumables, armor, etc.
    """
    
    def __init__(self, item_name, item_type, quantity):
        """
        Initialize an item.
        
        Args:
            name (str): Item name
            item_type (str): Type (weapon, consumable, armor, quest, etc.)
            description (str): Item description
            image_path (str): Path to item image
            value (int): Item value/price
            stackable (bool): Can multiple be in one slot?
            max_stack (int): Maximum stack size
        """

        self.item_data = ITEMS_DATA["TYPE"][item_type][item_name]
        self.description = self.item_data["DESCRIPTION"]
        self.image_path = self.item_data["SPRITE"]
        self.value = self.item_data["VALUE"]
        self.name = item_name
        self.item_type = item_type
        self.stackable = False
        self.quantity = quantity

        

        try:
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
        except:

            self.image = pygame.Surface((64, 64))
            self.image.fill((150, 150, 150))
            font = pygame.font.Font(None, 20)
            text = font.render(item_type[:3].upper(), True, (0, 0, 0))
            text_rect = text.get_rect(center=(32, 32))
            self.image.blit(text, text_rect)
    
    def __str__(self):
        """String representation of item"""
        if self.stackable and self.quantity > 1:
            return f"{self.name} x{self.quantity}"
        return self.name
    
    def __repr__(self):
        """Official representation"""
        return f"Item(name='{self.name}', type='{self.item_type}', qty={self.quantity})"
    
    def use(self, character):
        """
        Use/equip the item on a character.
        Override in subclasses for specific behavior.
        
        Args:
            character: Character using the item
            
        Returns:
            bool: True if item was consumed, False otherwise
        """
        print(f"Used {self.name}")
        return False
    
    def can_stack_with(self, other):
        """
        Check if this item can stack with another.
        
        Args:
            other (Item): Other item
            
        Returns:
            bool: True if can stack
        """
        return (self.stackable and 
                isinstance(other, Item) and
                self.name == other.name and
                self.item_type == other.item_type and
                self.quantity < self.max_stack)

        


class Weapon(Item):
    """Weapon items that increase attack power"""
    
    def __init__(self, item_name, quantity=1):
        super().__init__(item_name, "WEAPON", quantity)
        self.stackable = False
        self.dice_num = self.item_data["DICE_NUM"]
        self.dice_val = self.item_data["DICE_VAL"]
        self.bonus_mult = self.item_data["BONUS_MULT"]
        self.weapon_type = self.item_data["TYPE"]
        self.ap_cost = self.item_data["AP_COST"]
        self.range_min = self.item_data["RANGE_MIN"]
        self.range_max = self.item_data["RANGE_MAX"]
        self.dam_type = self.item_data["DAM_TYPE"]
        self.dam_equation = self.item_data["DAM_EQUATION"]
        self.req_str = self.item_data.get("REQ_STR", 0)
        self.req_dex = self.item_data.get("REQ_AGL", 0)
        self.req_int = self.item_data.get("REQ_INT", 0)
        self.req_chr = self.item_data.get("REQ_CHR", 0)
        self.ammo= self.item_data.get("AMMO", None)
    
    def use(self, character):
        """Equip the weapon"""
        print(f"{character.character_name} equipped {self.name}")
        character._equipment["weapon"] = self
        return False
    @property
    def range(self):
        return self.range_max


class Armor(Item):
    """Armor items that increase defense"""
    
    def __init__(self, item_name, quantity=1):
        super().__init__(item_name, "ARMOR", quantity)
        self.stackable = False
        self.armor_type = self.item_data["TYPE"]
        self.ab= self.item_data["AB"]
        self.bonus_str = self.item_data.get("BONUS_STR", 0)
        self.bonus_dex = self.item_data.get("BONUS_AGL", 0)
        self.bonus_int = self.item_data.get("BONUS_INT", 0)
        self.bonus_chr = self.item_data.get("BONUS_CHR", 0)
        self.bonus_end = self.item_data.get("BONUS_END", 0)
        
    
    def use(self, character):
        """Equip the armor"""
        print(f"{character.character_name} equipped {self.name} (+{self.ab} defense)")
        character._equipment["armor"] = self
        return False  # Armor is not consumed


class Consumable(Item):
    """Consumable items like potions"""
    
    def __init__(self, item_name, quantity):
        super().__init__(item_name, "CONSUMABLE", quantity)
        self.item_name = item_name
        self.stackable = True
        self.effect_type = self.item_data["EFFECT_TYPE"]
        self.max_stack = self.item_data["MAX_STACK"]
        self.quantity = quantity
        if self.effect_type == "buff":
            self.effect_status = self.item_data["EFFECT_STATUS"]
            self.effect_time = self.item_data["EFFECT_TIME"]
            self.effect_amount = self.item_data["EFFECT_AMOUNT"]
        elif self.effect_type == "heal":
            self.effect_amount = self.item_data["EFFECT_AMOUNT"]
        elif self.effect_type == "weapon":
            self.dice_num = self.item_data["DICE_NUM"]
            self.dice_val = self.item_data["DICE_VAL"]
            self.bonus_mult = self.item_data["BONUS_MULT"]
            self.dam_equation = self.item_data["DAM_EQUATION"]

            

    def use(self, character):
        """Use the consumable"""
        if self.effect_type == "heal":
            character.heal(self.effect_amount)
            print(f"{character.character_name} used {self.name} and healed {self.effect_amount} HP")
        elif self.effect_type == "buff":
            character._add_status(self.effect_status)
            print(f"{character.character_name} gained buff {self.effect_status} for {self.effect_time} turns")
        elif self.effect_type == "weapon":
            character.throw(self,character)
            if self.subject != "":
                print(f"{character.character_name} used {self.name} on... {character.object}self?!")
            else:
                print(f"{character.character_name} used {self.name} on... themself?")
        return True  # Consumables are used up
    def throw(self, character, target):
        """Throw the item"""
        if self.effect_type == "weapon":
            character.throw(self, target)
            print(f"{character.character_name} threw {self.name} at {target}!")
        else:
            print(f"You can't throw a {self.name} as a weapon!")
class Ammo(Item):
    def __init__(self, item_name, quantity):
        super().__init__(item_name, "AMMO", quantity)
        self.item_name = item_name
        self.quantity = quantity
    def use(self,character):
        """Ammo cant be used directly"""
        print(f"{self.name} is a type of ammo")
        return False
class QuestItem(Item):
    """Special quest-related items"""
    
    def __init__(self, item_name, quantity=1):
        super().__init__(item_name, "KEY", quantity)
        self.quest_id = None
    
    def use(self,character):
        """Quest items usually can't be used directly"""
        print(f"{self.name} is a quest item")
        return False


# =============
# EXAMPLE ITEMS
# =============

def create_example_items():
    """
    Create example items for testing.
    Create your own items based on Lab 1 designs.
    """
    items = []
    items.append(Weapon("OLD_WORLD_PISTOL",1))
    items.append(Weapon("RAILGUN",1))
    items.append(Weapon("PARTICLE-BEAM",1))
    items.append(Armor("SUPERCOOLED_ARMOR",1))
    items.append(Consumable("DISTILLED_WATER",1))
    items.append(Consumable("CYBERDYNAMICS_BEER",1))
    items.append(Ammo("9mm", 50))
    items.append(Ammo("Battery", 10))
    items.append(Ammo("Darts", 20))
    items.append(Ammo("Hydrogen", 5))
    for item in items:
        print(f"Created example item: {item}")
        print(f"  Type: {item.item_type}")
        print(f"  Description: {item.description}")
        print(f"  Value: {item.value}")
        print(f"  Stackable: {item.stackable}")
        print(f"  Image path: {item.image_path}")
        if item.item_type == "WEAPON":
            print(f"  Weapon type: {item.weapon_type}")
            print(f"  Damage equation: {item.dam_equation}")
            print(f"  AP cost: {item.ap_cost}")
        elif item.item_type == "ARMOR":
            print(f"  AB: {item.ab}")
        elif item.item_type == "CONSUMABLE":
            print(f"  Effect type: {item.effect_type}")
            if item.effect_type == "buff":
                print(f"  Effect status: {item.effect_status}")
                print(f"  Effect time: {item.effect_time}")
                print(f"  Effect amount: {item.effect_amount}")
            elif item.effect_type == "heal":
                print(f"  Heal amount: {item.effect_amount}")
            elif item.effect_type == "weapon":
                print(f"  Damage equation: {item.dam_equation}")
        
    # items.append(Item(
    #     name="Cool shovel",
    #     item_type="tool",
    #     description="A sturdy shovel.",
    #     image_path="../graphics/items/shovel.png",
    # ))
    
    # # Weapons
    # items.append(Weapon(
    #     name="Steel Sword",
    #     description="Heavy but powerful. Deals massive damage.",
    #     image_path="../graphics/items/sword.png",
    #     attack_bonus=15,
    #     value=200
    # ))
    
    # items.append(Weapon(
    #     name="Magic Sword",
    #     description="Channels magical energy for devastating spells.",
    #     image_path="../graphics/items/scithersword.png",
    #     attack_bonus=20,
    #     value=300
    # ))
    
    
    # items.append(Weapon(
    #     name="Legendary Staff",
    #     description="Forged by ancient masters. Extremely powerful!",
    #     image_path="../graphics/items/staff.png",
    #     attack_bonus=50,
    #     value=1000
    # ))


    # items.append(Consumable(
    #     name="Antidote",
    #     description="Cures poison. Keep one handy!",
    #     image_path="../graphics/items/potion_yellow.png",
    #     effect_type="cure",
    #     effect_amount=0,
    #     value=15,
    #     max_stack=10
    # ))
    
    # items.append(Consumable(
    #     name="Elixir",
    #     description="Fully restores HP and mana. Very rare!",
    #     image_path="../graphics/items/potion_purple.png",
    #     effect_type="full_restore",
    #     effect_amount=999,
    #     value=500,
    #     max_stack=5
    # ))
    
    # # Armor
    # items.append(Armor(
    #     name="Leather Armor",
    #     description="Light protective gear. Comfortable and flexible.",
    #     image_path="../graphics/items/leather_armor.png",
    #     defense_bonus=5,
    #     value=80
    # ))
    
    # items.append(Armor(
    #     name="Chain Mail",
    #     description="Strong metal links provide excellent protection.",
    #     image_path="../graphics/items/chain_mail.png",
    #     defense_bonus=12,
    #     value=250
    # ))
    
    # items.append(Armor(
    #     name="Wooden Shield",
    #     description="Basic shield. Better than nothing!",
    #     image_path="../graphics/items/wooden_shield.png",
    #     defense_bonus=3,
    #     value=40
    # ))
    
    # items.append(Armor(
    #     name="Dragon Scale Armor",
    #     description="Crafted from real dragon scales. Legendary defense!",
    #     image_path="../graphics/items/dragon_armor.png",
    #     defense_bonus=25,
    #     value=2000
    # ))
    
    # # Consumables
    # items.append(Consumable(
    #     name="Health Potion",
    #     description="Restores 50 HP. Tastes like cherries.",
    #     image_path="../graphics/items/health_potion.png",
    #     effect_type="heal",
    #     effect_amount=50,
    #     value=25,
    #     max_stack=99
    # ))
    
    # items.append(Consumable(
    #     name="Mana Potion",
    #     description="Restores 30 mana. Glows with magical energy.",
    #     image_path="../graphics/items/mana_potion.png",
    #     effect_type="mana",
    #     effect_amount=30,
    #     value=20,
    #     max_stack=99
    # ))
    
    # items.append(Consumable(
    #     name="Super Health Potion",
    #     description="Restores 100 HP! Very potent.",
    #     image_path="../graphics/items/super_potion.png",
    #     effect_type="heal",
    #     effect_amount=100,
    #     value=75,
    #     max_stack=50
    # ))
    
    # items.append(Consumable(
    #     name="Stamina Drink",
    #     description="Increases speed temporarily.",
    #     image_path="../graphics/items/stamina_drink.png",
    #     effect_type="speed",
    #     effect_amount=5,
    #     value=30,
    #     max_stack=20
    # ))
    
    
    
    print(f"Created {len(items)} example items")
    return items


# if __name__ == "__main__":
#     # Test item creation
#     pygame.init()
#     pygame.display.set_mode((1, 1))
#     print("Testing Item classes...\n")
    
#     test_gun = Weapon("OLD_WORLD_PISTOL",1)
#     print(f"Created: {test_gun}")
#     print(f"Type: {test_gun.item_type}")
#     print(f"Damage: {test_gun.dam_equation}\n")
    
#     test_consumable = Consumable("DISTILLED_WATER",1)
#     print(f"Created: {test_consumable}")
#     print(f"Stackable: {test_consumable.stackable}")
#     print(f"Max stack: {test_consumable.max_stack}\n")
    
#     test_armor = Armor("SUPERCOOLED_ARMOR",1)
#     print(f"Created: {test_armor}")
#     print(f"AB: {test_armor.ab}")
    
#     create_example_items()
#     print("Item tests completed!")