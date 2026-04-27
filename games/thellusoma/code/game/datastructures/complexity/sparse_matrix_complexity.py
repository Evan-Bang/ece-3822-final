"""
sparse_matrix_complexity.py - Performance analysis for SparseMatrix

Compare your SparseMatrix implementation to:
  - scipy.sparse (CSR format)
  - numpy dense matrix (numpy.ndarray)

Measure and report wall-clock time for:
  1. Building the matrix (set() calls)
  2. Random get() accesses
  3. items() full iteration
  4. multiply()

Run with:
    cd code/game/datastructures/complexity
    python sparse_matrix_complexity.py

Install dependencies if needed:
    pip install scipy numpy

Author: [Your Name]
Date:   [Date]
Lab:    Lab 6 - Sparse World Map
"""

import time
import random
import sys
import os
from scipy.sparse import csr_matrix as Scipy
import numpy as np


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.sparse_matrix import SparseMatrix

def test_scipy_sparse_matrix():
    data = [42] * 1000
    rows = [random.randint(0, 999) for _ in range(1000)]
    cols = [random.randint(0, 999) for _ in range(1000)]
    time_start = time.time()
    scipy_matrix = Scipy((data, (rows, cols)), shape=(1000, 1000))
    time_end = time.time()
    print(f"Scipy CSR build time: {time_end - time_start:.4f} seconds")
    time_start = time.time()
    i = 0
    while i < 1000:
        r = random.randint(0, 999)
        c = random.randint(0, 999)
        result = scipy_matrix[r, c]
        i += 1
    time_end = time.time()
    print(f"Scipy CSR random access time: {time_end - time_start:.4f} seconds")
    time_start = time.time()
    items = scipy_matrix.nonzero()
    time_end = time.time()
    print(f"Scipy CSR items() time: {time_end - time_start:.4f} seconds")
    other = Scipy((data, (rows, cols)), shape=(1000, 1000))
    time_start = time.time()
    result = scipy_matrix.dot(other)
    time_end = time.time()
    print(f"Scipy CSR multiply() time: {time_end - time_start:.4f} seconds")
def test_numpy_dense_matrix():
    rows = [random.randint(0, 999) for _ in range(1000)]
    cols = [random.randint(0, 999) for _ in range(1000)]
    time_start = time.time()
    numpy_matrix = np.ndarray((1000, 1000), dtype=int)
    for r, c in zip(rows, cols):
        numpy_matrix[r, c] = 42
    time_end = time.time()
    print(f"Numpy dense build time: {time_end - time_start:.4f} seconds")
    time_start = time.time()
    i = 0
    while i < 1000:
        r = random.randint(0, 999)
        c = random.randint(0, 999)
        result = numpy_matrix[r, c]
        i += 1
    time_end = time.time()
    print(f"Numpy dense random access time: {time_end - time_start:.4f} seconds")
    time_start = time.time()
    items = np.nonzero(numpy_matrix)
    time_end = time.time()
    print(f"Numpy dense items() time: {time_end - time_start:.4f} seconds")
    other = np.ndarray((1000, 1000), dtype=int)
    rows2 = [random.randint(0, 999) for _ in range(1000)]
    cols2 = [random.randint(0, 999) for _ in range(1000)]
    for r, c in zip(rows2, cols2):
        other[r, c] = 42
    time_start = time.time()
    result = np.dot(numpy_matrix, other)
    time_end = time.time()
    print(f"Numpy dense multiply() time: {time_end - time_start:.4f} seconds")
def test_SparseMatrix():
    sparse_matrix = SparseMatrix(rows=1000, cols=1000)
    time_start = time.time()
    i = 0
    while i < 1000:
        r = random.randint(0, 999)
        c = random.randint(0, 999)
        sparse_matrix.set((r, c), 42)
        i += 1
    time_end = time.time()
    print(f"SparseMatrix build time: {time_end - time_start:.4f} seconds")
    time_start = time.time()
    i = 0
    while i < 1000:
        r = random.randint(0, 999)
        c = random.randint(0, 999)
        result = sparse_matrix.get((r, c))
        i += 1
    time_end = time.time()
    print(f"SparseMatrix random access time: {time_end - time_start:.4f} seconds")
    time_start = time.time()
    items = sparse_matrix.items()
    time_end = time.time()
    print(f"SparseMatrix items() time: {time_end - time_start:.4f} seconds")
    other = SparseMatrix(rows=1000, cols=1000)
    product = sparse_matrix.multiply(other)
    time_end = time.time()
    print(f"SparseMatrix multiply() time: {time_end - time_start:.4f} seconds")
def run_all_tests():
    print("=" * 50)
    print("Running SparseMatrix Complexity Tests")
    print("=" * 50)
    print()
    test_scipy_sparse_matrix()
    print()
    test_numpy_dense_matrix()
    print()
    test_SparseMatrix()
    print()
    print("=" * 50)
    print("✓ ALL TESTS COMPLETED!")
    print("=" * 50)
if __name__ == '__main__':
    run_all_tests()