from typing import Tuple

import numpy as np

from enums import *
from game_grid import GameGrid


class CPU():

    def __init__(self, grid) -> None:
        self.__grid: GameGrid = grid


    def __choose_cell(self, axis, pos) -> Tuple:
        grid = self.__grid

        row = None
        col = None

        # axis can be 0 -> row, 1 -> col, 2 -> diagonal
        # [row_0, row_1,  row_2]
        # [col_0, col_1,  col_2]
        # [diag, antidiag, 0]
        if axis == SumGridMappings.ROW.value:
            row = pos
            for i in range(grid.grid_size):
                if grid.grid[row][i] == GameEntity.NOBODY.value:
                    col = i
                    break

        if axis == SumGridMappings.COL.value:
            col = pos
            for i in range(grid.grid_size):
                if grid.grid[i][col] == GameEntity.NOBODY.value:
                    row = i
                    break

        if axis == SumGridMappings.DIAG.value:
            for i in range(grid.grid_size):
                if grid.grid[i][i] == GameEntity.NOBODY.value:
                    row = i
                    col = i
                    break

        return (row, col)


    def get_move(self):
        grid = self.__grid
        move = None

        # Win, if CPU can
        CPU_winning_score = grid.grid_size * GameEntity.CPU.value
        moves = np.where(grid.sums_grid == CPU_winning_score - GameEntity.CPU.value)
        candidate_moves = [(axis, pos) for axis, pos in zip(moves[0], moves[1])]
        if len(candidate_moves) > 0:
            row, col = candidate_moves[0]
            #move = self.__choose_cell(row, col)
            

        # Block User from winning
        user_winning_score = grid.grid_size * GameEntity.USER.value
        moves = np.where(grid.sums_grid == user_winning_score - GameEntity.USER.value)
        candidate_moves = [(axis, pos) for axis, pos in zip(moves[0], moves[1])]
        if len(candidate_moves) > 0:
            row, col = candidate_moves[0]
            move = self.__choose_cell(row, col)

        # Take middle spot if open
        mid = grid.grid_size // 2
        if grid.grid[mid][mid] == GameEntity.NOBODY.value:
            move = (mid, mid)

        # Maximize CPU score
        CPU_winning_score = grid.grid_size * GameEntity.CPU.value
        moves = np.where(grid.sums_grid == CPU_winning_score - GameEntity.CPU.value)
        candidate_moves = [(axis, pos) for axis, pos in zip(moves[0], moves[1])]
        if len(candidate_moves) > 0:
            row, col = candidate_moves[0]
            move = self.__choose_cell(row, col)
        
        return move

