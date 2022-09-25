"""
Matrix ADT, ** only implemented for square matrices **
"""
from typing import List


class Matrix:
    """
    2D list implementation of a matrix each element of the instance attribute:
    'matrix' contains a row

    Instance Attributes:
        - rows: number of rows
        - columns: number of columns
        - Matrix: the 2D list that holds the entries

    Representation Invariants:
        - rows > 0
        - columns > 0

    # Example initialization: Matrix(3, 3)
    """
    rows: int
    columns: int
    matrix: List[List]

    def __init__(self, row: int, column: int) -> None:
        """
        Initialize a new empty matrix of a specified dimension
        """
        self.rows = row
        self.columns = column
        self.matrix = []

    def set_matrix(self, matrix: List[List]) -> None:
        """
        change the matrix instance attribute

        Preconditions:
            - all([len(matrix[i]) == self.columns for i in matrix])
            - len(matrix[i]) == rows
        """
        self.matrix = matrix

    def add_multiple_of_row(self, row_add: int, row_added: int, multiple: float,
                            matrix: List[list]) -> List[List]:
        """
        Elementary row operation, add a multiple of one row to another
        the rows are the list indices

        row_add is the row to add
        row_added is the row being added to

        Preconditions:
            - 0 <= row_add < len(matrix)
            - 0 <= row_added < len(matrix)
            - row_add != row_added

        >>> matrix_test = Matrix(3, 3)
        >>> matrix_test.set_matrix([[2, 3, 4], [5, 2, 1], [-2, -3, 4]])
        >>> matrix_test.add_multiple_of_row(0, 1, 2, matrix_test.matrix)
        [[2, 3, 4], [9, 8, 9], [-2, -3, 4]]
        """
        for entry in range(0, self.columns):
            matrix[row_added][entry] += multiple * matrix[row_add][entry]

        return matrix

    def solve(self, constants: List[float]) -> List[float]:
        """
        Solve a square matrix for a given list of constants by row reduction
        Output is the list of variables corresponding to the order of the columns

        Preconditions:
            - len(constants) == len(self.matrix)

       * Assumes that the Matrix has a unique solution *

        >>> matrix_test = Matrix(3, 3)
        >>> matrix_test.set_matrix([[2, -4, 5], [4, -1, 0], [-2, 2, -3]])
        >>> matrix_test.solve([-33, -5, 19])
        [-0.5, 3.0, -4.0]
        """
        matrix = list.copy(self.matrix)

        # Puts the matrix in row echelon form
        for column in range(0, self.columns):

            for row in range(column + 1, self.rows):
                if matrix[column][column] != 0:
                    multiple = matrix[row][column] / - matrix[column][column]
                    matrix = self.add_multiple_of_row(column, row, multiple, matrix)
                    constants[row] = constants[row] + multiple * constants[column]

        # Puts the matrix in reduced row echelon form (except the pivots are not one)
        for column in range(self.columns - 1, 0, -1):

            for row in range(column - 1, -1, -1):
                if matrix[column][column] != 0:
                    multiple = -matrix[row][column] / matrix[column][column]
                    matrix = self.add_multiple_of_row(column, row, multiple, matrix)
                    constants[row] = constants[row] + multiple * constants[column]

        # Makes the pivots 1
        for column in range(0, self.columns):
            constants[column] = constants[column] / matrix[column][column]

        return constants


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)
