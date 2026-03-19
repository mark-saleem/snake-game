import pygame
import sys
import random

pygame.init()

h1 = pygame.font.Font(None, 40)
h2 = pygame.font.Font(None, 30)
h3 = pygame.font.Font(None, 20)

title_font = h1
score_font = h2
highscore_font = h2

BLUE = (120, 190, 255)
DARK_BLUE = (20, 30, 90)
RED = (253, 21, 21)

cell_size = 20
number_of_cells = 25

offset = 50

class Food:
    def __init__(self, occupied_positions):
        self.position = self.generate_random_position(occupied_positions)

    def draw(self):
        food_rect = pygame.Rect(offset +self.position[0] * cell_size, offset + self.position[1] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, RED, food_rect, 0, 7)  

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return [x, y]
    
    def generate_random_position(self, occupied_positions):
        
        position = self.generate_random_cell()
        while position in occupied_positions:
            position = self.generate_random_cell()
        
        return position

class Snake:
    def __init__(self):
        self.body = [[6, 9], [5, 9], [4, 9]]
        self.head = self.body[0]
        self.direction = [1, 0]
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (offset+ segment[0] * cell_size, offset + segment[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_BLUE, segment_rect, 0, 7)

    def update(self):
        self.head = add_2Dlists(self.body[0], self.direction)
        self.body.insert(0, self.head)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = [[6, 9], [5, 9], [4, 9]]
        self.direction = [1, 0]

def add_2Dlists(list1, list2):
    return [list1[0] + list2[0], list1[1] + list2[1]]

class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = 'STOPPED'
        self.score = 0
        self.highscore = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()
    
    def update(self):
        if self.state == 'RUNNING':
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_self()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_position(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            if self.highscore < self.score:
                self.highscore = self.score   

    def check_collision_with_edges(self):
        if self.snake.head[0] < 0 or self.snake.head[0] >= number_of_cells or self.snake.head[1] < 0 or self.snake.head[1] >= number_of_cells:
            self.game_over()

    def check_collision_with_self(self):
        headless_body = self.snake.body[1:]
        if self.snake.head in headless_body:
            self.game_over() 

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_position(self.snake.body)
        self.state = 'STOPPED'
        self.score = 0

screen = pygame.display.set_mode((cell_size*number_of_cells + 2*offset, cell_size*number_of_cells + 2*offset))

pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

snake_game = SnakeGame()

while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if snake_game.state == 'STOPPED':
                    snake_game.state = 'RUNNING'

                if event.key == pygame.K_UP and snake_game.snake.direction != [0, 1]:
                    snake_game.snake.direction = [0, -1]
                if event.key == pygame.K_DOWN and snake_game.snake.direction != [0, -1]:
                    snake_game.snake.direction = [0, 1]
                if event.key == pygame.K_LEFT and snake_game.snake.direction != [1, 0]:
                    snake_game.snake.direction = [-1, 0]
                if event.key == pygame.K_RIGHT and snake_game.snake.direction != [-1, 0]:
                    snake_game.snake.direction = [1, 0]
        
        snake_game.update()

        screen.fill(BLUE)
        pygame.draw.rect(screen, DARK_BLUE, (offset-5, offset-5, cell_size*number_of_cells + 10, cell_size*number_of_cells + 10), 5)
        snake_game.draw()
        
        title_surface = title_font.render("Snake Game", True, DARK_BLUE)
        score_surface = score_font.render(f"Score: {snake_game.score}", True, DARK_BLUE)
        highscore_surface = score_font.render(f"Highscore: {snake_game.highscore}", True, DARK_BLUE)
        
        screen.blit(title_surface, (offset, 10))
        screen.blit(score_surface, (offset, offset + cell_size*number_of_cells + 10))
        screen.blit(highscore_surface, (offset + int((cell_size*number_of_cells)/2), offset + cell_size*number_of_cells + 10))

        pygame.display.update()
        clock.tick(10)

    