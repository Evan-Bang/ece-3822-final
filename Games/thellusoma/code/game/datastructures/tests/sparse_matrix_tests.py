"""
sparse_matrix_tests.py - Tests for SparseMatrix

Write tests for ALL methods of your SparseMatrix implementation.
You may use AI to help generate edge cases, but make sure you understand
every test before submitting.

Run with:
    cd code/game/datastructures/tests
    python sparse_matrix_tests.py

Author: [Your Name]
Date:   [Date]
Lab:    Lab 6 - Sparse World Map
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import tracemalloc
from datastructures.sparse_matrix import SparseMatrix
from scipy.sparse import csr_matrix


# ==========================================================================
# TODO: Write your tests below
#
# Suggested test ideas (each as a separate function):
#
def test_set_and_get():
    """Test basic set() and get() functionality."""
    m = SparseMatrix()
    m.set((1, 2), 10)
    assert m.get((1, 2)) == 10
#
def test_default_value():
    """Test the default value of the matrix."""
    m = SparseMatrix()
    assert m.get((0, 0)) == 0
#
def test_custom_default():
    """Test the custom default value of the matrix."""
    m = SparseMatrix(default=5)
    assert m.get((0, 0)) == 5
#
def test_len_empty():
    """Test the len() of an empty matrix."""
    m = SparseMatrix()
    assert len(m) == 0
#
def test_len_after_set():
    """Test the len() after setting some values."""
    m = SparseMatrix()
    m.set((1, 2), 10)
    m.set((3, 4), 20)
    print(len(m))
#
def test_items():
    m = SparseMatrix()
    m.set((1, 2), 10)
    m.set((3, 4), 20)
    items = list(m.items())
    assert ((1, 2), 10) in items
    assert ((3, 4), 20) in items
    assert len(items) == 2
#     """items() should yield exactly the non-default entries."""
#
def test_overwrite():
    m = SparseMatrix()
    m.set((1, 2), 10)
    m.set((1, 2), 15)
    assert m.get((1, 2)) == 15
    m.set((1, 2), 2)
    assert m.get((1, 2)) == 2
#     """Setting a position twice keeps only the latest value."""
#
def test_set_to_default_removes_entry():
    m = SparseMatrix()
    m.set((1, 2), 10)
    assert len(m) == 1
    m.set((1, 2), 0)
    assert (1, 2) not in m.items()
    assert len(m) == 0
#     """set(r, c, default) should remove the entry so len() decreases."""
#
def test_large_sparse():
    tracemalloc.start()
    m = SparseMatrix(rows=1000, cols=1000)
    m.set((10, 10), 1)
    m.set((500, 500), 2)
    m.set((999, 999), 3)
    assert m.get((10, 10)) == 1
    assert m.get((500, 500)) == 2
    assert m.get((999, 999)) == 3
    assert len(m) == 3
    current, peak = tracemalloc.get_traced_memory()
    assert current < 100000
    assert peak < 100000
    print(f"Current memory usage: {current} B")
    print(f"Peak memory usage: {peak} B")
    tracemalloc.stop()
#     """A 1000x1000 matrix with 10 entries should use minimal memory."""
#
def test_items_consistent_with_get():
    m = SparseMatrix()
    m.set((1, 2), 10)
    m.set((3, 4), 20)
    for k, v in m.items():
        assert m.get(k) == v
#     """Every (r, c) yielded by items() should match get(r, c)."""
#
def test_multiply_identity():
    a = SparseMatrix()
    a.set((0, 0), 1)
    a.set((1, 1), 1)
    i = SparseMatrix()
    i.set((0, 0), 1)
    i.set((1, 1), 1)
    result = a.multiply(i)
    assert result.get((0, 0)) == 1
    assert result.get((1, 1)) == 1
    assert len(result) == 2
#     """A * I == A  for a 2x2 identity matrix."""
#
def test_multiply_basic():
    a = SparseMatrix()
    a.set((0, 0), 1)
    a.set((0, 1), 2)
    a.set((1, 0), 3)
    a.set((1, 1), 4)
    b = SparseMatrix()
    b.set((0, 0), 5)
    b.set((0, 1), 6)
    b.set((1, 0), 7)
    b.set((1, 1), 8)
    result = a.multiply(b)
    assert result.get((0, 0)) == 19
    assert result.get((0, 1)) == 22
    assert result.get((1, 0)) == 43
    assert result.get((1, 1)) == 50
    assert len(result) == 4
#     """Hand-computed 2x2 example."""
#
def test_multiply_zero():
    a = SparseMatrix()
    a.set((0, 0), 1)
    a.set((0, 1), 2)
    a.set((1, 0), 3)
    a.set((1, 1), 4)
    z = SparseMatrix()
    result = a.multiply(z)
    assert result.get((0, 0)) == 0
    assert result.get((0, 1)) == 0
    assert result.get((1, 0)) == 0
    assert result.get((1, 1)) == 0
    assert len(result) == 0
#     """A * Z == all-zeros (empty sparse matrix)."""
#
def test_str():
    m = SparseMatrix()
    m.set((1, 2), 10)
    s = str(m)
    print(s)
    assert isinstance(s, str)
    assert len(s) > 0
#     """__str__ should return a non-empty string."""
# ==========================================================================


if __name__ == '__main__':
    # TODO: call your tests here
    test_set_and_get()
    test_default_value()
    test_custom_default()
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
    print("All tests passed!")
