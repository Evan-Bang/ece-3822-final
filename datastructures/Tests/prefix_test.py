"""
Test functions for BST.py

Author: Owen Ringrose
date: 4/19/2026

Run from /tests dir using: python BST_test.py
"""""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.prefix_tree import prefix_tree

def main():
    pt = prefix_tree()
    pt.add_word("apple")
    pt.add_word("anderdingus")
    pt.add_word("and")
    pt.add_word("a")
    pt.add_word("awesome")
    pt.add_word("bubble")
    pt.add_word("tea")
    
    words = pt.find_words("a")
    print(words)
    



if __name__ == '__main__':
    main()