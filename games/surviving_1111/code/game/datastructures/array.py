"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Owen RIngrose
Date: 2/9/2026
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self, initial_capacity=10):
        """
        Initialize an empty ArrayList with a given initial capacity.
        """
        # TODO: Initialize instance variables
        self.capacity = initial_capacity
        self.size = 0
        self.data = [None] * self.capacity

    def get_capacity(self):
        """
        Returns capacity of list
        """
        return self.capacity
        
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        Returns the number of elements when you call len(my_array)
        """
        return self.size
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """
        Returns an element at a given index. Used with bracket notation. ie: my_array[3]
        """
        if (index == -1):
            index = self.size - 1

        if (index >= self.size or index < 0):
            raise IndexError("Index out of bounds")
        else: 
            return self.data[index]

    
    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """
        Sets the value at a certain index. Used with bracket notation. ie: my_array[3] = 42
        """
        if (index >= self.size or index < 0):
            raise IndexError("Index out of bounds")
        else: 
            self.data[index] = value
    
    def append(self, value):
        """
        Adds item to the end of the list. If memory isnt allocated, double the size of the array.
        """
        if (self.size >= self.capacity):
            temp_data = [None] * (self.capacity * 2)
            for i in range(self.size):
                temp_data[i] = self.data[i]
            self.data = temp_data
            self.capacity *=2
        
        self.data[self.size] = value
        self.size += 1 
    
    def insert(self, index, value):
        """
        Inserts item in the middle of the list. If space is required double it.
        """
        if (index < 0 or index > self.size):
            raise IndexError("Index out of bounds")

        if self.size == self.capacity:
             temp_data = [None] * (self.capacity * 2)
             for i in range(self.size):
                temp_data[i] = self.data[i]
             self.data = temp_data
             self.capacity *= 2

        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]

        self.data[index] = value
        self.size += 1

    
    def remove(self, value):
        """
        Removes the first occurance of a value in this list, returns ValueError if the value is not contained in the list
        """
        # Find where the value is in the list
        index = -1
        for i in range(self.size):
            if (self.data[i] == value):
                index = i
                break
        
        if (index == -1):
            raise ValueError("Value not contained in list")
        
       
        # Copy data over 1, removing the indexed value
        for i in range(index, self.size - 1): 
            self.data[i] = self.data[i+1]

        # Update the size
        self.size += -1
        self.data[self.size] = None

        
    
    def pop(self, index=-1):
        """
        Remove the item at the given position in the list, and return it. If no index is specified
        a.pop() removes and returns the last item in the list. 
        It raises an IndexError if the list is empty or the index is outside the list range.
        """
        if (index < -1 or index >= self.size):
            raise IndexError("Index out of bounds")
        
        if (self.size == 0):
            raise IndexError("Cannot pop from empty list")

        # Handle a value of -1 for index
        if index == -1:
            index = self.size - 1

        # Get value so we can return
        value = self.data[index]

        # Copy data over 1, removing the indexed value
        for i in range(index, self.size - 1): 
            self.data[i] = self.data[i+1]

        # Update the size
        self.size += -1
        self.data[self.size] = None
        
        return value
    
    def clear(self):
        """
        Remove all items from the list.
        """
        for i in range(self.size):
            self.data[i] = None
        self.size = 0
        
    
    def index(self, value):
        """
        Return zero-based index of the first occurrence of x in the list. Raises a ValueError if there is no such item.
        """

        # Loop through and find index
        for i in range(self.size):
            if (self.data[i] == value):
                return i
        
        raise ValueError("Value not contained in list")

    def count(self, value):
        """
        Return the number of times x appears in the list.
        """
        count = 0
        for i in range(self.size):
            if self.data[i] == value:
                count += 1

        return count

    def extend(self, iterable):
        """
        Extend the list by appending all the items from the iterable. Similar to a[len(a):] = iterable.
        """
        for value in iterable:
            self.append(value)
        
    
    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        Used by python to check if the value is contained in the list
        """
        if (self.count(value) == 0):
            return False
        else:
            return True
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        Returns a string version of the list for printing
        """
        string = "["
        # append values
        for i in range(self.size):
            string += str(self.data[i])

            # Ensure we dont end with a comma
            if (i != self.size -1):
                string += ","

        string += ("]")

        return string
    
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """
        Returns a string version of the list for printing
        """
        # Use the __str__ to do this
        return str(self)
    

    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        Used to make the list iterable. https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/
        """
        # We are using yield here to turn the function intoa generator.
        for i in range(self.size):
            yield self.data[i]

