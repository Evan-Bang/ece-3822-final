"""
Test functions for BST.py

Author: Owen Ringrose
date: 4/19/2026

Run using: 
"""""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.BST import BST


# ==========================================================================
# Example tests to get you started
# ==========================================================================

def test_set_and_get():
    m = SparseMatrix()
    m.set(0, 0, 5)
    assert m.get(0, 0) == 5, f"Expected 5, got {m.get(0, 0)}"
    print("test_set_and_get: PASSED")


def test_default_value():
    m = SparseMatrix()
    assert m.get(99, 99) == 0, "Unset entries should return default (0)"
    print("test_default_value: PASSED")


def test_custom_default():
    m = SparseMatrix(default=-1)
    assert m.get(0, 0) == -1, "Custom default should be -1"
    print("test_custom_default: PASSED")


def test_len_empty():
    m = SparseMatrix()
    assert len(m) == 0, "Empty matrix should have length 0"
    print("test_len_empty: PASSED")


def test_len_after_set():
    m = SparseMatrix()
    m.set(1, 2, 10)
    m.set(3, 4, 20)
    assert len(m) == 2, f"Expected 2 entries, got {len(m)}"
    print("test_len_after_set: PASSED")


def test_items():
    """Test the items() method to yield all non-default entries."""
    m = SparseMatrix()
    m.set(0, 0, 5)
    m.set(1, 2, 10)
    m.set(3, 4, 20)
    
    assert len(m.items()) == 3
    expected_items = [((0, 0), 5), ((1, 2), 10), ((3, 4), 20)]
    actual_items = list(m.items())
    for item in actual_items:
        assert item in expected_items
    
    print("test_items: PASSED")

def test_overwrite():
    """Test that setting a position twice keeps only the latest value."""
    m = SparseMatrix()
    m.set(1, 1, 5)
    assert m.get(1, 1) == 5
    
    m.set(1, 1, 10)
    assert m.get(1, 1) == 10
    
    print("test_overwrite: PASSED")

def test_set_to_default_removes_entry():
    """Test that setting a position to default removes the entry."""
    m = SparseMatrix(default = 0)
    m.set(1, 1, 5)
    assert len(m) == 1
    
    m.set(1, 1, 0) 
    assert len(m) == 0
    
    print("test_set_to_default_removes_entry: PASSED")

def test_large_sparse():
    """Test that a large sparse matrix uses minimal memory."""
    m = SparseMatrix(default=None)
    for i in range(100000):
        m.set(i, i, i)
    assert len(m) == 100000
    print("test_large_sparse: PASSED")

def test_identity_multiply():
    """Test that multiplying by an identity matrix returns the original matrix."""
    m = SparseMatrix(rows=2, cols=2)
    m.set(0, 0, 1)
    m.set(0, 1, 1)
    
    identity = SparseMatrix(rows=2, cols=2)
    identity.set(0, 0, 1)
    identity.set(1, 1, 1)
    
    result = m.multiply(identity)
    
    assert result.get(0, 0) == 1
    assert result.get(0, 1) == 1
    print("test_identity_multiply: PASSED")

def test_multiply_empty():
    """Test that multiplying by an empty matrix returns an empty matrix."""
    m = SparseMatrix(rows=2, cols=2)
    m.set(0, 0, 1)
    m.set(0, 1, 1)
    m.set(1, 0, 1)
    m.set(1, 1, 1)
    
    empty = SparseMatrix(rows=2, cols=2)
    
    result = m.multiply(empty)
    
    assert len(result) == 0
    print("test_multiply_empty: PASSED")

def test_str():
    """Test that __str__ returns a non-empty string."""
    
    m = SparseMatrix()
    m.set(0, 0, 1)
    m.set(1, 1, 2)
    
    s = str(m)
    assert isinstance(s, str)
    assert len(s) > 0
    
    print("test_str: PASSED")

def test_multiply_basic():
    """Test a hand-computed 2x2 example."""
    # A = [[1,2],[3,4]], B = [[5,6],[7,8]]
    # C = [[19,22],[43,50]]
    m1 = SparseMatrix(rows=2, cols=2)
    m1.set(0, 0, 1)
    m1.set(0, 1, 2)
    m1.set(1, 0, 3)
    m1.set(1, 1, 4)
    
    m2 = SparseMatrix(rows=2, cols=2)
    m2.set(0, 0, 5)
    m2.set(0, 1, 6)
    m2.set(1, 0, 7)
    m2.set(1, 1, 8)
    
    result = m1.multiply(m2)
    
    assert result.get(0, 0) == 19
    assert result.get(0, 1) == 22
    assert result.get(1, 0) == 43
    assert result.get(1, 1) == 50
    
    print("test_multiply_basic: PASSED")


if __name__ == '__main__':
    test_set_and_get()
    test_default_value()
    test_custom_default()
    test_len_empty()
    test_len_after_set()

    test_multiply_basic()
    test_items()
    test_multiply_empty()
    test_identity_multiply()
    test_str()
    test_overwrite()
    test_set_to_default_removes_entry()
    test_large_sparse()