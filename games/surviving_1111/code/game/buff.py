"""
buff.py
Author: Owen Ringrose   
Date: 1/18/2026

Define the Buff class for temporary stat boosts/debuffs
"""
import pygame 
from settings import *



class Buff:
    """for temporary stat boosts/debuffs"""
    def __init__(self, stat_name, amount, duration_in_frames):
        self.stat_name = stat_name
        self.amount = amount
        self.duration = duration_in_frames
        self.elapsed_frames = 0
        
    def is_expired(self):
        if self.elapsed_frames >= self.duration:
            return True
        else:
            return False

    def update(self):
        self.elapsed_frames += 1

# End of buff.py