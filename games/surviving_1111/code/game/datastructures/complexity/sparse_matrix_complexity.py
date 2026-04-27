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

Author: Owen Ringrose
Date:   4/8/2026
Lab:    Lab 6 - Sparse World Map
"""

import time
import random
import sys
import os
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix, csr_matrix
import numpy as np

#try:
 #   from scipy.sparse import csr_matrix
  #  import numpy as np
#except ImportError:
 #   return {'error': 'scipy/numpy not installed — run: pip install scipy numpy'}

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.sparse_matrix import SparseMatrix
from datastructures.array import ArrayList

def test_set_value_complexity():
    
    
    print("Testing set time complexity...")
    MAX_N = 10000      
    SAMPLE_EVERY = 50

    ns        = []
    times_our = []
    times_sp  = []
    times_np  = []

    our_matrix = SparseMatrix(default=None)
    np_matrix  = np.zeros((MAX_N, MAX_N), dtype=float)

    # pre-generate all values so all three see the same data
    all_rows = [i for i in range(MAX_N)]
    all_cols = [i for i in range(MAX_N)]
    all_vals = [random.random() for _ in range(MAX_N)]

    n = SAMPLE_EVERY
    while n <= MAX_N:
        # our implementation
        start = time.perf_counter()
        for i in range(n - SAMPLE_EVERY, n):
            our_matrix.set(all_rows[i], all_cols[i], all_vals[i])
        times_our.append((time.perf_counter() - start) / SAMPLE_EVERY)

        # scipy csr_matrix
        start = time.perf_counter()
        csr_matrix(
            (all_vals[:n], (all_rows[:n], all_cols[:n])),
            shape=(MAX_N, MAX_N)
        )
        times_sp.append((time.perf_counter() - start) / n) 

        # numpy dense 
        start = time.perf_counter()
        for i in range(n - SAMPLE_EVERY, n):
            np_matrix[all_rows[i], all_cols[i]] = all_vals[i]
        times_np.append((time.perf_counter() - start) / SAMPLE_EVERY)

        ns.append(n)
        n += SAMPLE_EVERY

    # --- plot ---
    plt.figure(figsize=(14, 6))
    plt.plot(ns, times_our, label="Our SparseMatrix (DOK/HashTable)", color="blue",   linewidth=1)
    plt.plot(ns, times_sp,  label="scipy csr_matrix ",  color="green",  linewidth=1)
    plt.plot(ns, times_np,  label="numpy dense ndarray",              color="orange", linewidth=1)

    

    plt.title("SparseMatrix set() Time Complexity Comparison")
    plt.xlabel("Number of Entries (n)")
    plt.ylabel("Average Time per set() (seconds)")
    plt.legend()
    plt.tight_layout()
    plt.savefig('sparse_matrix_set_complexity.png')
    print("Plot saved as 'sparse_matrix_set_complexity.png'")

def test_get_value_complexity():
    print("Testing get time complexity...")
    MAX_N = 10000     
    SAMPLE_EVERY = 50

    ns        = []
    times_our = []
    times_sp  = []
    times_np  = []

    our_matrix = SparseMatrix(default=None)
    np_matrix  = np.zeros((MAX_N, MAX_N), dtype=float)

    all_rows = [0 for _ in range(MAX_N)]
    all_cols = [i for i in range(MAX_N)]
    all_vals = [random.random() for _ in range(MAX_N)]

    n = SAMPLE_EVERY
    while n <= MAX_N:
        # build up to n for all three
        for i in range(n - SAMPLE_EVERY, n):
            our_matrix.set(all_rows[i], all_cols[i], all_vals[i])
            np_matrix[all_rows[i], all_cols[i]] = all_vals[i]
        sp = csr_matrix(
            (all_vals[:n], (all_rows[:n], all_cols[:n])),
            shape=(MAX_N, MAX_N)
        )

        # random indices to access
        indices = [(0, random.randint(0, n-1)) for _ in range(SAMPLE_EVERY)]
        # ---- our implementation ----
        start = time.perf_counter()
        for r, c in indices:
            our_matrix.get(r, c)
        times_our.append((time.perf_counter() - start) / SAMPLE_EVERY)

        # ---- scipy csr_matrix ----
        start = time.perf_counter()
        for r, c in indices:
            sp[r, c]
        times_sp.append((time.perf_counter() - start) / SAMPLE_EVERY)

        # ---- numpy dense ----
        start = time.perf_counter()
        for r, c in indices:
            np_matrix[r, c]
        times_np.append((time.perf_counter() - start) / SAMPLE_EVERY)

        ns.append(n)
        n += SAMPLE_EVERY

    plt.figure(figsize=(14, 6))
    plt.plot(ns, times_our, label="Our SparseMatrix (DOK/HashTable)", color="blue",   linewidth=1)
    plt.plot(ns, times_sp,  label="scipy csr_matrix",                 color="green",  linewidth=1)
    plt.plot(ns, times_np,  label="numpy dense ndarray",              color="orange", linewidth=1)

    plt.title("SparseMatrix get() Time Complexity Comparison")
    plt.xlabel("Number of Entries (n)")
    plt.ylabel("Average Time per get() (seconds)")
    plt.legend()
    plt.tight_layout()
    plt.savefig('sparse_matrix_get_complexity.png')
    print("Plot saved as 'sparse_matrix_get_complexity.png'")

def test_items_complexity():
    MAX_N = 10000     
    SAMPLE_EVERY = 500
    print("Testing items() time complexity...")

    ns        = []
    times_our = []
    times_sp  = []
    times_np  = []

    our_matrix = SparseMatrix(default=None)

    all_rows = [i for i in range(MAX_N)]
    all_cols = [i for i in range(MAX_N)]
    all_vals = [random.random() for _ in range(MAX_N)]

    n = SAMPLE_EVERY
    while n <= MAX_N:
        for i in range(n - SAMPLE_EVERY, n):
            our_matrix.set(all_rows[i], all_cols[i], all_vals[i])

        sp = csr_matrix((all_vals[:n], (all_rows[:n], all_cols[:n])), shape=(MAX_N, MAX_N))
        np_matrix = np.zeros((n, n), dtype=float)
        for i in range(n):
            np_matrix[all_rows[i], all_cols[i]] = all_vals[i]

        start = time.perf_counter()
        our_matrix.items()
        times_our.append(time.perf_counter() - start)

        start = time.perf_counter()
        sp.nonzero()
        times_sp.append(time.perf_counter() - start)

        start = time.perf_counter()
        np_matrix.flatten()
        times_np.append(time.perf_counter() - start)

        ns.append(n)
        n += SAMPLE_EVERY

    plt.figure(figsize=(14, 6))
    plt.plot(ns, times_our, label="Our SparseMatrix",color="blue",   linewidth=1)
    plt.plot(ns, times_sp,  label="scipy csr_matrix",color="green",  linewidth=1)
    plt.plot(ns, times_np,  label=f"numpy dense", color="orange", linewidth=1)

    plt.title("items() Comparison: Sparse vs Dense Iteration")
    plt.xlabel("Number of Non-Zero Entries (n)")
    plt.ylabel("Total Time for items() (seconds)")
    plt.legend()
    plt.tight_layout()
    plt.savefig('sparse_matrix_items_complexity.png')
    print("Plot saved as 'sparse_matrix_items_complexity.png'")

def test_multiply_complexity():
    MAX_N = 500     
    SAMPLE_EVERY = 25
    print("Testing multiply() time complexity...")

    ns        = []
    times_our = []
    times_sp  = []
    times_np  = []

    all_rows = [i for i in range(MAX_N)]
    all_cols = [i for i in range(MAX_N)]
    all_vals = [random.random() for _ in range(MAX_N)]

    n = SAMPLE_EVERY
    while n <= MAX_N:
        our_a = SparseMatrix(rows=n, cols=n, default=0)
        our_b = SparseMatrix(rows=n, cols=n, default=0)
        for i in range(n):
            our_a.set(all_rows[i], all_cols[i], all_vals[i])
            our_b.set(all_rows[i], all_cols[i], all_vals[i])

        sp_a = csr_matrix((all_vals[:n], (all_rows[:n], all_cols[:n])), shape=(n, n))
        sp_b = csr_matrix((all_vals[:n], (all_rows[:n], all_cols[:n])), shape=(n, n))

        np_a = np.zeros((n, n), dtype=float)
        np_b = np.zeros((n, n), dtype=float)
        for i in range(n):
            np_a[all_rows[i], all_cols[i]] = all_vals[i]
            np_b[all_rows[i], all_cols[i]] = all_vals[i]

        start = time.perf_counter()
        our_a.multiply(our_b)
        times_our.append(time.perf_counter() - start)

        start = time.perf_counter()
        sp_a.dot(sp_b)
        times_sp.append(time.perf_counter() - start)

        start = time.perf_counter()
        np.dot(np_a, np_b)
        times_np.append(time.perf_counter() - start)

        ns.append(n)
        n += SAMPLE_EVERY
    plt.figure(figsize=(14, 6))
    plt.plot(ns, times_our, label="Our SparseMatrix multiply()", color="blue",   linewidth=1)
    plt.plot(ns, times_sp,  label="scipy csr_matrix dot()",      color="green",  linewidth=1)
    plt.plot(ns, times_np,  label="numpy dense dot()",           color="orange", linewidth=1)

    plt.title("SparseMatrix multiply() Time Complexity Comparison")
    plt.xlabel("Matrix Size (n)")
    plt.ylabel("Time for multiply() (seconds)")
    plt.legend()
    plt.tight_layout()
    plt.savefig('sparse_matrix_multiply_complexity.png')
    print("Plot saved as 'sparse_matrix_multiply_complexity.png'")

def bytes_used(our_matrix):
    """Estimate bytes used by walking hash table contents"""
    size = 0
    size += our_matrix.coordinate_hash.capacity * sys.getsizeof(None)  # empty slots
    for i in range(len(our_matrix.coordinate_hash.array)):
        bucket = our_matrix.coordinate_hash.array[i]
        if bucket is not None:
            current = bucket.head
            while current is not None:
                size += sys.getsizeof(current)        # node
                current = current.next
    return size

def test_space_complexity():
    print("Testing space complexity...")
    
    MAX_N = 100
    sparsities = [i/100 for i in range(0, 101, 5)]
    
    sizes_our = []
    sizes_np  = []

    for sparsity in sparsities:
        n_entries = int(MAX_N * MAX_N * (1 - sparsity))
        
        rows = [random.randint(0, MAX_N-1) for _ in range(n_entries)]
        cols = [random.randint(0, MAX_N-1) for _ in range(n_entries)]

        our_matrix = SparseMatrix(default=None)
        for r, c in zip(rows, cols):
            our_matrix.set(r, c, random.random())

        sizes_our.append(bytes_used(our_matrix))
        sizes_np.append(MAX_N * MAX_N * 8) 

    plt.figure(figsize=(14, 6))
    plt.plot([s * 100 for s in sparsities], sizes_our, label="Our SparseMatrix)", color="blue",   linewidth=1)
    plt.plot([s * 100 for s in sparsities], sizes_np,  label=f"numpy dense ", color="orange", linewidth=1)

    plt.title(f"Space Usage vs Sparsity ({MAX_N}x{MAX_N} matrix)")
    plt.xlabel("Sparsity (% zero entries)")
    plt.ylabel("Number of Slots Allocated")
    plt.legend()
    plt.tight_layout()
    plt.savefig('sparse_matrix_space_complexity.png')
    print("Plot saved as 'sparse_matrix_space_complexity.png'")

def run_all_tests():
    """Run all performance tests and print results."""
    print("Running performance tests for SparseMatrix...")
    print("-" * 50)
    #test_set_value_complexity()
    #test_get_value_complexity()
    #test_items_complexity()
    #test_multiply_complexity()
    test_space_complexity()

if __name__ == "__main__":
    run_all_tests()