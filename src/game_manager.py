from time import sleep
from typing import Tuple

import numpy as np

from enums import *


class GameManager():

    def __init__(self, grid, cpu) -> None:
        self.__grid = grid
        self.__cpu = cpu

        self.player_symbol = self.__get_player_symbol()
        self.cpu_symbol = GameSymbol.O if self.player_symbol == GameSymbol.X else GameSymbol.X

        self.__display_grids = {
            GameEntity.NOBODY:  np.flipud(np.arange(1, 10, dtype=int).reshape(3, 3)),
            GameEntity.USER:    np.full(shape=(3, 3), fill_value=self.player_symbol.name),
            GameEntity.CPU:     np.full(
                shape=(3, 3), fill_value=self.cpu_symbol.name)
        }

    def clear_display(self):
        print("\033[H\033[J", end="")

    def display_header(self):
        print('***** TEN! TAC! TOE! *****\n')

    def display_grid(self):
        side_padding = 8
        grid_to_display = self.__display_grids[GameEntity.NOBODY]
        grid_to_display = np.where(self.__grid.grid == GameEntity.USER.value, self.__display_grids[GameEntity.USER], grid_to_display)
        grid_to_display = np.where(self.__grid.grid ==  GameEntity.CPU.value,  self.__display_grids[GameEntity.CPU], grid_to_display)
        rows = [' '*side_padding + '{} | {} | {}  \n'.format(*row) for row in grid_to_display]
        horizontal_sep = ' '*(side_padding-2) + '----+---+----\n'
        print(horizontal_sep.join(rows))

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

    def __cell_num_to_index(self, cell_number: int) -> Tuple[int, int]:
        grid_size = self.__grid.grid_size
        row, col = divmod(cell_number - 1, grid_size)
        row = grid_size - 1 - row
        return (row, col)

    def __index_to_cell_num(self, index: Tuple[int, int]) -> int:
        grid_size = self.__grid.grid_size
        row, col = index
        return grid_size * (grid_size - row - 1) + (col+1)

    def run(self):
        self.clear_display()
        self.display_header()
        self.display_grid()

        turns_played = 0
        turn = GameEntity.USER if self.player_symbol == GameSymbol.X else GameEntity.CPU
        while not self.__grid.is_game_over():
            if turn == GameEntity.USER:
                selection = int(input(f'Select a cell to place {self.player_symbol.name}: '))
                row, col = self.__cell_num_to_index(selection)
                self.__grid.update_cell(row, col, GameEntity.USER.value)
                turn = GameEntity.CPU
            elif turn == GameEntity.CPU:
                print('CPU is thinking...')
                row, col = self.__cpu.get_move()
                sleep(turns_played / 4)
                self.__grid.update_cell(row, col, GameEntity.CPU.value)
                turn = GameEntity.USER
                print(f'{GameEntity.CPU.name} put {self.cpu_symbol.name} in {self.__index_to_cell_num((row, col))}')
                sleep(1)

            turns_played += 1
            self.clear_display()
            self.display_header()
            self.display_grid()

        winner: GameEntity = self.__grid.determine_winner()
        print(f'{winner.name} won!')
