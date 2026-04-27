"""
stack.py - Stack data structure implementation

A Last-In-First-Out (LIFO) data structure.
The last item added is the first item removed (like a stack of plates).

Author: Emmanuel Morales
Date: February 18, 2026
Lab: Lab 4 - Time Travel with Stacks
"""
from datastructures.array import ArrayList

class Stack:
    """
    A LIFO (Last-In-First-Out) data structure.
    
    The last item added is the first item removed.
    Think of it like a stack of plates - you add to the top and remove from the top.
    """
    
    def __init__(self, initial_capacity=10):
        """
        Initialize an empty stack with an initial capacity.

        Args:
            initial_capacity (int): The initial capacity of the stack (default is 10)
        """
        self.my_stack = ArrayList(initial_capacity)
    
    def push(self, item):
        """
        Add an item to the top of the stack.
        
        Args:
            item: The item to add to the stack
        """
        self.my_stack.append(item)
    
    def pop(self):
        """
        Remove and return the top item from the stack.
        
        Returns:
            The item that was on top of the stack, or None if empty
        """
        if self.is_empty():
            return None
        return self.my_stack.pop()
    
    def peek(self):
        """
        Return the top item without removing it.
        
        Returns:
            The item on top of the stack, or None if empty
        """
        if self.is_empty():
            return None
        return self.my_stack[len(self.my_stack) - 1]
    
    def is_empty(self):
        """
        Check if the stack is empty.
        
        Returns:
            bool: True if stack is empty, False otherwise
        """
        return len(self.my_stack) == 0
    
    def size(self):
        """
        Get the number of items in the stack.
        
        Returns:
            int: The number of items currently in the stack
        """
        return len(self.my_stack)
    
    def clear(self):
        """Remove all items from the stack."""
        self.my_stack.clear()
    
    def __str__(self):
        """String representation of the stack (for debugging)."""
        return f"My stack: {self.my_stack}"
