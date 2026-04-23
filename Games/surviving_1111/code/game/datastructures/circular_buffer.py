"""
circular_buffer.py - Circular Queue implementation

First in first out with a fixed length.

Author: Owen Ringrose
Date: 4/19/2026
**** Revision History ****
-4/19/2026: File created
"""
from datastructures.array import ArrayList

class CircularBuffer:
    """
    First in first out with a fixed length. Used in project for history systems like chat messages.
    """
    
    def __init__(self, capacity):
        """
        Initialize an empty queue.
        """
        self.data = ArrayList(initial_capacity= capacity)
        # fill this with Nones to avoid errors regarding acsessing data we havent appended yet
        for _ in range(capacity):
            self.data.append(None)
        self.length = 0
        self.capacity = capacity 
        self.start_index = 0
        self.end_index = 0
    
    def push(self, item):
        """
        Add an item to the queue
        
        Args:
            item: The item to add to the queue
        """
        if self.length == self.capacity:
            self.start_index = (self.start_index + 1) % self.capacity
        self.data[self.end_index] = item
        self.end_index = (self.end_index + 1) % self.capacity
        self.length = min(self.length + 1, self.capacity)
    
    def pop(self):
        """
        Remove and return the top item from the queue.
        
        Returns:
            The item that was at the front of the queue, or None if empty
        """
        if self.length == 0:
            return None
        element = self.data[self.start_index]
        self.data[self.start_index] = None
        self.start_index = (self.start_index + 1) % self.capacity
        self.length -= 1
        return element
    
    def peek(self):
        """
        Return the top item without removing it.
        
        Returns:
            The item on top of the queue, or None if empty
        """
        return self.data[self.start_index]
    
    def is_empty(self):
        """
        Check if the queueu is empty.
        
        Returns:
            bool: True if queue is empty, False otherwise
        """
        if self.length == 0:
            return True
        else:
            return False 
    
    def size(self):
        """
        Get the number of items in the queue.
        
        Returns:
            int: The number of items currently in the queue
        """
        return self.length
    
    def clear(self):
        """Remove all items from the queue."""
        self.data.clear()
        self.length = 0
        self.start_index = 0
        self.end_index = 0

    def __getitem__(self, index):
        """
        Get item at index
        """
        real_index = (self.start_index + index) % self.capacity
        return self.data[real_index]
    
    
    def __str__(self):
        """String representation of the queue (for debugging)."""
        return str(self.data)
    
    def __len__(self):
        """
        Get the length of the list
        """
        return self.size()
    