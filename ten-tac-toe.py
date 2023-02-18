import numpy as np
from enum import Enum


class CellAssignment(Enum):
    CPU = -1
    EMPTY = 0
    USER = 1


class GameGrid():

    def __init__(self, grid_dimensions=3) -> None:

        if grid_dimensions % 2 != 1:
            raise Exception('Grid size must be odd.')

        self.grid_size = grid_dimensions
        self.grid: np.array = self.__initialize_grid(grid_dimensions)
        self.sums_grid: np.array = self.__initialize_grid(grid_dimensions)
        self.mean_grid: np.array = self.__initialize_grid(grid_dimensions)

    def __initialize_grid(self, grid_dimensions=3) -> np.array:
        return np.zeros((grid_dimensions, grid_dimensions), dtype=int)

    def __str__(self) -> str:
        rows = ['  {} | {} | {}  \n'.format(*row) for row in self.grid]
        horizontal_sep = '----+---+----\n'
        return horizontal_sep.join(rows)

    def __update_grid_stats(self) -> None:
        # sums array of the game board as follows:
        # [row0, row1,  row2]
        # [col0, col1,  col2]
        # [diag, antidiag, 0]
        sums = np.zeros((self.grid_size, self.grid_size), dtype=int)
        sums[0] = self.grid.sum(axis=0)
        sums[1] = self.grid.sum(axis=1)
        sums[2][0] = np.sum(self.grid.diagonal())
        sums[2][1] = np.sum(np.fliplr(self.grid).diagonal())

        self.sums_grid = sums
        self.mean_grid = sums/self.grid_size

    def update_cell(self, cell_number: int, cell_value: int) -> None:
        if type(cell_number) != int or cell_number < 1 or cell_number > self.grid_size ** 2:
            raise Exception('Invalid input cell selection input.')

        cell_number -= 1
        row, col = divmod(cell_number, self.grid_size)
        row = self.grid_size - 1 - row
        col = col

        if self.grid[row][col] != CellAssignment.EMPTY.value:
            raise Exception('Selected cell already occupied.')

        self.grid[row][col] = cell_value
        self.__update_grid_stats()

    def determine_winner(self) -> int:
        # Draw is 0
        # User is 1
        # CPU  is -1
        winner = 0
        winner += int(np.any(self.mean_grid == CellAssignment.USER.value))
        winner -= int(np.any(self.mean_grid == CellAssignment.CPU.value))
        return winner

    def is_game_over(self) -> bool:
        return np.all(self.grid != CellAssignment.EMPTY.value)


class CPU():

    def __init__(self, grid) -> None:
        self.__grid: GameGrid = grid

    def get_move(self):  # -> Tuple(int, int):
        mid = self.__grid.grid_size // 2
        if self.__grid[mid][mid] == CellAssignment.EMPTY.value:
            return (mid, mid)


class GameManager():

    def __init__(self, grid, cpu) -> None:
        self.__grid = grid
        self.display_grid()

    def clear_display(self):
        print("\033[H\033[J", end="")

    def display_header(self):
        print('***** TEN! TAC! TOE! *****\n')

    def display_grid(self):
        print(self.__grid)

    def get_user_input(self, prompt: str, expected_type=str):
        user_input = None
        while not user_input:
            try:
                user_input = expected_type(input(prompt))
            except ValueError:
                print('Invalid input type.')
        return user_input

    def run(self):
        self.clear_display()
        self.display_header()

        symbol = self.get_user_input('Would you like to be X or O? ')

        while not self.__grid.is_game_over():
            selection = int(input('Select a cell to place X: '))
            self.__grid.update_cell(selection, CellAssignment.USER.value)

            self.clear_display()
            self.display_header()
            self.display_grid()


if __name__ == '__main__':
    grid = GameGrid()
    cpu = CPU(grid)
    game = GameManager(grid, cpu)
    game.run()
