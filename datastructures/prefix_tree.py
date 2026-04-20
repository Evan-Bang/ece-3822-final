"""
prefix_tree.py - prefix tree (trie) implementation

see https://www.geeksforgeeks.org/dsa/trie-insert-and-search/ for more info

Author: Owen Ringrose
Date: 4/19/2026
**** Revision History ****
-4/19/2026: File created
"""
from datastructures.hash_table import HashTable

class prefix_node:
    """
    Node in the prefix tree. Children are stored in hash table because they are so cool
    """
    def __init__(self, char):
        self.char = char
        self.children = HashTable(initial_capacity=26)
        self.is_end_of_word = False

class prefix_tree: 
    """
    Prefix tree (trie) implementation. Words are stored as paths from the root to the leaf of the tree. 
    Words can also end in partial paths if indicated
    """

    def __init__(self):
        self.root = prefix_node(None)

    def add_word(self, word):
        """ Add words to prefix tree """
        if not (isinstance(word, str)):
            raise TypeError
        else:
            current = self.root
            for char in word:
            # Add each char as a node in trie
                if char not in current.children:
                    current.children.set(char, prefix_node(char))
                    current = current.children.get(char)

                # set to true when at end of word
                current.is_end_of_word == True