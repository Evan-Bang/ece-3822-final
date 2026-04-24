"""
array.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Emmanuel Morales
Date: February 9, 2026
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self, initial_capacity=10):
        """
        Initializes the Array with an initial capacity (default = 10).

        Args:
            initial_capacity (int): The initial capacity of the array (default is 10)
        """
        self.capacity = initial_capacity
        self.size = 0
        self.my_array = [None] * self.capacity
    
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        Returns the number of elements in the array.
        """
        return self.size
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """
        Returns the element at an index.

        Args:
            index (int): The index of the element to return
        """
        if (index >= 0 and index < self.size):
            return self.my_array[index]
        else:
            raise IndexError("Index is not valid")
    
    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """
        Sets a value for an element at an index.

        Args:
            index (int): The index of the element to set
            value: The element to set at the index
        """
        if (index >= 0 and index < self.size):
            self.my_array[index] = value
        else:
            raise IndexError("Index is not valid")
    
    # Helper for resizing the array to double its current capacity
    def resize(self):
        """
        Doubles the size of the array.
        """
        resized_capacity = self.capacity * 2
        resized_array = [None] * resized_capacity
        for i in range(self.size):
            resized_array[i] = self.my_array[i]
        self.my_array = resized_array
        self.capacity = resized_capacity
    

    def append(self, value):
        """
        Appends a value at the end of the array.

        Args:
            value: The element to append to the end of the array
        """
        if (self.size == self.capacity):
            self.resize()
        self.my_array[self.size] = value
        self.size += 1
    
    
    def insert(self, index, value):
        """
        Inserts an element at a given index, shifting elements to the back as needed.

        Args:
            index (int): The index of the element to set
            value: The element to insert at the index
        """
        # Check if index is valid
        if (index >= 0 and index <= self.size):
            # Resize array if capacity would be exceeded
            if (self.size == self.capacity):
                self.resize()
            # Shift elements to the back to make space for the new value
            for i in range(self.size, index, -1):
                self.my_array[i] = self.my_array[i-1]
            # Insert the new value at the given index
            self.my_array[index] = value
            self.size += 1
        else:
            raise IndexError("Index is not valid")

    def shiftforward(self, index):
        """
        # Shift elements to the front to overwrite and fill the space of the removed value at a given index.

        Args:
            index (int): The index of the element to remove
        """
        for i in range(index, self.size - 1):
            self.my_array[i] = self.my_array[i + 1]
        self.my_array[self.size - 1] = None
        self.size -= 1


    def remove(self, value):
        """
        Remove the first instance of a value, shifting elements to the front as needed.

        Args:
            value: The element to remove from the array
        """
        index = self.index(value)
        self.shiftforward(index)

    
    def pop(self, index=-1):
        """
        Remove the elements at a given position in the array, and return it. Removes and returns the last element by default.

        Args:
            index (int): The index of the element to remove and return (default is -1, which is the last element)
        """
        if (index <= -1):
            index = self.size + index
            if (index < 0 or index >= self.size):
                raise IndexError("Index is not valid")
        elif (index < 0 or index >= self.size):
            raise IndexError("Index is not valid")
        popped_value = self.my_array[index]
        self.shiftforward(index)
        return popped_value
            
    
    def clear(self):
        """
        Clears all elements from the array.
        """
        self.my_array = [None] * self.capacity
        self.size = 0


    def index(self, value):
        """
        Returns index of the first occurrence of a value in the array.

        Args:
            value: The element to find the first index of in the array
        """
        for i in range(self.size):
            if self.my_array[i] == value:
                return i
        raise ValueError("There is no such value in the array")


    def count(self, value):
        """
        Return the number of times a value appears in the array.

        Args:
            value: The element to count the number of instances of in the array
        """
        count = 0
        for i in range(self.size):
            if self.my_array[i] == value:
                count += 1
        return count


    def extend(self, iterable):
        """
        Extends the array by appending all the elements from the iterable.

        Args:
            iterable: An iterable of elements to append to the end of the array
        """
        for element in iterable:
            self.append(element)


    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        Returns True if the value is in the array, False otherwise.

        Args:
            value: The element to check for in the array
        """
        try:
            self.index(value)
            return True
        except ValueError:
            return False
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        Returns a user-friendly string representation of the array.
        """
        string_array = "["
        for i in range(self.size):
            string_array += str(self.my_array[i])
            if (i < self.size - 1):
                string_array += ", "
        string_array += "]"
        return string_array
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """
        Returns a developer-friendly string representation of the array.
        """
        return self.__str__()
    
    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        Makes the array iterable so you can use it in for loops.
        """
        for i in range(self.size):
            yield self.my_array[i]
            