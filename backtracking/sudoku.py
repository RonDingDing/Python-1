"""
Given a partially filled 9×9 2D array, the objective is to fill a 9×9
square grid with digits numbered 1 to 9, so that every row, column, and
and each of the nine 3×3 sub-grids contains all of the digits.

This can be solved using Backtracking and is similar to n-queens.
We check to see if a cell is safe or not and recursively call the
function on the next column to see if it returns True. if yes, we
have solved the puzzle. else, we backtrack and place another number
in that cell and repeat this process.
"""
from typing import List, Optional, Tuple, Union

Matrix = List[List[int]]

# assigning initial values to the grid
initial_grid: Matrix = [
    [3, 0, 6, 5, 0, 8, 4, 0, 0],
    [5, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0],
]

initial_not_solvable_grid: Matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


# a grid with no solution
no_solution: Matrix = [
    [5, 0, 6, 5, 0, 8, 4, 0, 3],
    [5, 2, 0, 0, 0, 0, 0, 0, 2],
    [1, 8, 7, 0, 0, 0, 0, 3, 1],
    [0, 0, 3, 0, 1, 0, 0, 8, 0],
    [9, 0, 0, 8, 6, 3, 0, 0, 5],
    [0, 5, 0, 0, 9, 0, 6, 0, 0],
    [1, 3, 0, 0, 0, 0, 2, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    [0, 0, 5, 2, 0, 6, 3, 0, 0],
]


def is_safe(grid: Matrix, row: int, column: int, n: int) -> bool:
    """
    This function checks the grid to see if each row,
    column, and the 3x3 subgrids contain the digit 'n'.
    It returns False if it is not 'safe' (a duplicate digit
    is found) else returns True if it is 'safe' or 0.
    """
    if n == 0:
        return True

    elif n < 0 or n > 9 or (not isinstance(n, int)):
        return False

    for i in range(9):
        if (grid[row][i] == n and i != column) or (grid[i][column] == n and i != row):
            return False

    for i in range(3):
        for j in range(3):
            new_row = (row - row % 3) + i
            new_column = (column - column % 3) + j
            if (
                new_row != row
                and new_column != column
                and grid[new_row][new_column] == n
            ):
                return False

    return True


def is_completed(grid: Matrix) -> bool:
    """
    This function checks if the puzzle is completed or not.
    it is completed when all the cells are assigned with a non-zero number.

    >>> is_completed([[0]])
    False
    >>> is_completed([[1]])
    True
    >>> is_completed([[1, 2], [0, 4]])
    False
    >>> is_completed([[1, 2], [3, 4]])
    True
    >>> is_completed(initial_grid)
    False
    >>> is_completed(no_solution)
    False
    """
    return all(all(cell != 0 for cell in row) for row in grid)


def find_empty_location(grid: Matrix) -> Optional[Tuple[int, int]]:
    """
    This function finds an empty location so that we can assign a number
    for that particular row and column.
    """
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None


def check_original_solvable(grid: Matrix) -> bool:
    """
    This function checks whether the original grid provided is solvable.

    >>> check_original_solvable(initial_not_solvable_grid)
    False
    >>> check_original_solvable(no_solution)
    False
    """
    for original_row in range(9):
        for origin_col in range(9):
            origin_digit = grid[original_row][origin_col]
            if origin_digit:
                if not is_safe(grid, original_row, origin_col, origin_digit):
                    return False
    return True


def sudoku_solve(grid: Matrix) -> Union[Matrix, bool]:
    """
    Takes a partially filled-in grid and attempts to assign values to
    all unassigned locations in such a way to meet the requirements
    for Sudoku solution (non-duplication across rows, columns, and boxes)
    """

    if is_completed(grid):
        return grid

    row, column = find_empty_location(grid)

    for digit in range(1, 10):
        if is_safe(grid, row, column, digit):
            grid[row][column] = digit

            if sudoku_solve(grid):
                return grid

            grid[row][column] = 0

    return False


def print_grid(grid: Optional[Matrix]) -> None:
    """
    A function to print the solution in the form
    of a 9x9 grid
    """
    if grid:
        for row in grid:
            for cell in row:
                print(cell, end=" ")
            print()


def sudoku(grid: Matrix) -> Optional[Matrix]:
    """
    Find the solution of a sudoku.
    """

    if not check_original_solvable(grid):
        return None
    return sudoku_solve(grid)


if __name__ == "__main__":
    # make a copy of grid so that you can compare with the unmodified grid
    for example_grid in (
        initial_grid,
        no_solution,
        initial_not_solvable_grid,
    ):
        print("\nExample grid:\n" + "=" * 20)
        print_grid(example_grid)
        print("\nExample grid solution:")
        solution = sudoku(example_grid)
        if solution:
            print_grid(solution)
        else:
            print("Cannot find a solution.")
