"""
Linked_list.py - Linked list implementation

Implements different types of linked lists for NPC movement:
This is a doubly linked list
I implemented this as a more standard version as opposed to the one in patrol_path

Author: Owen Ringrose
"""
class Node:
    def __init__(self, value):
        self.prev = None
        self.next = None
        self.value = value
    
class Linked_List:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        """
        Appends to linked list
         Args:
            value : Value of item being appeneded
        """
        self.length += 1
        new = Node(value)

        if (self.head is None):
            self.head = new
            self.tail = new
            return
        
        self.tail.next = new
        new.prev = self.tail
        self.tail = new

    def delete_at_index(self, index):
        """
        Deletes item at index of linked list
        Args:
            index (int): index of which to delete
        returns:
            value: value of index that was removed
        """
        if self.head is None:
            return None
        
        if index < 0 or index >= self.length:
            raise IndexError("Index out of bounds")
        
        self.length -= 1

        if (index == 0):
            value = self.head.value
            self.head = self.head.next 
            if self.head is not None:
                self.head.prev = None
            return value

        elif(index == self.length):
            value = self.tail.value
            self.tail = self.tail.prev
            self.tail.next = None
            return value

        cur = self.head
        for i in range(index):
            cur = cur.next
        
        cur.prev.next = cur.next
        cur.next.prev = cur.prev

        return cur.value

    def get_index(self,value):
        """
        Returns the index of a value
        returns -1 if value is not in list
        Args:
         value: value to find index of
        """
        cur = self.head
        index = 0
        while cur is not None:
            if cur.value == value:
                return index
            cur = cur.next
            index += 1
        return -1
    
    def __getitem__(self, index):
        """
        Returns an element at a given index. Used with bracket notation. ie: LL[3]
        """
        if (index == -1):
            index = self.length - 1

        if (index >= self.length or index < 0):
            raise IndexError("Index out of bounds")
        else: 
            current = self.head
            for i in range(index):
                current = current.next
            return current.value
                

    
    # Enables bracket notation for setting elements: my_list[3] = 42
    def __setitem__(self, index, value):
        """
        Sets the value at a certain index. Used with bracket notation. ie: my_array[3] = 42
        """
        if (index == -1):
            index = self.length - 1

        if (index >= self.length or index < 0):
            raise IndexError("Index out of bounds")
        else: 
            current = self.head
            for i in range(index):
                current = current.next
            current.value = value
            return current.value

    def __len__(self):
        return self.length



        
        