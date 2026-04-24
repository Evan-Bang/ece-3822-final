"""
stack.py - Stack data structure implementation

A Last-In-First-Out (LIFO) data structure.
The last item added is the first item removed (like a stack of plates).

Author: [Your Name]
Date: [Date]
Lab: Lab 4 - Time Travel with Stacks
"""
from .array import ArrayList

class Stack(ArrayList):
    """
    A LIFO (Last-In-First-Out) data structure.
    
    The last item added is the first item removed.
    Think of it like a stack of plates - you add to the top and remove from the top.
    """
    
    def __init__(self,initial_capacity=10):
        """
        Initialize an empty stack.
        """
        super().__init__(initial_capacity)
        pass
    
    def push(self, item):
        """
        Add an item to the top of the stack.
        
        Args:
            item: The item to add to the stack
        """
        
        if self._size == self._capacity:
            self._capacity *= 2
            new_data = [None] * self._capacity
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data
        self._data[self._size] = item
        self._size += 1
        pass
    
    def pop(self):
        """
        Remove and return the top item from the stack.
        
        Returns:
            The item that was on top of the stack, or None if empty
        """
        if self._size == 0:
            return None
        data = self._data[self._size-1]
        self._data[self._size - 1] = None
        self._size -= 1
        return data
    
    def peek(self):
        """
        Return the top item without removing it.
        
        Returns:
            The item on top of the stack, or None if empty
        """
        if self._size == 0:
            return None
        index = self._size - 1
        data = self._data[index]
        return data
    
    # def is_empty(self):
    #     """
    #     Check if the stack is empty.
        
    #     Returns:
    #         bool: True if stack is empty, False otherwise
    #     """
    #     pass
    
    # def size(self):
    #     """
    #     Get the number of items in the stack.
        
    #     Returns:
    #         int: The number of items currently in the stack
    #     """
    #     pass
    
    # def clear(self):
    #     """Remove all items from the stack."""
    #     pass
    
    # def __str__(self):
    #     """String representation of the stack (for debugging)."""
    #     pass
