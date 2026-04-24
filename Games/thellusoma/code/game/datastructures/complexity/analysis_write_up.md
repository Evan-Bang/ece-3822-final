# Sparse Matrix Complexity Analysis

**Name:** [Your Name]
**Date:** [Date]
**Implementation:** [DOK]

---

## Overview

Describe your implementation choice and why you chose it.  For example:
- What backing data structure does it use?
- Why is it appropriate for the tile-map use case?
- What trade-offs does it make compared to the other options?
It uses a hash table that hashes tuples (matrix coordinates). This is a dictionary of keys (DOK) implementation. It works since most of the values of a tilemap (especially a collision map) are zero or empty. There is somewhat of a tradeoff when the tilemaps get more complex since there will be more nonzero than zero values, but for basic games like this it works fine.
---

## Time Complexity

Fill in the `?` cells after analysing your implementation.

| Operation | Your SparseMatrix | scipy sparse (CSR) | numpy dense |
|-----------|-------------------|--------------------|-------------|
| `set(r, c, v)` | O(n) | O(nnz) amortised | O(1) |
| `get(r, c)` | O(1) | O(log nnz) | O(1) |
| `items()` iteration | O(nnz) | O(nnz) | O(n²) |
| `multiply(other)` | O(nnz²) | O(nnz²/n) | O(n³) |

*nnz = number of non-zero entries, n = matrix dimension side length*

Explain your reasoning for each `?` in a sentence or two.
Since my set uses a hash table, it keeps the O(1) set. However, it still does take some time to traverse each bucket at large n, so I would consider it O(n).
Again since it is implemented with a hash table and arrays, the get method keeps the O(1) complexity.
The items iteration is O(nnz) since it needs to iterate through each non-zero value.
The multiply method is O(nnz²) since it loops through each sparse matrix once (two loops).
---

## Benchmark Results

Run `sparse_matrix_complexity.py` and paste the output here:
==================================================
Running SparseMatrix Complexity Tests
==================================================

Scipy CSR build time: 0.0009 seconds
Scipy CSR random access time: 0.0193 seconds
Scipy CSR items() time: 0.0008 seconds
Scipy CSR multiply() time: 0.0002 seconds

Numpy dense build time: 0.0020 seconds
Numpy dense random access time: 0.0021 seconds
Numpy dense items() time: 0.0047 seconds
Numpy dense multiply() time: 1.0581 seconds

SparseMatrix build time: 0.0118 seconds
SparseMatrix random access time: 0.0023 seconds
SparseMatrix items() time: 0.0012 seconds
SparseMatrix multiply() time: 0.0218 seconds

==================================================
✓ ALL TESTS COMPLETED!
==================================================

```
(paste timing table here)
```
Operation | SparseMatrix | scipy | numpy
set       | 0.0118 seconds | 0.0009 seconds | 0.0020 seconds
get       | 0.0023 seconds | 0.0193 seconds | 0.0021 seconds
items     | 0.0012 seconds | 0.0008 seconds | 0.0047 seconds
multiply  | 0.0218 seconds | 0.0002 seconds | 1.0581 seconds
---

## Space Complexity

| Representation | Space Used |
|----------------|-----------|
| Dense n×n      | O(n²)     |
| Your sparse    | O(nnz)      |

At what density (percentage of non-zero entries) does your sparse matrix
use *more* memory than a dense matrix?  Show your reasoning.
When the density is high, then the sparse matrix will use more memory since there is more memory used per element of the sparse matrix (coords and value) than in a dense matrix (just the value).
---

## Observations

1. How does your implementation compare to scipy in terms of speed?
It's pretty close for the most part and even slightly faster for get, although slower in set.
2. When is a sparse representation faster than a dense one?
Whenever most of the data points in the matrix are zero (definition of sparse matrix)
3. Was the overhead per entry (your structure vs. numpy array) noticeable?
Yes, since my set function is generally slower than the others. This may be due to resizing for large n.
---

## Conclusions

Write 2–3 sentences summarising what you learned about sparse data structures
from this experiment.

---

I learned that sparse matrices are a hash map representation of a matrix. By only hashing non-zero elements and their coordinates, it helps save on memory and time when the values of the matrix are mostly zero.

## References

List any resources (textbooks, websites, papers) you used.
