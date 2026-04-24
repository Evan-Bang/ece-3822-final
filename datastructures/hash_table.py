"""
hash_table.py - Hash Table implementation

Only required if you implement SparseMatrix using DOK (Option A).

Author: [Your Name]
Date:   [Date]
Lab:    Lab 6 - Sparse World Map
"""
from datastructures.array import ArrayList

class HashTable:

    def __init__(self, initial_capacity=64):
        """Initialize a hash table with the given initial capacity."""
        self.capacity = initial_capacity
        self.buckets = ArrayList()
        for _ in range(initial_capacity):
            self.buckets.append(ArrayList())
        self.size = 0

    def _hash(self, key):
        """Return a hash value for the given key."""
        # TODO: implement your own hash function — do not use Python's hash()
        hash_value = 0
        if isinstance(key, str):
            for char in key:
                hash_value = hash_value * 31 + ord(char)
        elif isinstance(key, tuple):
            for item in key:
                hash_value = hash_value * 31 + self._hash(item)
        elif isinstance(key, int):
            hash_value = key
        return hash_value % self.capacity

    def set(self, key, value):
        """Set the value for the given key in the hash table."""
        # TODO
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))   
        self.size += 1
        if self.size / self.capacity > 0.7:
            self._resize() 

    def get(self, key, default=None):
        """Get the value for the given key from the hash table, or return default if not found."""
        # TODO
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        return default

    def delete(self, key):
        """Remove the given key from the hash table."""
        # TODO
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.remove((k, v))
                self.size -= 1
                return

    def __contains__(self, key):
        """Check if the given key is in the hash table."""
        # TODO
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return True
        return False

    def __len__(self):
        """Return the number of key-value pairs in the hash table."""
        # TODO
        return self.size

    def items(self):
        """Return an iterable of (key, value) pairs in the hash table."""
        # TODO
        values = ArrayList()
        for bucket in self.buckets:
            for key, value in bucket:
                values.append((key, value))
        return values

    def _resize(self):
        """Resize the hash table"""
        # TODO
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = ArrayList()
        for _ in range(self.capacity):
            self.buckets.append(ArrayList())
        self.size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.set(key, value)
    def to_dict(self):
        # .json requires a python dict object
        result = {}
        for key, value in self.items():
            result[key] = value
        return result