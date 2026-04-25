"""
stack_tests.py - Test suite for Stack implementation

Tests all Stack methods with edge cases.

Author: Emmanuel Morales
Date: February 18, 2026
Lab: Lab 4 - Time Travel with Stacks
"""

import sys
sys.path.append('../..')
from datastructures.stack import Stack
from datastructures.array import ArrayList


def test_stack_init():
    """
    Test initializing an empty Stack
    """
    stack = Stack()
    assert stack.is_empty() == True, "New stack should be empty"
    assert stack.size() == 0, "New stack should have size 0"
    assert stack.my_stack.capacity == 10, "Stack should have default capacity of 10"
    print("✓ Stack initialization works correctly!")

def test_stack_push_peek_pop():
    """
    Test pushing, peeking, and popping items from Stack
    """
    stack = Stack()
    
    # Test peeking and popping from an empty stack
    assert stack.peek() is None, "Peeking empty stack should return None"
    assert stack.pop() is None, "Popping empty stack should return None"

    # Test pushing items
    stack.push(1)
    assert stack.peek() == 1, "Peek should return 1"
    assert stack.size() == 1, "Stack size should be 1 after one push"
    
    stack.push(2)
    assert stack.peek() == 2, "Peek should return 2"
    assert stack.size() == 2, "Stack size should be 2 after two pushes"
    
    # Test popping items
    popped = stack.pop()
    assert popped == 2, "Pop should return 2"
    assert stack.peek() == 1, "Peek should return 1 after popping 2"
    assert stack.size() == 1, "Stack size should be 1 after popping one item"
    
    popped = stack.pop()
    assert popped == 1, "Pop should return 1"
    assert stack.is_empty() == True, "Stack should be empty after popping all items"

    popped = stack.pop()
    assert popped is None, "Popping from empty stack should return None"
    
    print("✓ Stack push, peek, and pop all work correctly!")

def test_stack_empty_clear():
    """
    Test is_empty and clear methods from Stack
    """
    stack = Stack()

    assert stack.is_empty() == True, "New stack should be empty"

    stack.push(1)
    assert stack.is_empty() == False, "Stack should not be empty after pushing an item"

    stack.push(2)
    stack.push(3)
    assert stack.size() == 3, "Stack size should be 3 after pushing three items"

    stack.clear()   
    assert stack.is_empty() == True, "Stack should be empty after clear"
    assert stack.size() == 0, "Stack size should be 0 after clear"
    
    print("✓ Stack is_empty and clear work correctly!")

def test_stack_str():
    """
    Test the string representation of the Stack
    """
    stack = Stack()
    assert str(stack) == "My stack: []", "String representation of empty stack should be 'My stack: []'"
    
    stack.push(1)
    assert str(stack) == "My stack: [1]", "String representation should show the integer in the stack"
    
    stack.push("hello")
    assert str(stack) == "My stack: [1, hello]", "String representation should show the integer and string in stack"

    stack.push(3.14)
    assert str(stack) == "My stack: [1, hello, 3.14]", "String representation should show an integer, string, and float in stack"
    
    print("✓ Stack __str__ method works correctly!")

def run_all_tests():
    """Run all stack tests"""
    print("=" * 50)
    print("Running Stack Tests")
    print("=" * 50)
    print()
    
    test_stack_init()
    test_stack_push_peek_pop()
    test_stack_empty_clear()
    test_stack_str()
    
    print()
    print("=" * 50)
    print("✓ ALL TESTS PASSED!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
