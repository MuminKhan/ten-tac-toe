import numpy as np

from enums import *


class GameGrid():

    def __init__(self, grid_dimensions=3) -> None:
        # Proper diagonals cannot be made with even grid lengths. 
        if grid_dimensions % 2 != 1:
            raise Exception('Grid size must be odd.')

        self.grid_size = grid_dimensions
        self.grid: np.array = self.__initialize_grid(grid_dimensions)
        self.sums_grid: np.array = self.__initialize_grid(grid_dimensions)

    def __initialize_grid(self, grid_dimensions) -> np.array:
        return np.zeros((grid_dimensions, grid_dimensions), dtype=int)

    def __str__(self) -> str:
        rows = ['  {} | {} | {}  \n'.format(*row) for row in self.grid]
        horizontal_sep = '----+---+----\n'
        return horizontal_sep.join(rows)

    def __compute_sums_of_grid(self) -> np.ndarray:
        # sums array of the game board as follows:
        # [row0, row1,  row2]
        # [col0, col1,  col2]
        # [diag, antidiag, 0]
        sums = np.zeros((self.grid_size, self.grid_size), dtype=int)
        sums[0] = self.grid.sum(axis=1)
        sums[1] = self.grid.sum(axis=0)
        sums[2][0] = np.sum(self.grid.diagonal())
        sums[2][1] = np.sum(np.fliplr(self.grid).diagonal())
        return sums

    def update_cell(self, row: int, col: int, cell_value: int) -> None:
        if self.grid[row][col] != GameEntity.NOBODY.value:
            raise Exception('Selected cell already occupied.')

        self.grid[row][col] = cell_value
        self.sums_grid = self.__compute_sums_of_grid()
