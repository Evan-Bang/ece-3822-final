"""
array_tests.py - Dynamic Array Implementation Tests

Test all methods in the ArrayList class to ensure they work as expected.

Author: Emmanuel Morales
Date: February 9, 2026
Lab: Lab 3 - ArrayList and Inventory System
"""

import sys
import os
import random
sys.path.append('../..')

from datastructures.array import ArrayList

def test_array_init_len():
    """Test creating an ArrayList"""
    print("Testing ArrayList creation and len...")
    
    # Test default capacity
    arr = ArrayList()
    assert len(arr) == 0, "New ArrayList should have size 0"
    assert arr.capacity == 10, "Default capacity should be 10"
    
    # Test custom capacity
    arr2 = ArrayList(initial_capacity=5)
    assert arr2.capacity == 5, "Custom capacity should be 5"
    
    print("✓ ArrayList creation works and len displays the correct size!")

def test_array_append_getitem():
    """
    Test appending elements to the ArrayList
    """
    print("Testing ArrayList append and getitem...")
    
    # Test appending elements and retrieving them with getitem
    arr = ArrayList()
    for i in range(9):
        # create a random element for appending to the array
        element = random.randint(1, 100)
        arr.append(element)
        assert len(arr) == i + 1, f"ArrayList should have size {i + 1} after appending"
        assert arr[i] == element, f"Element at index {i} should be {element}"
    
    print("✓ ArrayList append works and getitem retrives the correct elements!")

def test_array_setitem():
    """
    Test setting elements in the ArrayList
    """
    # Test setting elements in the array using setitem
    arr = ArrayList()
    for i in range(10):
        arr.append(None) # init an empty index
        element = random.randint(1, 100)
        arr[i] = element
        assert arr[i] == element, f"Element at index {i} should be {element}"
    
    print("✓ ArrayList setitem works!")

def test_array_resize():
    """
    Test that resize doubles the capacity of the ArrayList
    """
    arr = ArrayList(initial_capacity=2)
    for i in range(5):
        element = random.randint(1, 100)
        arr.append(element)
        assert len(arr) == i + 1, f"ArrayList should have size {i + 1} after appending"
        if (i == 2):
            assert arr.capacity == 4, "Capacity should double to 4 after appending a third element"
        if (i == 4):
            assert arr.capacity == 8, "Capacity should double to 8 after appending a fifth element"
    print("✓ ArrayList resize doubles capacity!")

def test_array_insert():
    """
    Test inserting elements at given indices within the ArrayList
    """
    arr = ArrayList()
    for i in range(5):
        element = random.randint(1, 100)
        arr.insert(i, element)
        assert arr[i] == element, f"Element at index {i} should be {element}"
    
    for i in range(5):
        element = random.randint(1, 100)
        index = random.randint(0, 4)
        arr.insert(index, element)
        assert arr[index] == element, f"Element at index {index} should be {element}"
    print("✓ ArrayList insert works correctly!")

def test_array_index_clear():
    """
    Test the index searching and array clearing of the ArrayList
    """
    # Test index searching
    arr = ArrayList()
    for i in range(10):
        arr.append(i)
        assert arr.index(i) == i, f"Index of element {i} should be {i}"

    # Test clearing the array
    assert arr.size == 10, "ArrayList should have size 10 after appending 10 elements"
    assert arr.capacity == 10, "Capacity should be 10 after appending 10 elements"
    arr.clear()
    assert arr.size == 0, "ArrayList should have size 0 after clear"
    assert arr.capacity == 10, "Capacity should remain 10 after clear"

    print("✓ ArrayList index and clear methods work correctly!")

