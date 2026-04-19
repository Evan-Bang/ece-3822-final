"""
Leaderboard.py

Author: Owen Ringrose
date: 4/17/2026

*** Revision History ***
4/17/2026: file created
"""

# Class that is stored in the BST
class leaderboard_member:
   def __init__(self, uuid, score):
        self.uuid = uuid
        self.score = score
    def __eq__(self, value):
    
