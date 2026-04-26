"""
leaderboard_member.py - object to be stored in leaderoard

Author: Owen Ringrose
Date: 4/17/2026

This is so we have clean comparison logic for our BST.

**** Revision History ****
-4/19/2026: file created
"""
class leaderboard_member:
    def __init__(self, uuid, score):
        self.uuid = uuid
        self.score = score


    def get_score(self):
        return self.score
    
    def set_score(self,score):
        self.score = score

    def get_uuid(self):
        return self._uuid
    
    def __eq__(self, other):
        return (self.uuid == other.uuid and self.score == other.score)
    
    def __lt__(self, other):
        if self.score < other.score:
            return True
        elif self.score > other.score:
            return False
        else: 
            return self.uuid < other.uuid
    
    def __le__(self, other):
        if self.score <= other.score:
            return True
        elif self.score > other.score:
            return False
    
    def __gt__(self, other):
        if self.score > other.score:
            return True
        elif self.score < other.score:
            return False
        else: 
            return self.uuid > other.uuid
        
    def __ge__(self, other):
        if self.score >= other.score:
            return True
        elif self.score < other.score:
            return False

