"""
Test functions for BST.py

Author: Owen Ringrose
date: 4/19/2026

Run from /tests dir using: python BST_test.py
"""""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.BST import BST
from datastructures.leaderboard_member import leaderboard_member
import random

def append_elements():
    """Tests adding elements to a bst"""
    bst = BST()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)

    assert len(bst) == 3
    print("Passed: Appending Elements")

def delete_elements():
    """Tests deleting elements"""
    bst = BST()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)

    bst.delete(2)
    bst.delete(1)
    bst.delete(3)

    assert len(bst) == 0
    print("Passed: deleting Elements")


def test_in_order():
    """Test inorder retrival"""
    # We are using python built in here but only cause we dont have sorting logic for our own
    array = []
    bst = BST()

    for i in range(20):
        random_num = random.random()
        array.append(random_num)
        bst.insert(random_num)

    array.sort()
    BST_elements = bst.get_elements_sorted()

    for i in range(20):
        assert BST_elements[i] == array[i]
    print("Passed: get elements sorted")

def test_get_top_n():
    """Test getting top n"""
    array = []
    bst = BST()

    for i in range(20):
        random_num = random.random()
        array.append(random_num)
        bst.insert(random_num)

    array.sort(reverse=True)
    array_top_10 = array[:10]
    BST_elements = bst.get_top_n(10)
    #print(array_top_10)
    #print(BST_elements)

    assert len(BST_elements) == 10
    for i in range(10):
        assert BST_elements[i] == array_top_10[i]
    print("Passed: get n elements sorted")

    
def test_ranged_query():
    """Test ranged query of BST"""
    bst = BST()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)
    bst.insert(3.5)
    bst.insert(4)
    bst.insert(5)
    bst.insert(6)
    bst.insert(7)
    bst.insert(8)
    bst.insert(9)

    ranged_query = bst.range_query(4, 7)
    assert ranged_query[0] == 4
    assert ranged_query[1] == 5
    assert ranged_query[2] == 6
    assert ranged_query[3] == 7
    print("Passed: ranged_query")

def test_ranged_query_swapped_bounds():
    bst = BST()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)
    bst.insert(3.5)
    bst.insert(4)
    bst.insert(5)
    bst.insert(6)
    bst.insert(7)
    bst.insert(8)
    bst.insert(9)

    ranged_query = bst.range_query(7, 4)
    # Nothing should satisfy those conditions
    assert len(ranged_query) == 0

def test_tree_balance():
    bst = BST()

    for i in range(20):
        bst.insert(i)
    
    height = bst.head.height

    # This isnt the most rigorous test, we should really recursivley check each subtree but this gives an idea
    # For normal BST sorted append would give a height of 20.
    assert height == 5
    print("Passed: Balance test")


def test_search():
    bst = BST()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)
    bst.insert(4)
    bst.insert(5)

    assert bst.search(5) == 5
    assert bst.search(6) is None
    print("Passed: search test")

def test_leaderboard():
    bst = BST()

    for i in range(100):
        bst.insert(leaderboard_member(i,i))

    # Test inserting users with same score
    bst.insert(leaderboard_member(111, 20))

    assert len(bst) == 101

    top_10 = bst.get_top_n(10)
    assert top_10[0].score == 99
    assert top_10[1].score == 98 
    print("Passed: leaderboard object test")

    




if __name__ == '__main__':
    append_elements()
    delete_elements()
    test_in_order()
    test_get_top_n()
    test_ranged_query()
    test_ranged_query_swapped_bounds()
    test_tree_balance()
    test_search()
    test_leaderboard()