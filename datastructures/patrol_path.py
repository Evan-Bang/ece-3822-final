"""
patrol_path.py - Linked list implementation for NPC patrol paths

Implements different types of linked lists for NPC movement:
- Singly linked list (one-way patrol)
- Circular linked list (looping patrol)
- Doubly linked list (back-and-forth patrol)

Author: Owen
Date: Ringrose
Lab: Lab 5 - NPC Patrol Paths with Linked Lists
"""

from .waypoint import Waypoint


class PatrolPath:
    """
    A linked list of waypoints that defines how an NPC moves.

    Supports three patrol types:
    - "one_way": Walk through waypoints once, then stop
    - "circular": Loop through waypoints infinitely
    - "back_and_forth": Walk forward to end, then reverse back to start
    """

    def __init__(self, patrol_type="circular"):
        """
        Initialize an empty patrol path.

        Args:
            patrol_type (str): Type of patrol - "one_way", "circular", or "back_and_forth"
        """
   

        self.head = None
        self.tail = None
        self.current = None
        self.patrol_type = patrol_type
        self.size = 0
        self.direction = 1

    def add_waypoint(self, x, y, wait_time=0):
        """
        Add a waypoint to the end of the patrol path.

        Args:
            x (float): X coordinate
            y (float): Y coordinate
            wait_time (float): How long to wait at this waypoint
        """
    
        new_waypoint = Waypoint(x, y, wait_time)
        if (self.is_empty()):
            self.head = new_waypoint
            self.tail = new_waypoint
            self.current = new_waypoint
        else:
        
            self.tail.next = new_waypoint
        
            if (self.patrol_type != "one_way"):
                new_waypoint.prev = self.tail

            self.tail = new_waypoint

            if (self.patrol_type == "circular"):
                self.tail.next = self.head
                self.head.prev = self.tail
        
        self.size += 1

    def get_next_waypoint(self):
        """
        Get the next waypoint in the patrol sequence.

        Returns:
            Waypoint: The next waypoint to move toward, or None if patrol is complete
        """
      
        if (self.is_empty() or self.current == None):
            return None

        result = self.current

        if (self.patrol_type == "one_way"):
            self.current = self.current.next
        
        elif(self.patrol_type == "circular"):
            self.current = self.current.next
    
        else:
            # has to be a better way to do this.
            if (self.direction == 1 and self.current == self.tail) or (self.direction == -1 and self.current == self.head):
                self.direction *= -1

            if (self.direction == 1):
                self.current = self.current.next
            else:
                self.current = self.current.prev
        return result

    def reset(self):
        """Reset patrol to the beginning."""
        self.current = self.head
        self.direction = 1

    def __len__(self):
        return self.size

    def __iter__(self):
        self._iter_current = self.head
        return self

    def __next__(self):
        if self._iter_current is None:
            raise StopIteration
        result = self._iter_current
        if self._iter_current == self.tail:
            self._iter_current = None
        else:
            self._iter_current = self._iter_current.next
        return result

    def is_empty(self):
        return self.head is None

    def get_path_info(self):
        return {
            "type": self.patrol_type,
            "length": len(self),
            "current": str(self.current) if self.current else "None",
            "direction": self.direction if self.patrol_type == "back_and_forth" else "N/A"
        }