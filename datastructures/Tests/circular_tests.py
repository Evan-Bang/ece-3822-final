"""
Test functions for circular_buffer.py

Author: Owen Ringrose
date: 4/19/2026

Run from /tests dir using: python circular_tests.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.circular_buffer import CircularBuffer


def test_push_and_pop():
    """Test basic push and pop"""
    cb = CircularBuffer(5)
    cb.push(1)
    cb.push(2)
    cb.push(3)
    
    assert cb.pop() == 1
    assert cb.pop() == 2
    assert cb.pop() == 3
    print("Passed: push and pop")


def test_fifo_order():
    """Test that order is first in first out"""
    cb = CircularBuffer(5)
    for i in range(5):
        cb.push(i)

    for i in range(5):
        assert cb.pop() == i
    print("Passed: FIFO order")


def test_overflow_evicts_oldest():
    """Test that pushing past capacity evicts the oldest element"""
    cb = CircularBuffer(3)
    cb.push(1)
    cb.push(2)
    cb.push(3)
    cb.push(4)  # Should evict 1

    assert cb.pop() == 2
    assert cb.pop() == 3
    assert cb.pop() == 4
    print("Passed: overflow evicts oldest")


def test_empty_pop():
    """Test that popping from empty buffer returns None"""
    cb = CircularBuffer(3)
    assert cb.pop() is None
    print("Passed: empty pop returns None")


def test_peek():
    """Test peek does not remove element"""
    cb = CircularBuffer(3)
    cb.push(1)
    cb.push(2)

    assert cb.peek() == 1
    assert len(cb) == 2  # length unchanged
    print("Passed: peek")


def test_is_empty():
    """Test is_empty"""
    cb = CircularBuffer(3)
    assert cb.is_empty() == True
    cb.push(1)
    assert cb.is_empty() == False
    print("Passed: is_empty")


def test_len():
    """Test __len__"""
    cb = CircularBuffer(5)
    for i in range(5):
        cb.push(i)
        assert len(cb) == i + 1
    print("Passed: __len__")


def test_clear():
    """Test clear resets buffer"""
    cb = CircularBuffer(5)
    cb.push(1)
    cb.push(2)
    cb.push(3)
    cb.clear()

    assert len(cb) == 0
    assert cb.is_empty() == True
    assert cb.pop() is None
    print("Passed: clear")


def test_wrap_around():
    """Test that indices wrap correctly after pop and push"""
    cb = CircularBuffer(3)
    cb.push(1)
    cb.push(2)
    cb.push(3)
    cb.pop()  # Remove 1, start_index moves
    cb.push(4)  # Should wrap around in underlying array

    assert cb.pop() == 2
    assert cb.pop() == 3
    assert cb.pop() == 4
    print("Passed: wrap around")


def test_getitem():
    """Test index access"""
    cb = CircularBuffer(5)
    cb.push(10)
    cb.push(20)
    cb.push(30)

    assert cb[0] == 10
    assert cb[1] == 20
    assert cb[2] == 30
    print("Passed: __getitem__")


if __name__ == '__main__':
    test_push_and_pop()
    test_fifo_order()
    test_overflow_evicts_oldest()
    test_empty_pop()
    test_peek()
    test_is_empty()
    test_len()
    test_clear()
    test_wrap_around()
    test_getitem()