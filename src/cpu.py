from typing import Tuple

import numpy as np

from enums import *
from game_grid import GameGrid


class CPU():

    def __init__(self, grid) -> None:
        self.__grid: GameGrid = grid

    def __find_open_cell(self, axis, pos) -> Tuple:
        grid = self.__grid
        open_spots_mask = np.ma.masked_array(grid.grid == 0)

        row = None
        col = None
        if axis == SumGridMappings.ROW.value:
            spots = np.where(open_spots_mask[pos] == True)
            if len(spots) > 0 and len(spots[0]) > 0:
                row = pos
                col = spots[0][0]
        elif axis == SumGridMappings.COL.value:
            spots = np.where(open_spots_mask[:, pos] == True)
            if len(spots) > 0 and len(spots[0]) > 0:
                row = spots[0][0]
                col = pos
        elif axis == SumGridMappings.DIAG.value:
            diag_mask = np.zeros_like(grid.grid, dtype=bool)
            np.fill_diagonal(diag_mask, val=True)
            if pos == 1:
                diag_mask = np.fliplr(diag_mask)
            spots = np.argwhere(diag_mask * open_spots_mask)
            if len(spots) > 0 and len(spots[0]) > 0:
                row, col = spots[0]

        return (row, col)

    def get_move(self) -> Tuple[int, int]:
        moves = []
        grid = self.__grid

        user_winning_score = grid.grid_size * GameEntity.USER.value
        CPU_winning_score  = grid.grid_size * GameEntity.CPU.value

        # CPU Wins / Block User Win
        targets = list(np.argwhere(grid.sums_grid == CPU_winning_score - GameEntity.CPU.value))
        targets += list(np.argwhere(grid.sums_grid == user_winning_score - GameEntity.USER.value))
        for target in targets:
            move = self.__find_open_cell(*target)
            moves.append(move)

        # Take middle spot
        mid = grid.grid_size // 2
        if grid.grid[mid][mid] == GameEntity.NOBODY.value:
            move = (mid, mid)
            moves.append(move)

        # Greedy on row / cols
        targets =  list(np.argwhere(grid.sums_grid == GameEntity.CPU.value))
        targets += list(np.argwhere(grid.sums_grid == GameEntity.NOBODY.value))
        targets += list(np.argwhere(grid.sums_grid == GameEntity.USER.value))
        for target in targets:
            move = self.__find_open_cell(*target)
            moves.append(move)

        # Return highest priority valid move
        for move in moves:
            if None not in move:
                return move
