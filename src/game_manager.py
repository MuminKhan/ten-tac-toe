from time import sleep
from typing import Tuple

import numpy as np

from cpu import CPU
from enums import *
from game_grid import GameGrid


class GameManager():

    def __init__(self, grid, cpu) -> None:
        self.__grid: GameGrid = grid
        self.__cpu: CPU  = cpu

        self.__player_symbol: GameSymbol = None
        self.__cpu_symbol:    GameSymbol = None
        self.__display_grids: dict[GameEntity: np.ndarray] = None

        self.__initialize_game_objects()


    def __initialize_game_objects(self):
        grid_size = self.__grid.grid_size

        self.__clear_display()
        self.__display_header()
        self.__player_symbol = self.__get_player_symbol()
        self.__cpu_symbol = GameSymbol.O if self.__player_symbol == GameSymbol.X else GameSymbol.X
        self.__display_grids = {
            GameEntity.NOBODY:  np.flipud(np.arange(1, (grid_size**2)+1, dtype=int).reshape(grid_size, grid_size)),
            GameEntity.USER:    np.full(shape=(grid_size, grid_size), fill_value=self.__player_symbol.name),
            GameEntity.CPU:     np.full(shape=(grid_size, grid_size), fill_value=self.__cpu_symbol.name)
        }
        self.__display_grid()

    def __clear_display(self):
        print("\033[H\033[J", end="")

    def __display_header(self):
        print('******* TEN! TAC! TOE! *******\n')

    def __display_grid(self):
        side_padding = 10
        grid_to_display = self.__display_grids[GameEntity.NOBODY]
        grid_to_display = np.where(self.__grid.grid == GameEntity.USER.value, self.__display_grids[GameEntity.USER], grid_to_display)
        grid_to_display = np.where(self.__grid.grid ==  GameEntity.CPU.value,  self.__display_grids[GameEntity.CPU], grid_to_display)
        rows = [' '*side_padding + '{} | {} | {}  \n'.format(*row) for row in grid_to_display]
        horizontal_sep = ' '*(side_padding-2) + '----+---+----\n'
        print(horizontal_sep.join(rows))

    def __full_display(self):
        self.__clear_display()
        self.__display_header()
        self.__display_grid()

    def __get_user_input(self, prompt: str, expected_type=str):
        user_input = None
        while not user_input:
            try:
                user_input = expected_type(input(prompt))
            except ValueError:
                print('Invalid input type.')
        return user_input

    def __get_player_symbol(self):
        user_symbol = None
        available_symbols = {symbol.name for symbol in GameSymbol}
        while user_symbol is None:
            symbol = self.__get_user_input('Would you like to be X or O? ').upper()

            if len(symbol) > 0 and symbol[0] in available_symbols:
                user_symbol = GameSymbol.X if len(symbol) > 0 and symbol[0] == GameSymbol.X.name else GameSymbol.O

        return user_symbol

    def play_again(self):
        play_again = None
        while play_again is None:
            user_answer = self.__get_user_input('Would you like to play again (y/n)? ').lower()
            if len(user_answer) <= 0:
                continue
            play_again = user_answer[0] == 'y' 
            print(user_answer, play_again)

        return play_again

    def __cell_num_to_index(self, cell_number: int) -> Tuple[int, int]:
        grid_size = self.__grid.grid_size
        row, col = divmod(cell_number - 1, grid_size)
        row = grid_size - 1 - row
        return (row, col)

    def __index_to_cell_num(self, index: Tuple[int, int]) -> int:
        grid_size = self.__grid.grid_size
        row, col = index
        return grid_size * (grid_size - row - 1) + (col+1)
    
    def __determine_winner(self) -> int:
        mean_grid = self.__grid.sums_grid / self.__grid.grid_size
        winner = GameEntity.NOBODY.value
        winner += int(np.any(mean_grid == GameEntity.USER.value))
        winner -= int(np.any(mean_grid == GameEntity.CPU.value))
        return GameEntity(winner)

    def __is_game_over(self) -> bool:
        return np.all(self.__grid.grid != GameEntity.NOBODY.value) or np.any(np.abs(self.__grid.sums_grid) == self.__grid.grid_size)

    def run(self):
        """Runs the Ten-Tac-Toe game"""
        turns_played = 0
        turn = GameEntity.USER if self.__player_symbol == GameSymbol.X else GameEntity.CPU
        while not self.__is_game_over():
            self.__full_display()

            # User's turn
            if turn == GameEntity.USER:
                try: 
                    selection = int(input(f'Select a cell to place {self.__player_symbol.name}: '))
                    row, col = self.__cell_num_to_index(selection)
                    self.__grid.update_cell(row, col, GameEntity.USER.value)
                except Exception:
                    print('Invalid Selection! Please choose an empty grid number...')
                    sleep(1)
                    continue
                turn = GameEntity.CPU

            # CPU's turn
            elif turn == GameEntity.CPU:
                print('CPU is thinking...')
                row, col = self.__cpu.get_move()
                sleep(turns_played / 4)
                self.__grid.update_cell(row, col, GameEntity.CPU.value)
                turn = GameEntity.USER
                print(f'{GameEntity.CPU.name} put {self.__cpu_symbol.name} in {self.__index_to_cell_num((row, col))}')
                sleep(1)

            turns_played += 1
        
        # End Game
        self.__full_display()
        winner: GameEntity = self.__determine_winner()
        print(f'{winner.name} won!')
