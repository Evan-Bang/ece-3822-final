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

Author: Emmanuel Morales
Date:   April 12, 2026
Lab:    Lab 6 - Sparse World Map
"""

import time
import random
import sys
import os
import matplotlib.pyplot as plt
import tracemalloc
sys.path.append('../..')
from datastructures.array import ArrayList
from datastructures.sparse_matrix import SparseMatrix

try:
    from scipy.sparse import csr_matrix
    import numpy as np
except ImportError:
    print({'error': 'scipy/numpy not installed — run: pip install scipy numpy'})

def generate_sparse_data(n):
    """
    Generate a random sparse pattern for a matrix of size n x n.
    Args:
        n (int): The number of rows and columns for the square matrix.
    Returns:
        rows (ArrayList): Row indices of non-default entries.
        cols (ArrayList): Column indices of non-default entries.
        values (ArrayList): Values of non-default entries.
    """
    nnz = max(1, n) # number of non-zero entries, at least 1
    rows = ArrayList()
    cols = ArrayList()
    values = ArrayList()
    for i in range(nnz):
        rows.append(random.randrange(n))
        cols.append(random.randrange(n))
        values.append(random.randrange(1, n))
    return rows, cols, values

def time_complexity_set():
    """
    Measure set() performance for SparseMatrix, csr_matrix, and numpy dense arrays.
     For each n, generate a sparse pattern and time how long it takes to build the matrices.
     Results are plotted on a log-log scale with reference lines for O(1), O(log n), O(n), O(n log n), O(n^2).
     """
    print("Time Complexity of SparseMatrix.set() vs csr_matrix vs numpy dense")
    iters = 100 # number of iterations to average over
    # number of rows/columns for the test matrices
    ns = [10, 25, 50, 75, 100] # temp
    ns = [10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000, 1200, 1500, 2000]
    sparse_times = ArrayList()
    csr_times = ArrayList()
    numpy_times = ArrayList()

    for n in ns:
        rows, cols, values = generate_sparse_data(n)
        total_sparse = 0
        total_csr = 0
        total_dense = 0

        for iteration in range(iters):
            # SparseMatrix performance measurement
            start_time = time.perf_counter()
            sparsematrix = SparseMatrix()
            for i in range(len(values)):
                row_i, col_i, val_i = rows[i], cols[i], values[i]
                sparsematrix.set(row_i, col_i, val_i)
            total_sparse += time.perf_counter() - start_time

            # Scipy CSR performance measurement
            start_time = time.perf_counter()
            csr_matrix((values, (rows, cols)), shape=(n, n))
            total_csr += time.perf_counter() - start_time

            # Numpy dense performance measurement
            start_time = time.perf_counter()
            dense = np.zeros((n, n), dtype=int)
            dense[rows, cols] = values
            total_dense += time.perf_counter() - start_time
        # Record average times for this n
        sparse_times.append(total_sparse / iters)
        print("n:", n, "\t", f"SparseMatrix set(): {total_sparse / iters:.6f} sec")
        csr_times.append(total_csr / iters)
        print("        ", f"scipy csr sparse build: {total_csr / iters:.6f} sec")
        numpy_times.append(total_dense / iters)
        print("        ", f"numpy dense build: {total_dense / iters:.6f} sec")

    plt.figure(1)
    plt.plot(ns, sparse_times, label="SparseMatrix set()")
    plt.plot(ns, csr_times, label="scipy csr sparse build")
    plt.plot(ns, numpy_times, label="numpy dense build")

    ns_ref = np.array(ns)
    min_times = min(sparse_times)
    o1 = np.ones_like(ns_ref)
    olog = np.log(ns_ref / ns_ref[0])
    on = ns_ref / ns_ref[0]
    onlogn = olog * on
    onn = (ns_ref / ns_ref[0]) ** 2
    plt.plot(ns_ref, o1 * min_times, label="O(1)", linestyle="dashed")
    plt.plot(ns_ref, olog * min_times, label="O(log n)", linestyle="dashed")
    plt.plot(ns_ref, on * min_times, label="O(n)", linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_times, label="O(n log n)", linestyle="dashed")
    plt.plot(ns_ref, onn * min_times, label="O(n^2)", linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("average time")
    plt.legend()
    plt.title("SparseMatrix.set() vs csr_matrix vs numpy dense Time Complexity")


def time_complexity_get():
    """
    Measure random access performance for SparseMatrix, csr_matrix, and numpy dense arrays.
    For each n, generate a sparse pattern and time how long it takes to perform random get() accesses.
    Results are plotted on a log-log scale with reference lines for O(1), O(log n), O(n), O(n log n), O(n^2).
    """
    print("Time Complexity of SparseMatrix.get() vs csr_matrix vs numpy dense")
    iters = 100 # number of iterations to average over
    # number of rows/columns for the test matrices
    ns = [10, 25, 50, 75, 100] # temp
    ns = [10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000, 1200, 1500, 2000]
    sparse_times = ArrayList()
    csr_times = ArrayList()
    dense_times = ArrayList()

    for n in ns:
        # Build the matrices for this n
        rows, cols, values = generate_sparse_data(n)
        # Build SparseMatrix
        sparsematrix = SparseMatrix()
        for i in range(len(values)):
            row_i, col_i, val_i = rows[i], cols[i], values[i]
            sparsematrix.set(row_i, col_i, val_i)
        # Build csr_matrix
        csr = csr_matrix((values, (rows, cols)), shape=(n, n))
        # Build numpy dense matrix
        dense = np.zeros((n, n), dtype=int)
        dense[rows, cols] = values
        # Generate random row/col pairs to access
        randomaccess = ArrayList() # array list that will hold randomly generated row/col pairs to access
        for i in range(n * 7):
            randomaccess.append((random.randrange(n), random.randrange(n)))

        total_sparse = 0
        total_csr = 0
        total_dense = 0
        # Benchmark random access for each implementation
        for iteration in range(iters):
            # SparseMatrix performance measurement
            start_time = time.perf_counter()
            for row, col in randomaccess:
                sparsematrix.get(row, col)
            total_sparse += time.perf_counter() - start_time

            # Scipy CSR performance measurement
            start_time = time.perf_counter()
            for row, col in randomaccess:
                csr[row, col]
            total_csr += time.perf_counter() - start_time

            # Numpy dense performance measurement
            start_time = time.perf_counter()
            for row, col in randomaccess:
                dense[row, col]
            total_dense += time.perf_counter() - start_time
        # Record average times for this n
        sparse_times.append(total_sparse / iters)
        print("n:", n, "\t", f"SparseMatrix get: {total_sparse / iters:.6f} sec")
        csr_times.append(total_csr / iters)
        print("        ", f"csr_matrix get: {total_csr / iters:.6f} sec")
        dense_times.append(total_dense / iters)
        print("        ", f"numpy dense get: {total_dense / iters:.6f} sec")

    plt.figure(2)
    plt.plot(ns, sparse_times, label="SparseMatrix get")
    plt.plot(ns, csr_times, label="csr_matrix get")
    plt.plot(ns, dense_times, label="numpy dense get")

    ns_ref = np.array(ns)
    min_times = min(sparse_times)
    o1 = np.ones_like(ns_ref)
    olog = np.log(ns_ref / ns_ref[0])
    on = ns_ref / ns_ref[0]
    onlogn = olog * on
    onn = (ns_ref / ns_ref[0]) ** 2
    plt.plot(ns_ref, o1 * min_times, label="O(1)", linestyle="dashed")
    plt.plot(ns_ref, olog * min_times, label="O(log n)", linestyle="dashed")
    plt.plot(ns_ref, on * min_times, label="O(n)", linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_times, label="O(n log n)", linestyle="dashed")
    plt.plot(ns_ref, onn * min_times, label="O(n^2)", linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("average time")
    plt.legend()
    plt.title("Random Access Time Complexity")


def time_complexity_items():
    """
    Measure iteration over non-default entries for SparseMatrix, csr_matrix, and numpy dense matrix.
    For each n, generate a sparse pattern and time how long it takes to iterate over non-default entries using items() for SparseMatrix and equivalent for csr_matrix.
    Results are plotted on a log-log scale with reference lines for O(1), O(log n), O(n), O(n log n), O(n^2).
    """
    print("Time Complexity of SparseMatrix.items() vs csr_matrix iteration vs numpy dense iteration")
    iters = 100 # number of iterations to average over
    # number of rows/columns for the test matrices
    ns = [10, 25, 50, 75, 100] # temp
    ns = [10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000, 1200, 1500, 2000]
    sparse_times = ArrayList()
    csr_times = ArrayList()
    dense_times = ArrayList()

    for n in ns:
        # Build the matrices for this n
        rows, cols, values = generate_sparse_data(n)
        # Build SparseMatrix
        sparsematrix = SparseMatrix()
        for i in range(len(values)):
            row_i, col_i, val_i = rows[i], cols[i], values[i]
            sparsematrix.set(row_i, col_i, val_i)
        # Build csr_matrix
        csr = csr_matrix((values, (rows, cols)), shape=(n, n))
        # Build numpy dense matrix
        dense = np.zeros((n, n), dtype=int)
        dense[rows, cols] = values

        total_sparse = 0
        total_csr = 0
        total_dense = 0

        # Benchmark iteration over non-default entries for each implementation
        for iteration in range(iters):
            # SparseMatrix performance measurement
            start_time = time.perf_counter()
            for item in sparsematrix.items():
                pass
            total_sparse += time.perf_counter() - start_time

            # Scipy CSR performance measurement
            start_time = time.perf_counter()
            csr_coo = csr.tocoo()
            rows = csr_coo.row
            cols = csr_coo.col
            values = csr_coo.data
            for i in range(len(values)):
                row_i, col_i, val_i = rows[i], cols[i], values[i]
            total_csr += time.perf_counter() - start_time

            # Numpy dense matrix performance measurement
            start_time = time.perf_counter()
            for i in range(n):
                for j in range(n):
                    if dense[i, j] != 0:
                        pass
            total_dense += time.perf_counter() - start_time

        # Record average times for this n
        sparse_times.append(total_sparse / iters)
        print("n:", n, "\t", f"SparseMatrix items: {total_sparse / iters:.6f} sec")
        csr_times.append(total_csr / iters)
        print("        ", f"csr_matrix items: {total_csr / iters:.6f} sec")
        dense_times.append(total_dense / iters)
        print("        ", f"numpy dense matrix: {total_dense / iters:.6f} sec")

    plt.figure(3)
    plt.plot(ns, sparse_times, label="SparseMatrix items")
    plt.plot(ns, csr_times, label="csr_matrix items")
    plt.plot(ns, dense_times, label="numpy dense matrix")

    ns_ref = np.array(ns)
    min_times = min(sparse_times)
    o1 = np.ones_like(ns_ref)
    olog = np.log(ns_ref / ns_ref[0])
    on = ns_ref / ns_ref[0]
    onlogn = olog * on
    onn = (ns_ref / ns_ref[0]) ** 2
    plt.plot(ns_ref, o1 * min_times, label="O(1)", linestyle="dashed")
    plt.plot(ns_ref, olog * min_times, label="O(log n)", linestyle="dashed")
    plt.plot(ns_ref, on * min_times, label="O(n)", linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_times, label="O(n log n)", linestyle="dashed")
    plt.plot(ns_ref, onn * min_times, label="O(n^2)", linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("average time")
    plt.legend()
    plt.title("Iteration over Non-default Entries")

def time_complexity_multiply():
    """
    Measure multiplication performance for SparseMatrix, csr_matrix, and numpy dense arrays.
    For each n, generate two sparse patterns and time how long it takes to multiply the matrices using 
    multiply() for SparseMatrix, dot() for csr_matrix, and dot() for numpy dense.
    """
    print("Time Complexity of SparseMatrix.multiply() vs csr_matrix vs numpy dense")
    iters = 100 # number of iterations to average over
    # number of rows/columns for the test matrices
    ns = [10, 25, 50, 75, 100] # temp
    ns = [10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000, 1200, 1500, 2000]
    sparse_times = ArrayList()
    csr_times = ArrayList()
    dense_times = ArrayList()

    for n in ns:
        # Build the matrices for this n
        rows_a, cols_a, values_a = generate_sparse_data(n)
        rows_b, cols_b, values_b = generate_sparse_data(n)
        # Build SparseMatrix
        matrix_a = SparseMatrix()
        matrix_b = SparseMatrix()
        for i in range(len(values_a)):
            row_i, col_i, val_i = rows_a[i], cols_a[i], values_a[i]
            matrix_a.set(row_i, col_i, val_i)
        for i in range(len(values_b)):
            row_i, col_i, val_i = rows_b[i], cols_b[i], values_b[i]
            matrix_b.set(row_i, col_i, val_i)
        # Build csr_matrix
        csr_a = csr_matrix((values_a, (rows_a, cols_a)), shape=(n, n))
        csr_b = csr_matrix((values_b, (rows_b, cols_b)), shape=(n, n))
        # Build numpy dense matrix
        dense_a = np.zeros((n, n), dtype=int)
        dense_b = np.zeros((n, n), dtype=int)
        dense_a[rows_a, cols_a] = values_a
        dense_b[rows_b, cols_b] = values_b

        total_sparse = 0
        total_csr = 0
        total_dense = 0
        # Benchmark multiplication for each implementation
        for iteration in range(iters):
            # SparseMatrix performance measurement
            start_time = time.perf_counter()
            matrix_a.multiply(matrix_b)
            total_sparse += time.perf_counter() - start_time
            # Scipy CSR performance measurement
            start_time = time.perf_counter()
            csr_a.dot(csr_b)
            total_csr += time.perf_counter() - start_time
            # Numpy dense performance measurement
            start_time = time.perf_counter()
            dense_a.dot(dense_b)
            total_dense += time.perf_counter() - start_time
        # Record average times for this n
        sparse_times.append(total_sparse / iters)
        print("n:", n, "\t", f"SparseMatrix multiply: {total_sparse / iters:.6f} sec")
        csr_times.append(total_csr / iters)
        print("        ", f"csr_matrix multiply: {total_csr / iters:.6f} sec")
        dense_times.append(total_dense / iters)
        print("        ", f"numpy dense multiply: {total_dense / iters:.6f} sec")

    plt.figure(4)
    plt.plot(ns, sparse_times, label="SparseMatrix multiply")
    plt.plot(ns, csr_times, label="csr_matrix multiply")
    plt.plot(ns, dense_times, label="numpy dense multiply")

    ns_ref = np.array(ns)
    min_times = min(sparse_times)
    o1 = np.ones_like(ns_ref)
    olog = np.log(ns_ref / ns_ref[0])
    on = ns_ref / ns_ref[0]
    onlogn = olog * on
    onn = (ns_ref / ns_ref[0]) ** 2
    plt.plot(ns_ref, o1 * min_times, label="O(1)", linestyle="dashed")
    plt.plot(ns_ref, olog * min_times, label="O(log n)", linestyle="dashed")
    plt.plot(ns_ref, on * min_times, label="O(n)", linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_times, label="O(n log n)", linestyle="dashed")
    plt.plot(ns_ref, onn * min_times, label="O(n^2)", linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("average time")
    plt.legend()
    plt.title("Matrix Multiplication Time Complexity")


def space_complexity_set():
    """
    Measure space complexity for building each sparse matrix implementation.
    For each n, generate a sparse pattern and measure the peak memory usage when building the matrices using set() for SparseMatrix, csr_matrix constructor, and numpy dense array construction.
    Results are plotted on a log-log scale with reference lines for O(1), O(log n), O(n), O(n log n), O(n^2).
    """
    print("Space Complexity of SparseMatrix.build() vs csr_matrix vs numpy dense")
    iters = 100 # number of iterations to average over
    # number of rows/columns for the test matrices
    ns = [10, 25, 50, 75, 100] # temp
    ns = [10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000, 1200, 1500, 2000]
    sparse_space = ArrayList()
    csr_space = ArrayList()
    dense_space = ArrayList()

    for n in ns:
        rows, cols, values = generate_sparse_data(n)
        total_sparse = 0
        total_csr = 0
        total_dense = 0

        for iteration in range(iters):
            # SparseMatrix space measurement
            tracemalloc.start()
            sparsematrix = SparseMatrix()
            for i in range(len(values)):
                row_i, col_i, val_i = rows[i], cols[i], values[i]
                sparsematrix.set(row_i, col_i, val_i)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_sparse += peak
            tracemalloc.clear_traces()

            # Scipy CSR space measurement
            tracemalloc.start()
            csr_matrix((values, (rows, cols)), shape=(n, n))
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_csr += peak
            tracemalloc.clear_traces()

            # Numpy dense space measurement
            tracemalloc.start()
            dense = np.zeros((n, n), dtype=int)
            dense[rows, cols] = values
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            total_dense += peak
            tracemalloc.clear_traces()

        # Record average space for this n
        sparse_space.append(total_sparse / iters)
        print("n:", n, "\t", f"SparseMatrix build peak: {(total_sparse / iters)/1e6:.6f} MB")
        csr_space.append(total_csr / iters)
        print("        ", f"csr_matrix build peak: {(total_csr / iters)/1e6:.6f} MB")
        dense_space.append(total_dense / iters)
        print("        ", f"numpy dense build peak: {(total_dense / iters)/1e6:.6f} MB")

    plt.figure(5)
    plt.plot(ns, sparse_space, label="SparseMatrix build memory")
    plt.plot(ns, csr_space, label="csr_matrix build memory")
    plt.plot(ns, dense_space, label="numpy dense build memory")

    ns_ref = np.array(ns)
    min_space = min(sparse_space)
    o1 = np.ones_like(ns_ref)
    olog = np.log(ns_ref / ns_ref[0])
    on = ns_ref / ns_ref[0]
    onlogn = olog * on
    onn = (ns_ref / ns_ref[0]) ** 2
    plt.plot(ns_ref, o1 * min_space, label="O(1)", linestyle="dashed")
    plt.plot(ns_ref, olog * min_space, label="O(log n)", linestyle="dashed")
    plt.plot(ns_ref, on * min_space, label="O(n)", linestyle="dashed")
    plt.plot(ns_ref, onlogn * min_space, label="O(n log n)", linestyle="dashed")
    plt.plot(ns_ref, onn * min_space, label="O(n^2)", linestyle="dashed")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("memory peak (MB)")
    plt.legend()
    plt.title("Build Space Complexity")


def show_all_plots():
    plt.show()


def run_all_analysis():
    """Run all sparse matrix complexity analysis."""
    print("=" * 50)
    print("Running SparseMatrix Complexity Analysis...")
    print("=" * 50)

    time_complexity_set()
    time_complexity_get()
    time_complexity_items()
    time_complexity_multiply()
    space_complexity_set()

    print("=" * 50)
    print("✓ COMPLETED SPARSE MATRIX COMPLEXITY ANALYSIS!")
    print("=" * 50)


if __name__ == "__main__":
    timer = time.time()
    run_all_analysis()
    print(f"Total run time = {time.time() - timer:.2f} seconds")
    show_all_plots()
