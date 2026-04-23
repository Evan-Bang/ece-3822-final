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

Author: Owen Ringrose
Date:   4/3/2026
Lab:    Lab 6 - Sparse World Map
"""

from .hash_table import HashTable

# =============================================================================
# Do not modify SparseMatrixBase.
# =============================================================================

class SparseMatrixBase:
    """Interface definition. Your SparseMatrix must inherit from this."""

    def __init__(self, rows=None, cols=None, default=0):
        self.rows    = rows
        self.cols    = cols
        self.default = default

    def set(self, row, col, value):
        raise NotImplementedError

    def get(self, row, col):
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
        super().__init__(rows, cols, default)
        self.coordinate_hash = HashTable()
        
    def set(self, row, col, value):
        """
        Set a value at the provided coordinates
        Args:
         value: row: row coordinate
                col: collumn coordinate
                value: value at coordinate
        """
        coordinate = (row, col)
        self.coordinate_hash.set(coordinate, value)
        if value == self.default:
            self.coordinate_hash.delete(coordinate)

    def get(self, row, col):
        """
        Get the value at a coordinate
        Args:
            row: row coordinate
            col: collumn coordinate
        returns:
            value: value at the coordinate
            returns None if no value at coordinate
        """
        coordinate = (row, col)
        return self.coordinate_hash.get(coordinate, self.default)

    def items(self):
        """Returns all of the key value pairs in the matrix"""
        return self.coordinate_hash.items()

    def __len__(self):
        """Returns the number of non-default entries in the matrix"""
        return len(self.coordinate_hash)

    def multiply(self, other):
        """Multiplies this matrix with another matrix, returns a new matrix"""
        if not isinstance(other, SparseMatrix):
            raise TypeError("Can only multiply with another SparseMatrix")
        if self.cols != other.rows:
            raise ValueError("Incompatible dimensions for multiplication")
        
        result = SparseMatrix(rows=self.rows, cols=other.cols, default=self.default)
        
        # Matrix multiplication loop, I think this can be done more efficiently since this is a sparse matrix
        for (row, col), value, in self.items():
            for k in range(other.cols):
                other_value = other.get(col, k)
                if other_value != other.default:
                    result_value = result.get(row,k)
                    result.set(row, k, result_value + value * other_value)
        
        return result

    def __str__(self):
        """Return a string representation of the matrix"""
        return f"{self.items()}"
