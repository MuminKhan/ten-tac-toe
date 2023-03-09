from cpu import CPU
from game_grid import GameGrid
from game_manager import GameManager


def main():
    play_again = True
    while play_again:
        grid = GameGrid()
        cpu = CPU(grid)
        game = GameManager(grid, cpu)
        game.run()
        play_again = game.play_again()


if __name__ == '__main__':
    try:
        main()
    except: 
        print('Something went really wrong. Exiting...')
        raise

