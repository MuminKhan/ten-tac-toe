from enum import Enum, auto
from typing import Tuple

import numpy as np


class GameEntity(Enum):
    CPU = -1
    NOBODY = 0
    USER = 1


class GameSymbol(Enum):
    X = auto()
    O = auto()


class GameGrid():

    def __init__(self, grid_dimensions=3) -> None:

        if grid_dimensions % 2 != 1:
            raise Exception('Grid size must be odd.')

        self.grid_size = grid_dimensions
        self.grid: np.array = self.__initialize_grid(grid_dimensions)
        self.sums_grid: np.array = self.__initialize_grid(grid_dimensions)

    def __initialize_grid(self, grid_dimensions=3) -> np.array:
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
        sums[0] = self.grid.sum(axis=0)
        sums[1] = self.grid.sum(axis=1)
        sums[2][0] = np.sum(self.grid.diagonal())
        sums[2][1] = np.sum(np.fliplr(self.grid).diagonal())
        return sums

    def update_cell(self, row: int, col: int, cell_value: int) -> None:
        if self.grid[row][col] != GameEntity.NOBODY.value:
            raise Exception('Selected cell already occupied.')

        self.grid[row][col] = cell_value
        self.sums_grid = self.__compute_sums_of_grid()

    def determine_winner(self) -> int:
        mean_grid = self.sums_grid / self.grid_size
        winner = GameEntity.NOBODY.value
        winner += int(np.any(mean_grid == GameEntity.USER.value))
        winner -= int(np.any(mean_grid == GameEntity.CPU.value))
        return GameEntity(winner)

    def is_game_over(self) -> bool:
        return np.all(self.grid != GameEntity.NOBODY.value) or np.any(np.abs(self.sums_grid) == self.grid_size)


class CPU():

    def __init__(self, grid) -> None:
        self.__grid: GameGrid = grid

    def get_move(self):
        mid = self.__grid.grid_size // 2
        if self.__grid[mid][mid] == GameEntity.NOBODY.value:
            return (mid, mid)


class GameManager():

    def __init__(self, grid, cpu) -> None:
        self.__grid = grid
        self.__cpu = cpu

        self.player_symbol = self.__get_player_symbol()
        self.cpu_symbol = GameSymbol.O if self.player_symbol == GameSymbol.X else GameSymbol.X

    def clear_display(self):
        print("\033[H\033[J", end="")

    def display_header(self):
        print('***** TEN! TAC! TOE! *****\n')

    def display_grid(self):
        print(self.__grid)

    def __get_user_input(self, prompt: str, expected_type=str):
        user_input = None
        while not user_input:
            try:
                user_input = expected_type(input(prompt))
            except ValueError:
                print('Invalid input type.')
        return user_input

    def __get_player_symbol(self):
        symbol = self.__get_user_input('Would you like to be X or O? ').upper()
        return GameSymbol.X if len(symbol) > 0 and symbol[0] == GameSymbol.X.name else GameSymbol.O

    def __cell_to_row_col(self, cell_number: int) -> Tuple[int, int]:
        grid_size = self.__grid.grid_size
        if type(cell_number) != int or cell_number < 1 or cell_number > grid_size ** 2:
            raise Exception('Invalid input cell selection input.')
        cell_number -= 1
        row, col = divmod(cell_number, grid_size)
        row = grid_size - 1 - row
        return (row, col)

    def run(self):
        self.clear_display()
        self.display_header()
        self.display_grid()

        turn = GameEntity.USER if self.player_symbol == GameSymbol.X else GameEntity.CPU
        while not self.__grid.is_game_over():
            if turn == GameEntity.USER:
                selection = int(input('Select a cell to place X: '))
                row, col = self.__cell_to_row_col(selection)
                self.__grid.update_cell(row, col, GameEntity.USER.value)
                turn = GameEntity.CPU
            elif turn == GameEntity.CPU:
                row, col = self.__cpu.get_move()
                self.__grid.update_cell(row, col, GameEntity.CPU.value)
                turn = GameEntity.USER

            self.clear_display()
            self.display_header()
            self.display_grid()

        winner = self.__grid.determine_winner()
        if winner == GameEntity.USER:
            winner = 'You'
        elif winner == GameEntity.CPU:
            winner = 'CPU'
        else:
            winner = 'No one'
        print(f'{winner} won!')


if __name__ == '__main__':
    grid = GameGrid()
    cpu = CPU(grid)
    game = GameManager(grid, cpu)
    game.run()
