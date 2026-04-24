# Sparse Matrix Complexity Analysis

**Name:** Emmanuel Morales  
**Date:** April 12, 2026  
**Implementation:** COO  

---

## Overview

I chose to implement the SparseMatrix using a coordinate list, which is backed by an ArrayList that stores triples (row, column, value) of the non-default entries. The reason for choosing this implementation was the simplicity of using a data structure that I was already familiar with instead of having to create a new hash table and then having to also test it and debug it on top of the SparseMatrix. In the tile-map use case, it is expected that each tile can be one of three different types, so a sparse represantation for each type of tile would be more efficient because it would avoid iterating over tiles that don't need to be rendered. The trade off with choosing COO is the relatively slower random access versus that of a hash table.

---

## Time Complexity

| Operation | Your SparseMatrix | scipy sparse (CSR) | numpy dense |
|-----------|-------------------|--------------------|-------------|
| `set(r, c, v)` | O(nnz) | O(nnz) amortised | O(1) |
| `get(r, c)` | O(nnz) | O(log nnz) | O(1) |
| `items()` iteration | O(nnz) | O(nnz) | O(n²) |
| `multiply(other)` | O(nnz²) | O(nnz²/n) | O(n³) |

*nnz = number of non-zero entries, n = matrix dimension side length*

When using SparseMatrix.set(r, c, v), the ArrayList is scanned for a pre-existin entry with a non-zero value on the given (r,c), and when found the value would get updated. Entries with a zero would get removed, and only non-zero entries are appended to the ArrayList. The amount of searching and appending is limited to the number of non-zero entries for set(r, c, v), or O(nnz).

The SparseMatrix.get(r,c) operation is also O(nnz) because while searching for the value at the provided (r, c), only the non-zero entries are checked to see if they match the (r, c), and if an entry doesn't exist, the default 0 would be returned.

Similarly in time complexity, SparseMatrix.items() would only iterate once through each non-zero entry in the SparseMatrix, making it do O(nnz) work.

Multiplying involves iterating over the self and other SparseMatrix, which are holding a number of non-zero entries. In a worse case where both have the same number of non-zero entries, it would be O(nnz²).

---

## Benchmark Results

Run `sparse_matrix_complexity.py` and paste the output here:

