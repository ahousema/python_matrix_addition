from random import randint


class Matrix:
    def __init__(self, rows=0, cols=0, data=None):
        self.rows = rows
        self.cols = cols
        self.data = data

    @classmethod
    def from_data(cls, data):
        """Construct matrix from 2D data (array of arrays)."""
        rows = len(data)
        cols = len(data[0])
        return cls(rows, cols, data)

    @classmethod
    def from_size(cls, rows, cols):
        """Construct an empty matrix of the given size."""
        # https://www.geeksforgeeks.org/python-which-is-faster-to-initialize-lists/
        data = [[None for i in range(cols)] for j in range(rows)]
        return cls(rows, cols, data)

    @classmethod
    def from_random(cls, rows, cols, min=1, max=100):
        """Construct a randomized matrix of the given size."""
        data = [[randint(min, max) for c in range(cols)] for r in range(rows)]
        return cls(rows, cols, data)

    def __add__(self, other):
        """Add this matrix to another one with the same dimensions."""
        if self.rows != other.rows or self.cols != other.cols:
            raise RuntimeError("Matrices are not the same size")
        mat_sum = Matrix.from_size(self.rows, self.cols)
        for r in range(self.rows):
            for c in range(self.cols):
                mat_sum.data[r][c] = self.data[r][c] + other.data[r][c]
        return mat_sum

    def __str__(self):
        """Convert matrix to a string."""
        rtn = [f"({self.rows}x{self.cols})"]
        rtn.extend([" ".join([str(val) for val in row]) for row in self.data])
        return "\n".join(rtn)


class MatrixReader:
    def __init__(self, file_name):
        self.fp = open(file_name, "r")
        line = self.fp.readline()
        (self.total_rows, self.total_cols) = [int(val) for val in line.split()]

    def __del__(self):
        self.close()

    def close(self):
        if self.fp is not None:
            self.fp.close()
            self.fp = None

    def read_dimensions(self):
        self.fp.seek(0, 0)
        line = self.fp.readline()
        dimensions = line.split()
        self.close()
        return dimensions

    def read_rows(self, num_rows=None):
        rows = []
        rows_read = 0
        while line := self.fp.readline():
            rows_read += 1
            row = [int(val) for val in line.split()]
            rows.append(row)
            if num_rows is not None and rows_read >= num_rows:
                break
        return rows

    def read_matrix(self, num_rows=None, close=False):
        data = self.read_rows(num_rows)
        if close:
            self.close()
        return Matrix(len(data), self.total_cols, data)


class MatrixWriter:
    def __init__(self, rows, cols, file_name):
        self.fp = open(file_name, "w")
        print(f"{rows} {cols}", file=self.fp)

    def __del__(self):
        self.close()

    def close(self):
        if self.fp is not None:
            self.fp.close()
            self.fp = None

    def write_rows(self, rows):
        """Write rows to the matrix."""
        for row in rows:
            print(" ".join([str(val) for val in row]), file=self.fp)

    def write_matrix(self, matrix, close=False):
        self.write_rows(matrix.data)
        if close:
            self.close()
