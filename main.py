from snake_game.snake_game import SnakeGame

class Main:
    
    def __init__(self):
        self.snake_game = SnakeGame()

if __name__ == '__main__':
    main = Main()
    main.snake_game.run_game()