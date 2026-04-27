"""
sparse_matrix.py - Sparse Matrix implementation

A sparse matrix stores only non-default entries, saving memory when most
cells share the same value (like -1 in a tile map).

Choose one of three backing representations:

  Option A — DOK (Dictionary of Keys): {(row, col): value}
    Requires implementing HashTable in hash_table.py.
    Do not use Python's built-in dict or set.

  Option B — COO (Coordinate List): list of (row, col, value) triples
    Use your ArrayList from Lab 3. Do not use Python's built-in list.

  Option C — CSR (Compressed Sparse Row): three parallel arrays
    row_ptr, col_idx, values. Most efficient for row-wise access.

All three options must satisfy the same interface.

Author: [Your Name]
Date:   [Date]
Lab:    Lab 6 - Sparse World Map
"""
from datastructures.hash_table import HashTable
from datastructures.array import ArrayList
# =============================================================================
# Do not modify SparseMatrixBase.
# =============================================================================

class SparseMatrixBase:
    """Interface definition. Your SparseMatrix must inherit from this."""

    def __init__(self, rows=None, cols=None, default=0):
        self.rows    = rows
        self.cols    = cols
        self.default = default

    def set(self, key, value):

        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def items(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def multiply(self, other):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


# =============================================================================
# Your implementation goes here.
# =============================================================================

class SparseMatrix(SparseMatrixBase):

    def __init__(self, rows=None, cols=None, default=0):
        """Initialize a sparse matrix with the given dimensions and default value."""
        super().__init__(rows, cols, default)
        # TODO: initialize your backing data structure
        self.data = HashTable()
        self.rows = rows
        self.cols = cols

    def set(self, key, value):
        """Set the value at (row, col) to the given value."""
        # TODO
        if value == self.default:
            self.data.delete(key)
        else:
            self.data.set(key, value)
    

    def get(self, key):
        """Get the value at (row, col)."""
        # TODO
        return self.data.get(key, self.default)

    def items(self):
        """Return an iterable of (row, col, value) for all non-default entries."""
        # TODO
        return self.data.items()

    def __len__(self):
        """Return the number of non-default entries in the matrix."""
        # TODO
        return len(self.data)

    def multiply(self, other):
        """Return the product of this matrix with another matrix."""
        # TODO
        result = SparseMatrix(self.rows, other.cols, self.default)

        for (r1, c1), v1 in self.data.items():
            for (r2, c2), v2 in other.data.items():
                if c1 == r2:
                    key = (r1, c2)
                    result.set(key, result.get(key) + v1 * v2)

        return result

    def __str__(self):
        """Return a string representation of the matrix."""
        # TODO
        if self.rows is None or self.cols is None:
            return " "
        for row in range(self.rows):
            row_values = ArrayList()
            for col in range(self.cols):
                row_values.append(self.get((row, col)))
            return str(row_values)
