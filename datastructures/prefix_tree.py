"""
prefix_tree.py - prefix tree (trie) implementation

see https://www.geeksforgeeks.org/dsa/trie-insert-and-search/ for more info

Author: Owen Ringrose
Date: 4/19/2026

To test run the test in /Tests/prefix_test.py
**** Revision History ****
-4/19/2026: File created
"""
from datastructures.hash_table import HashTable
from datastructures.array import ArrayList
from datastructures.stack import Stack

class prefix_node:
    """
    Node in the prefix tree. Children are stored in hash table because they are so cool
    """
    def __init__(self, char):
        self.char = char
        self.children = HashTable(initial_capacity=26)
        self.is_end_of_word = False

    def get_children(self):
        children = ArrayList()
        dict_items = self.children.items()
        for (key,value) in dict_items:
            children.append(value)
        return children
            

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
            current.is_end_of_word = True
        return word
    
    def __contains__(self, word):
        """
        Is the word in the tree
        """
        if not (isinstance(word, str)):
            return False
        else:
            current = self.root
            for char in word:
                if char not in current.children:
                    return False
                current = current.children.get(char)
            return current.is_end_of_word
    
    def find_words(self, prefix):
        """
        Returns an arraylist of all the words in the tree that start with the prefix
        """
        word_list = ArrayList()
        character_stack = Stack()
        
        if not (isinstance(prefix, str)):
            return word_list
        else:
            current = self.root

            # Get to prefix
            for char in prefix:
                if char not in current.children:
                    print("not in tree")
                    print(current.children.items())
                    return word_list
            # Start depth first
                current = current.children.get(char)
            character_stack.push((current, prefix))

            while len(character_stack) > 0:
                node, current_word = character_stack.pop()
                #print(f"Visited char {node.char}, {node.is_end_of_word} ")
            
                if node.is_end_of_word == True:
                    word_list.append(current_word)
                
                for child in node.get_children():
                    # We push the next child and what our current word is 
                    character_stack.push((child, current_word + child.char))

            return word_list
                        
                        
    def is_prefix(self, word):
        """
        check if word is the prefix of some string
        in the trie.
        """
        if not (isinstance(word, str)):
            return False
        else:
            current = self.root
            for char in word:
                if char not in current.children:
                    return False
                current = current.children.get(char)
            return True
    
    