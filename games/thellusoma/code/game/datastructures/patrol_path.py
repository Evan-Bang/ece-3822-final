"""
patrol_path.py - Linked list implementation for NPC patrol paths

Implements different types of linked lists for NPC movement:
- Singly linked list (one-way patrol)
- Circular linked list (looping patrol)
- Doubly linked list (back-and-forth patrol)

Author: [Your Name]
Date: [Date]
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
        # TODO: Initialize head, tail, current to None
        self.head = None
        self.tail = None
        self.current = None
        # TODO: Store patrol_type
        self.patrol_type = patrol_type
        # TODO: Initialize size to 0
        self.size = 0
        # TODO: Initialize direction to 1 (1 = forward, -1 = backward for back_and_forth)
        self.direction = 1
        pass

    def add_waypoint(self, x, y, wait_time=0):
        """
        Add a waypoint to the end of the patrol path.

        Args:
            x (float): X coordinate
            y (float): Y coordinate
            wait_time (float): How long to wait at this waypoint
        """
        # TODO: Create a new Waypoint node
        waypoint = Waypoint(x, y, wait_time)
        # TODO: If the list is empty, set head, tail, and current to the new node
        # TODO: Otherwise, link the new node after the current tail
        # TODO: For "back_and_forth" and "circular", set prev pointer on the new node
        # TODO: Update tail to the new node
        if self.head is None:
            self.head = waypoint
            self.tail = waypoint
            self.current = waypoint
        else:
            self.tail.next = waypoint
            if self.patrol_type == "back_and_forth" or self.patrol_type == "circular":
                waypoint.prev = self.tail
            self.tail = waypoint
        # TODO: For "circular", close the loop (tail.next = head, head.prev = tail)
        if self.patrol_type == "circular":
            self.tail.next = self.head
            self.head.prev = self.tail
        # TODO: Increment size
        self.size += 1
        pass

    def get_next_waypoint(self):
        """
        Get the next waypoint in the patrol sequence.

        Returns:
            Waypoint: The next waypoint to move toward, or None if patrol is complete
        """
        # TODO: If empty or current is None, return None
        if self.current is None:
            return None
        # TODO: Save current as result to return
        result = self.current
        # TODO: For "one_way": advance current to current.next (becomes None at end)
        if self.patrol_type == "one_way":
            self.current = self.current.next
        # TODO: For "circular": advance current to current.next (wraps around)
        elif self.patrol_type == "circular":
            self.current = self.current.next
        # TODO: For "back_and_forth": advance forward or backward based on direction,
        #       reversing direction when hitting the end or start
        elif self.patrol_type == "back_and_forth":
            if self.direction == 1:
                if self.current.next is not None:
                    self.current = self.current.next
                else:
                    self.direction = -1
                    self.current = self.current.prev
            elif self.direction == -1:
                if self.current.prev is not None:
                    self.current = self.current.prev
                else:
                    self.direction = 1
                    self.current = self.current.next
        else:
            # if patrol type is invalid
            self.current = self.current.next
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

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError('PatrolPath indices must be integers')
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError('PatrolPath index out of range')

        node = self.head
        for _ in range(index):
            node = node.next
        return (node.x, node.y)

    def is_empty(self):
        return self.head is None

    def get_path_info(self):
        return {
            "type": self.patrol_type,
            "length": len(self),
            "current": str(self.current) if self.current else "None",
            "direction": self.direction if self.patrol_type == "back_and_forth" else "N/A"
        }
