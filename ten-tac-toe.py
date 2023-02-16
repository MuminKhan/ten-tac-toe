import numpy as np

class GameGrid():

    def __init__(self, grid_dimensions=3) -> None:
        self._dimensions = grid_dimensions
        self._grid: np.array = self.__initialize(grid_dimensions)

    def __initialize(self, grid_dimensions=3) -> np.array:
        return np.zeros((grid_dimensions, grid_dimensions), dtype=int)

    def __str__(self) -> str:
        rows = ['  {} | {} | {}  \n'.format(*row) for row in self._grid]
        horizontal_sep = '----+---+----\n'
        return horizontal_sep.join(rows)


if __name__ == '__main__':
    grid = GameGrid()
    print(grid)