def test_array_remove_pop_count():
    """
    Test popping and removing elements from the ArrayList
    """
    
    # Create and fill an ArrayList
    asize = 10
    arr = ArrayList(asize)
    for i in range(asize):
        arr.append(i)
    
    # Test popping elements and shifting elements forward after popping
    assert len(arr) == asize, f"ArrayList should have size {asize} after appending {asize} elements"
    popped = arr.pop() # pop the last element
    assert popped == (asize - 1), f"Popped element should be {asize - 1}"
    assert len(arr) == (asize - 1), f"ArrayList should have size {asize - 1} after popping"
    popped = arr.pop(0) # pop the first element
    assert popped == 0, "Popped element at index 0 should be 0"
    assert len(arr) == (asize - 2), f"ArrayList should have size {asize - 2} after popping again"
    assert arr[0] == 1, "Element at index 0 should now be 1 after popping the first element"

    # Test removing elements, shifting elements forward after removing, and counting elements
    count = (arr.count(2)) # There's at least a 2 in the array before removal
    arr.remove(2)
    assert arr.count(2) == count - 1, f"Count of element 2 should be {count - 1} after removal"
    assert len(arr) == (asize - 3), f"ArrayList should have size {asize - 3} after removing an element"
    assert arr[1] == 3, "Element at index 1 should now be 3 after removing the element 2"
    
    print("✓ ArrayList remove, pop, and count work correctly!")

def test_array_extend_contains():
    """
    Test extending an Arraylist and using the "in" operator
    """
    array1 = ArrayList()
    for i in range(5):
        array1.append(i)
    array2 = ArrayList()
    for i in range(5, 10):
        array2.append(i)
    
    assert len(array1) == 5, "array1 should have size 5 after appending 5 elements"
    assert len(array2) == 5, "array2 should have size 5 after appending 5 elements"
    array1.extend(array2)
    assert len(array1) == 10, "array1 should have size 10 after extending it with array2"

    for i in range(5, 10):
        assert i in array1, f"Element {i} should be in array1 after having extended it with array2"
    
    print("✓ ArrayList extend and contains work correctly!")

def test_array_iter_str_repr():
    """
    Test string representation and iteration of the ArrayList
    """
    arr = ArrayList()
    for i in range(4):
        arr.append(i)
    
    # Test string representation
    arr_str = "[0, 1, 2, 3]"
    assert str(arr) == arr_str, f"String representation should be {arr_str}"
    assert repr(arr) == arr_str, f"repr should be the same as str and should be {arr_str}"
    
    # Test iteration
    arr_list = [0, 1, 2, 3]
    for i in arr:
        assert i in arr_list, f"Element {i} should be in the list {arr_list} during iteration"

    print("✓ ArrayList string representation and iteration work correctly!")


def test_pop_negative_index():
    """
    Test popping with a negative index.
    This should pop the element at the corresponding positive index from the end of the array.
    """
    arr = ArrayList()
    for i in range(10):
        arr.append(i)

    popped = arr.pop(-2) # pop the second to last element using a negative index
    assert popped == 8, "Element should be 8 when popping with index -2"
    assert len(arr) == 9, "ArrayList should have size 9 after popping with index -2"
    
    print("✓ ArrayList pop works correctly with negative indices!")

def test_insert_at_beginning():
    """
    Test inserting elements at the beginning of the ArrayList, causing resizing and shifting.
    This tests the insert method's ability to handle edge cases where elements need to be shifted and the array needs to be resized.
    """
    arr = ArrayList(2)
    arr.append(1)
    arr.append(2)
    index1 = arr.index(1)
    assert index1 == 0, "Element 1 should be at index 0"
    assert len(arr) == 2, "ArrayList should have size 2 before inserting a new element at the beginning"
    assert arr.capacity == 2, "Capacity should be 2 before inserting a new element at the beginning"
    arr.insert(0, 0)  # This should cause a resize and shift elements
    assert arr[0] == 0, "Element at index 0 should now be 0"
    assert arr.index(1) == (index1 + 1), "Element 1 should have shifted to index 1"
    assert len(arr) == 3, "ArrayList should have size 3 after inserting a new element at the beginning"
    assert arr.capacity == 4, "Capacity should have doubled to 4 after inserting a third element"


def run_all_tests():
    """Run all tests"""
    print("="*50)
    print("Running ArrayList Tests")
    print("="*50)
    
    test_array_init_len()
    test_array_append_getitem()
    test_array_setitem()
    test_array_resize()
    test_array_insert()
    test_array_index_clear()
    test_array_remove_pop_count()
    test_array_extend_contains()
    test_array_iter_str_repr()
    test_pop_negative_index()
    test_insert_at_beginning()
    
    print("="*50)
    print("✓ ALL TESTS PASSED!")
    print("="*50)

if __name__ == "__main__":
    run_all_tests()