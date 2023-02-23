from cpu import CPU
from game_grid import GameGrid
from game_manager import GameManager


def main():
    grid = GameGrid()
    cpu = CPU(grid)
    game = GameManager(grid, cpu)
    game.run()


if __name__ == '__main__':
    try:
        main()
    except: 
        print('Something went really wrong. Exiting...')

