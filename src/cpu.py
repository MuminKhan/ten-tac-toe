from typing import Tuple

import numpy as np

from enums import *
from game_grid import GameGrid


class CPU():

    def __init__(self, grid) -> None:
        self.__grid: GameGrid = grid

    def __choose_cell(self, axis, pos) -> Tuple:
        grid = self.__grid
        open_slots = np.ma.masked_array(grid.grid == 0)

        row = None
        col = None
        if axis == SumGridMappings.ROW.value:
            row = pos
            col = np.where(open_slots[row] == True)
            col = col[0][0]
        elif axis == SumGridMappings.COL.value:
            row, _ = np.where(open_slots[:axis] == True)
            row = row[0]
            col = pos
        elif axis == SumGridMappings.DIAG.value:
            diag_mask = np.zeros_like(grid.grid, dtype=bool)
            np.fill_diagonal(diag_mask, val=True)
            if pos:
                diag_mask = np.fliplr(diag_mask)
            row, col = np.argwhere(diag_mask * open_slots)[0]

        return (row, col)

    def get_move(self) -> Tuple[int, int]:
        grid = self.__grid

        user_winning_score = grid.grid_size * GameEntity.USER.value
        CPU_winning_score = grid.grid_size * GameEntity.CPU.value

        # CPU Wins
        targets = list(np.argwhere(grid.sums_grid == CPU_winning_score - GameEntity.CPU.value))
        # Block User Win
        targets += list(np.argwhere(grid.sums_grid == user_winning_score - GameEntity.USER.value))
        if len(targets) > 0:
            return self.__choose_cell(*targets[0])

        # Take middle spot
        mid = grid.grid_size // 2
        if grid.grid[mid][mid] == GameEntity.NOBODY.value:
            return (mid, mid)

        # Greedy on row / cols
        NotImplementedError('Strategy not implemented yet...')

        # Take any available corner spot
        NotImplementedError('Strategy not implemented yet...')
