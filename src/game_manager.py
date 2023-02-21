from typing import Tuple

from enums import *


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
        rows = []
        for i in range(self.__grid.grid_size-1, -1, -1):
            cells = [n for n in range((3*i)+1, (3*i)+4)]
            rows.append('  {} | {} | {}  \n'.format(*cells))
        horizontal_sep = '----+---+----\n'
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

        winner:GameEntity = self.__grid.determine_winner()
        print(f'{winner.name.title()} won!')