```
| n | SparseMatrix `set()` (sec) | CSR build (sec) | NumPy dense build (sec) |
|---|-----------------------------|------------------|---------------------------|
| 10 | 0.000019 | 0.000147 | 0.000019 |
| 25 | 0.000064 | 0.000161 | 0.000027 |
| 50 | 0.000198 | 0.000188 | 0.000040 |
| 75 | 0.000410 | 0.000210 | 0.000052 |
| 100 | 0.000682 | 0.000245 | 0.000066 |
| 150 | 0.001478 | 0.000298 | 0.000095 |
| 200 | 0.002543 | 0.000342 | 0.000119 |
| 250 | 0.003930 | 0.000377 | 0.000150 |
| 300 | 0.005542 | 0.000425 | 0.000172 |
| 400 | 0.009911 | 0.000520 | 0.000294 |
| 500 | 0.015381 | 0.000609 | 0.000390 |
| 750 | 0.034859 | 0.000861 | 0.000679 |
| 1000 | 0.061689 | 0.001083 | 0.001008 |
| 1200 | 0.089267 | 0.001256 | 0.001300 |
| 1500 | 0.139703 | 0.001560 | 0.001833 |
| 2000 | 0.248363 | 0.002029 | 0.002876 |


| n | SparseMatrix `get` (sec) | CSR `get` (sec) | NumPy dense `get` (sec) |
|---|---------------------------|------------------|---------------------------|
| 10 | 0.000106 | 0.000597 | 0.000011 |
| 25 | 0.000551 | 0.001492 | 0.000026 |
| 50 | 0.002183 | 0.002995 | 0.000051 |
| 75 | 0.004809 | 0.004508 | 0.000077 |
| 100 | 0.008479 | 0.006011 | 0.000103 |
| 150 | 0.018920 | 0.009163 | 0.000170 |
| 200 | 0.033370 | 0.012076 | 0.000219 |
| 250 | 0.051846 | 0.014921 | 0.000274 |
| 300 | 0.075463 | 0.017979 | 0.000355 |
| 400 | 0.136554 | 0.024447 | 0.000539 |
| 500 | 0.212829 | 0.030284 | 0.000691 |
| 750 | 0.482874 | 0.045566 | 0.001075 |
| 1000 | 0.875527 | 0.060572 | 0.001449 |
| 1200 | 1.237580 | 0.072405 | 0.001783 |
| 1500 | 1.968291 | 0.091408 | 0.002274 |
| 2000 | 3.469264 | 0.121570 | 0.002654 |


| n | SparseMatrix `items` (sec) | CSR iteration (sec) | NumPy dense iteration (sec) |
|---|-----------------------------|-----------------------|------------------------------|
| 10 | 0.000003 | 0.000031 | 0.000021 |
| 25 | 0.000005 | 0.000038 | 0.000120 |
| 50 | 0.000009 | 0.000050 | 0.000465 |
| 75 | 0.000013 | 0.000062 | 0.001031 |
| 100 | 0.000017 | 0.000070 | 0.001795 |
| 150 | 0.000025 | 0.000084 | 0.003974 |
| 200 | 0.000032 | 0.000093 | 0.006995 |
| 250 | 0.000039 | 0.000106 | 0.010970 |
| 300 | 0.000049 | 0.000122 | 0.016381 |
| 400 | 0.000070 | 0.000173 | 0.029488 |
| 500 | 0.000082 | 0.000180 | 0.045310 |
| 750 | 0.000132 | 0.000263 | 0.105448 |
| 1000 | 0.000171 | 0.000343 | 0.181966 |
| 1200 | 0.000219 | 0.000387 | 0.270674 |
| 1500 | 0.000259 | 0.000461 | 0.422212 |
| 2000 | 0.000360 | 0.000568 | 0.774156 |


| n | SparseMatrix `multiply` (sec) | CSR multiply (sec) | NumPy dense multiply (sec) |
|---|-------------------------------|----------------------|------------------------------|
| 10 | 0.000050 | 0.000068 | 0.000002 |
| 25 | 0.000169 | 0.000072 | 0.000009 |
| 50 | 0.000813 | 0.000087 | 0.000062 |
| 75 | 0.001594 | 0.000090 | 0.000200 |
| 100 | 0.002863 | 0.000093 | 0.000465 |
| 150 | 0.006639 | 0.000101 | 0.001632 |
| 200 | 0.010738 | 0.000108 | 0.004581 |
| 250 | 0.017698 | 0.000120 | 0.009326 |
| 300 | 0.025181 | 0.000137 | 0.017425 |
| 400 | 0.045536 | 0.000167 | 0.046669 |
| 500 | 0.074157 | 0.000194 | 0.087407 |
| 750 | 0.168816 | 0.000215 | 0.312232 |
| 1000 | 0.307412 | 0.000229 | 0.746607 |
| 1200 | 0.441223 | 0.000241 | 1.392770 |
| 1500 | 0.673072 | 0.000248 | 2.739847 |
| 2000 | 1.213138 | 0.000292 | 13.781409 |

| n | SparseMatrix build peak (MB) | CSR build peak (MB) | NumPy dense build peak (MB) |
|---|-------------------------------|-----------------------|-------------------------------|
| 10 | 0.000432 | 0.001956 | 0.002232 |
| 25 | 0.000832 | 0.001950 | 0.007232 |
| 50 | 0.001312 | 0.001950 | 0.022232 |
| 75 | 0.001312 | 0.001950 | 0.047232 |
| 100 | 0.002272 | 0.001950 | 0.082232 |
| 150 | 0.002272 | 0.004350 | 0.185832 |
| 200 | 0.004220 | 0.005150 | 0.327032 |
| 250 | 0.004220 | 0.005950 | 0.508504 |
| 300 | 0.004276 | 0.011582 | 0.730408 |
| 400 | 0.008284 | 0.014782 | 1.293624 |
| 500 | 0.008284 | 0.017982 | 2.017064 |
| 750 | 0.015964 | 0.025982 | 4.525160 |
| 1000 | 0.015964 | 0.033982 | 8.033032 |
| 1200 | 0.015964 | 0.040382 | 11.560172 |
| 1500 | 0.031324 | 0.049982 | 18.048808 |
| 2000 | 0.031324 | 0.066142 | 32.066184 |


```

---

## Space Complexity

| Representation | Space Used |
|----------------|-----------|
| Dense n×n      | O(n²)     |
| Your sparse    | O(nnz)      |

At what density (percentage of non-zero entries) does your sparse matrix
use *more* memory than a dense matrix?  Show your reasoning.

The space complexity of SparseMatrix is O(nnz) because only non-zero entries are stored. In order for the SparseMatrix to use more memory than a dense matrix, the number of non-zero entries has to approach n². Since each entry is storing three integers (row, column, value), there's more overhead than the single integer stored in a dense matrix, so a ~33% filled SparseMatrix would be worse than a dense matrix in space complexity.

---

## Observations

1. How does your implementation compare to scipy in terms of speed?  
In terms of speed, my SparseMatrix implementation was always faster than the scipy csr_matrix when comparing iterating over the matrices, likely in part due to the fact that the csr_matrix had to be converted to COO with csr_matrix.tocoo() before before being able to iterate over it in a similar manner. If the iteration were done in its native format, it would be faster. Overall though, the scipy csr_matrix was significantly faster than the SparseMatrix implementation, unless the number of non-zero entries is something tiny like 10.

2. When is a sparse representation faster than a dense one?  
Sparse represenatation is faster than a dense one as long as the number of non-zero entries is significantly less than n². When a sparse matrix is close to being full, the dense representation will be faster.

3. Was the overhead per entry (your structure vs. numpy array) noticeable?  
The overhead per entry is larger in the SparseMatrix implementation due to the storage of the triple in the SparseMatrix, whereas the numpy array only stores the value for each entry.

---

## Conclusions

From working on this lab I learned that sparse data structures are very efficient when a full matrix would contain a few non-default entries. Although my implementation wasn't as fast when compared against CSR and Numpy, it was more space efficient than both of them on the amount of memory allocation that was needed. Outside of this lab, I would probably use Scipy when random access isn't necessary because its space complexity was similar to my SparseMatrix implementation, while having better time complexity on average than SparseMatrix.


---

## References

Googled some definitions  
Copilot for thinking through how to start the implementation