"""
hash_table.py - Hash Table implementation

Only required if you implement SparseMatrix using DOK (Option A).

Author: Owen Ringrose
Date:   4/3/2026
Lab:    Lab 6 - Sparse World Map
"""
import math
from .array import ArrayList
from .patrol_path import PatrolPath
from .linked import Linked_List
class HashTable:

    def __init__(self, initial_capacity=64):
        self.capacity = initial_capacity
        self.array = ArrayList(self.capacity)
        # updates the array size.
        self.prefill_array()
        self.element_count = 0
        self.load_factor = 0
        self.load_factor_threshold = 0.75
        # Keeps track if we are resizing to 
        self.resizing = False
        
    def prefill_array(self):
        """Prefills the array with None values, used for resizing"""
        self.array = ArrayList(self.capacity)
        for _ in range(self.capacity):
            self.array.append(None)

    def _hash(self, key):
        """Hash function for integer and tuple keys, Uses the Cormen's Multiplication method, for tuples combines the elements using XORs"""
        A = (5**0.5 - 1) / 2  # This number just has to be random and real this is a common choice
        prime = 31
        if isinstance(key, tuple):
            k = 0
            i = 1
            for element in key:
                if not isinstance(element, int):
                    raise TypeError("Keys must be integers or tuples of integers.")
                    
                #Multiplication Method (Cormen)
                k = (element*(prime**i)) ^ k
                i +=1
        elif isinstance(key, int):
            k = key
        else:
            raise TypeError("Keys must be integers or tuples of integers.")
        s = k*A
        x = s % 1
        index = math.floor(self.capacity * x)
        return index


    def set(self, key, value):
        """ Set a value in the hash table, handles collisions using chaining, used to update value or add new one"""
        index = self._hash(key)
        if self.array[index] is None:
            # Linked List
            self.array[index] = Linked_List() 
        # Add the key-value pair to the linked list at the index
        current = self.array[index].head
        while current is not None:
            (k, v) = current.value
            if k == key:
                current.value = (k, value)
                return
            current = current.next
            
        self.array[index].append((key, value))
        if not self.resizing:
            self.element_count += 1
            self.load_factor = self.element_count / self.capacity 
            if self.load_factor > self.load_factor_threshold:
                self._resize()
        return
       
            
    def get(self, key, default=None):
        """ Get a value from the hash table, returns default if key is not found"""
        index = self._hash(key)
        if self.array[index] is None:
            return default
        current = self.array[index].head
        while current is not None:
            (k, v) = current.value
            if k == key:
                return v
            current = current.next
        return default


    def delete(self, key):
        """Deletes a value from the hash table"""
        #print("delete called with key:", key)
        index = self._hash(key)
        if self.array[index] is None:
            raise KeyError("key not in hash")
        current = self.array[index].head
        linked_index = 0
        while current is not None:
            (k, v) = current.value
            if k == key:
                #print("deleted key:", key)
                self.array[index].delete_at_index(linked_index)
                self.element_count -= 1
                #print("decreased:", key)
                self.load_factor = self.element_count / self.capacity
                return v
            current = current.next
            linked_index +=1
        raise KeyError("key not in hash")

        

    def __contains__(self, key):
        """Checks if a key is in the hash table"""
        index = self._hash(key)
        if self.array[index] is None:
            return False
        current = self.array[index].head
        while current is not None:
            (k, v) = current.value
            if k == key:
                return True
            current = current.next
        return False

    def __len__(self):
        """Returns the number of elements in the hash table"""
        return self.element_count

    def items(self):
        """Returns a list of key value pairs in the hash table"""
        items = ArrayList()
        for i in range(len(self.array)):
            if self.array[i] is None:
                pass
            elif isinstance(self.array[i], Linked_List):
                for j in range(len(self.array[i])):
                    items.append(self.array[i][j])
            else:
                raise TypeError("Collision not stored as linked list")
        return items

    def _resize(self):
        """Doubles the capacity of the table, rehashes each element"""
        self.resizing = True
        elements = self.items()
        # print("Resizing hash table from capacity", self.capacity, "to", self.capacity*2)
        self.capacity *= 2
        self.array = ArrayList(self.capacity)
        self.prefill_array()
        for key, value in elements:
            #print(f"Rehashing key: {key}, value: {value}")
            self.set(key, value)
        self.resizing = False

