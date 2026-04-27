"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: [Evan Bang]
Date: [2/5/26]
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self, initial_capacity=10):
        """
        Initialize the list
        """
        # TODO: Initialize instance variables
        self._data = [None] * initial_capacity
        self._size = 0
        self._capacity = initial_capacity
        pass
    
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        Get the length of the list
        """
        # TODO: Return the size
        return self._size
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """
        Get item at index
        """
        # TODO: Return element at index
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        return self._data[index]
    
    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """
        Set item at index to a value
        """
        # TODO: Set element at index
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")
        self._data[index] = value
        pass
    
    def append(self, value):
        """
        Add value to end of list
        """
        if self._size == self._capacity:
            self._capacity *= 2
            new_data = [None] * self._capacity
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data
        self._data[self._size] = value
        self._size += 1
        pass
    
    def insert(self, index, value):
        """
        Insert value at index in list
        """
        if index < 0:
            index += self._size
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")
        if self._size == self._capacity:
            self._capacity *= 2
            new_data = [None] * self._capacity
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1
        pass
    
    def remove(self, value):
        """
        Remove any instance of a value in a list
        """
        for i in range(self._size):
            if self._data[i] == value:
                for j in range(i, self._size - 1):
                    self._data[j] = self._data[j + 1]
                self._data[self._size - 1] = None
                self._size -= 1
                return
        raise ValueError("Value not found in ArrayList")
    
    def pop(self, index=-1):
        """
        Remove the last item from the list and return it
        """
        if index < 0:
            index = self._size - 1
        data = self._data[index]
        self.remove(self._data[index])
        return data
    
    def clear(self):
        """
        Clear array and set size to zero
        """
        self._data = [None] * self._capacity
        self._size = 0
        pass
    
    def index(self, value):
        """
        Find indices for given value
        """
        for i in range(self._size):
            if self._data[i] == value:
                return i
        raise ValueError("Value not found in ArrayList")

    def count(self, value):
        """
        Count how many times a value appears in a list
        """
        count = 0
        for i in range(self._size):
            if self._data[i] == value:
                count += 1 
        return count

    def extend(self, iterable):
        """
        Append each item from iterable to list
        """
        for item in iterable:
            self.append(item)
        pass
    
    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        Checks if value is in list
        """
        for i in range(self._size):
            if self._data[i] == value:
                return True
        return False
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        Creates a string representation of the list
        """
        result = "["
        for i in range(self._size):
            result += self._data[i].__str__()
            if i < self._size - 1:
                result += ", "
        result += "]"
        return result
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """
        Creates another more code-looking representation of the list
        """
        return f"ArrayList({self.__str__()})"
    
    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        Lets the user loop through list
        """
        for i in range(self._size):
            yield self._data[i]
        pass
