"""
sparse_matrix_tests.py - Tests for SparseMatrix

Write tests for ALL methods of your SparseMatrix implementation.
You may use AI to help generate edge cases, but make sure you understand
every test before submitting.

Run with:
    cd code/game/datastructures/tests
    python sparse_matrix_tests.py

Author: Emmanuel Morales
Date:   April 9, 2026
Lab:    Lab 6 - Sparse World Map
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.sparse_matrix import SparseMatrix
from datastructures.array import ArrayList
from scipy.sparse import csr_matrix

def test_set_and_get():
    """
    Test that set() and get() work correctly for a small matrix.
    """
    print(" Testing set() and get()...")
    matrix = SparseMatrix()
    matrix.set(0, 1, 2)
    assert matrix.get(0, 1) == 2, "get() should return 2 as set by set()"
    matrix.set(3, 4, 5)
    assert matrix.get(3, 4) == 5, "get() should return 5 as set by set()"
    assert matrix.get(6, 7) == 0, "get() should return default 0 for unset entries"
    print(" ✓ set() and get() work correctly for a small matrix.")

def test_default_value():
    """
    Test that the default value is returned for unset entries.
    """
    print(" Testing default value...")
    matrix = SparseMatrix(default=-1)
    assert matrix.get(0, 0) == -1, "get() should return default -1 for unset entries"
    matrix = SparseMatrix(default=1)
    assert matrix.get(0, 0) == 1, "get() should return default 1 for unset entries"
    print(" ✓ Default value works correctly.")

def test_len_empty():
    """
    Test that len() returns 0 for an empty matrix.
    """
    print(" Testing len() on empty matrix...")
    matrix = SparseMatrix()
    assert len(matrix) == 0, "len() should return 0 for an empty matrix"
    print(" ✓ len() works correctly for an empty matrix.")

def test_len_after_set():
    """
    Test that len() returns the correct number of stored entries after using set()
    """
    print(" Testing len() after set()...")
    matrix = SparseMatrix()
    matrix.set(0, 1, 2)
    assert len(matrix) == 1, "len() should return 1 after setting one entry"
    matrix.set(3, 4, 5)
    assert len(matrix) == 2, "len() should return 2 after setting two entries"
    matrix.set(0, 1, 0) # setting to default should remove the entry
    assert len(matrix) == 1, "len() should return 1 after changing a previous entry to default"
    print(" ✓ len() works correctly after using set().")

def test_items():
    """
    Test that items() yields exactly the non-default entries.
    """
    print(" Testing items()...")
    matrix = SparseMatrix()
    matrix.set(0, 1, 2)
    matrix.set(3, 4, 5)
    matrix.set(6, 7, 8)
    items = ArrayList() # empty list to collect items
    for item in matrix.items():
        items.append(item)
    assert len(items) == 3, "items() should yield 3 entries"
    assert ((0, 1), 2) in items, "items() should contain ((0, 1), 2)"
    assert ((3, 4), 5) in items, "items() should contain ((3, 4), 5)"
    assert ((6, 7), 8) in items, "items() should contain ((6, 7), 8)"
    print(" ✓ items() works correctly.")

def test_overwrite():
    """
    Test that overwriting an entry with set() only keeps the latest value.
    """
    print(" Testing overwrite...")
    matrix = SparseMatrix()
    matrix.set(0, 1, 2)
    matrix.set(0, 1, 3)
    assert matrix.get(0, 1) == 3, "get() should return 3 as set by the overwrite"
    print(" ✓ Overwriting works correctly.")

def test_set_to_default_removes_entry():
    """
    Test that setting an entry to its default value removes it from the matrix.
    """
    print(" Testing set to default removes entry...")
    matrix = SparseMatrix()
    matrix.set(0, 1, 2)
    assert len(matrix) == 1, "Matrix should have one entry"
    matrix.set(0, 1, 0)  # Set to default value
    assert len(matrix) == 0, "Matrix should have no entries after setting to default"
    print(" ✓ set to default removes entry correctly.")

def test_large_sparse():
    """
    Test large sparse matrix
    """
    print(" Testing large sparse matrix...")
    matrix = SparseMatrix()
    for i in range(1000):
        matrix.set(i, i, i+1)  # Set 1000 entries on the diagonal
    assert len(matrix) == 1000, "Matrix should have 1000 entries"
    print(" ✓ Large sparse matrix works correctly.")

def test_items_consistent_with_get():
    """
    Test that every (r, c) yielded by items() matches get(r, c).
    """
    print(" Testing items() consistency with get()...")
    matrix = SparseMatrix()
    matrix.set(0, 1, 2)
    matrix.set(3, 4, 5)
    matrix.set(6, 7, 8)
    for ((row_i, col_i), val_i) in matrix.items():
        assert matrix.get(row_i, col_i) == val_i, f"items() and get() inconsistent for ({row_i}, {col_i})"
    print(" ✓ items() is consistent with get().")

def test_multiply_identity():
    """
    Test that multiplying by an identity matrix returns the original matrix.
    """
    print(" Testing multiplication by identity matrix...")
    matrix = SparseMatrix()
    matrix.set(0, 1, 2)
    matrix.set(3, 4, 5)
    matrix.set(6, 7, 8)
    identity = SparseMatrix()
    identity.set(0, 0, 1)
    identity.set(1, 1, 1)
    identity.set(2, 2, 1)
    matrix.multiply(identity)
    assert matrix.get(0, 1) == 2, "Multiplication by identity should return the original matrix"
    assert matrix.get(3, 4) == 5, "Multiplication by identity should return the original matrix"
    assert matrix.get(6, 7) == 8, "Multiplication by identity should return the original matrix"
    print(" ✓ Multiplication by identity works correctly.")

def test_multiply_basic():
    """
    Test multiplication with a basic 2x2 example.
    """
    print(" Testing basic multiplication...")
    matrixA = SparseMatrix()
    matrixA.set(0, 0, 1)
    matrixA.set(0, 1, 2)
    matrixA.set(1, 0, 3)
    matrixA.set(1, 1, 4)

    matrixB = SparseMatrix()
    matrixB.set(0, 0, 5)
    matrixB.set(0, 1, 6)
    matrixB.set(1, 0, 7)
    matrixB.set(1, 1, 8)

    matrixAB = matrixA.multiply(matrixB)
    assert matrixAB.get(0, 0) == 19, "Expected 19 for (0, 0)"
    assert matrixAB.get(0, 1) == 22, "Expected 22 for (0, 1)"
    assert matrixAB.get(1, 0) == 43, "Expected 43 for (1, 0)"
    assert matrixAB.get(1, 1) == 50, "Expected 50 for (1, 1)"
    print(" ✓ Basic multiplication works correctly.")

def test_multiply_zero():
    """
    Test multiplication with a 0 matrix.
    """
    print(" Testing multiplication with zero matrix...")
    matrixA = SparseMatrix()
    matrixA.set(0, 0, 1)
    matrixA.set(0, 1, 2)
    matrixA.set(1, 0, 3)
    matrixA.set(1, 1, 4)

    matrixB = SparseMatrix() # zero matrix by default

    matrixAB = matrixA.multiply(matrixB)
    assert matrixAB.get(0, 0) == 0, "Expected 0 for (0, 0)"
    assert matrixAB.get(0, 1) == 0, "Expected 0 for (0, 1)"
    assert matrixAB.get(1, 0) == 0, "Expected 0 for (1, 0)"
    assert matrixAB.get(1, 1) == 0, "Expected 0 for (1, 1)"
    print(" ✓ Multiplication with zero matrix works correctly.")

def test_str():
    """
    Test that __str__ returns a readable non-empty string.
    """
    print(" Testing __str__...")
    matrix = SparseMatrix()
    matrix.set(0, 1, 2)
    matrix.set(3, 4, 5)
    matrix.set(6, 7, 8)
    matrix_str = matrix.__str__()
    assert isinstance(matrix_str, str), "__str__ should return a string"
    assert len(matrix_str) > 0, "__str__ should return a non-empty string"
    print(matrix_str)  # Print the string representation for visual inspection
    print(" ✓ __str__ returns a readable non-empty string.")

def run_all_tests():
    """Run all sparse matrix tests"""
    print("=" * 50)
    print("Running Sparse Matrix Tests")
    print("=" * 50)
    print()
    test_set_and_get()
    test_default_value()
    test_len_empty()
    test_len_after_set()
    test_items()
    test_overwrite()
    test_set_to_default_removes_entry()
    test_large_sparse()
    test_items_consistent_with_get()
    test_multiply_identity()
    test_multiply_basic()
    test_multiply_zero()
    test_str()
    print()
    print("=" * 50)
    print("✓ ALL TESTS PASSED!")
    print("=" * 50)

if __name__ == '__main__':
    run_all_tests()
