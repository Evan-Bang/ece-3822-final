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

Author: Emmanuel Morales
Date:   April 9, 2026
Lab:    Lab 6 - Sparse World Map
"""

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
        """
        Initializes a new SparseMatrix with the given dimensions and default value.
        Args:
            rows (int): The number of rows in the matrix.
            cols (int): The number of columns in the matrix.
            default (int, optional): The default value for unspecified entries. Defaults to 0.
        """
        self.matrix = ArrayList()
        self.size = 0

    def set(self, row, col, value):
        """
        Sets the value at the specified row and column.
        If the value is equal to the default, the entry is removed.
        The number of rows and columns is updated if the new entry exceeds current dimensions.

        Args:
            row (int): The row index.
            col (int): The column index.
            value (int): The value to set.
        """
        # Search for existing entry at (row, col), and update or remove it as needed
        for i in range(len(self.matrix)):
            row_i, col_i, val_i = self.matrix[i]
            if row_i == row and col_i == col:
                if value == self.default:
                    self.matrix.pop(i)
                    self.size -= 1
                else:
                    self.matrix[i] = (row, col, value)
                return
        # If there was no pre-existing entry and value is not default, add a new entry
        if value != self.default:
            self.matrix.append((row, col, value))
            self.size += 1
            # Update the number of rows and cols if needed
            if self.rows is None or row + 1 > self.rows:
                self.rows = row + 1
            if self.cols is None or col + 1 > self.cols:
                self.cols = col + 1

    def get(self, row, col):
        """
        Retrieves the value at the specified row and column.
        Args:
            row (int): The row index.
            col (int): The column index.
        Returns:
            int: The value at the specified position, or the default if not set.
        """
        for i in range(len(self.matrix)):
            row_i, col_i, val_i = self.matrix[i]
            if row_i == row and col_i == col:
                return val_i
        return self.default

    def items(self):
        """
        Returns an iterator over the non-default entries in the sparse matrix, 
        where each entry is returned as a tuple: ((row, col), value).
        """
        for i in range(len(self.matrix)):
            row_i, col_i, val_i = self.matrix[i]
            yield ((row_i, col_i), val_i)

    def __len__(self):
        """
        Returns the number of non-default entries in the sparse matrix.

            Returns:
                int: The number of non-default entries currently stored in the matrix
        """
        return self.size

    def multiply(self, other):
        """
        Multiplies this sparse matrix with another sparse matrix.

        Args:
            other (SparseMatrix): The matrix to multiply with.
        
        Returns:
            SparseMatrix: A new sparse matrix representing the product.
        """
        # new SparseMatrix for the results
        result = SparseMatrix(self.rows, other.cols, self.default)
        
        for ((row, col), value) in self.items(): # for each non-default entry in self
            for ((other_row, other_col), other_value) in other.items(): # for each non-default entry in other
                if other_row == col: # when self column matches other row
                    product = value * other_value
                    result_value = result.get(row, other_col)
                    result.set(row, other_col, result_value + product)
        return result

    def __str__(self):
        """
        Returns a string representation of the sparse matrix.

        Returns:
            str: A string showing the number of rows, columns, the default value, and non-default entries.
        """
        # return a string representation of the matrix, showing non-default entries
        matrix_str = f"SparseMatrix(rows={self.rows}, cols={self.cols}, default={self.default}, entries=["
        for i in range(len(self.matrix)):
            row_i, col_i, val_i = self.matrix[i]
            matrix_str += f"(({row_i}, {col_i}), {val_i})"
            if i < (len(self.matrix) - 1):
                matrix_str += ", "
        matrix_str += "])"
        return matrix_str
