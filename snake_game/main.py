import pygame, sys, random

from settings import Settings
from food import Food
from snake import Snake
from button import Button

class Main:

    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()

        self.settings = Settings()

        pygame.display.set_caption("Snake Game")

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.snake = Snake(self)
        self.occupied_positions = self.snake.body
    
        self.food = Food(self)
        
        self.play_button = Button(self, "Play", [300, 300])
        self.menu_button = Button(self, "Menu", [300, 400])
        self.return_button = Button(self, "Return", [300, 400])

        self.color1_botton = Button(self, "Orange", [150, 300])
        self.color2_botton = Button(self, "Blue", [300, 300])
        self.color3_botton = Button(self, "Green", [450, 300])

        self.easy_button = Button(self, "Easy", [150, 250])
        self.normal_button = Button(self, "Normal", [300, 250])
        self.hard_button = Button(self, "Hard", [450, 250])

        self.small_button = Button(self, "Small", [150, 200])
        self.medium_button = Button(self, "Medium", [300, 200])
        self.large_button = Button(self, "Large", [450, 200])

        self.background_color = self.settings.background_color

        self.state = 'STOPPED'
        self.score = 0
        self.highscore = 0

        self.clicked_button = False
        self.moved = False

        self.title_color = self.settings.border_color
        self.score_color = self.settings.border_color
        self.highscore_color = self.settings.border_color

        self.title_font = self.settings.h1
        self.score_font = self.settings.h2
        self.highscore_font = self.settings.h2

    def run_game(self):
        while True:
             
            self._check_events()

            self.update()

            self.draw()
            
            self.moved = False
            
            self.clock.tick(self.settings.fps)
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            
            if self.clicked_button == False:
                if self.state == 'STOPPED':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        self._check_play_button(mouse_position)
                        self._check_menu_button(mouse_position)

            if self.clicked_button == False:
                if self.state == 'MENU':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        self._check_return_button(mouse_position)
                        
                        self._check_color1_button(mouse_position)
                        self._check_color2_button(mouse_position)
                        self._check_color3_button(mouse_position)

                        self._check_easy_button(mouse_position)
                        self._check_normal_button(mouse_position)
                        self._check_hard_button(mouse_position)

                        self._check_small_button(mouse_position)
                        self._check_medium_button(mouse_position)
                        self._check_large_button(mouse_position)

            if event.type == pygame.MOUSEBUTTONUP and self.clicked_button == True:
                self.clicked_button = False
            
            if self.state == 'RUNNING':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_LEFT or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        if self.moved == False:
                            if event.key == pygame.K_UP and self.snake.direction != [0, 1]:
                                self.snake.direction = [0, -1]
                            if event.key == pygame.K_DOWN and self.snake.direction != [0, -1]:
                                self.snake.direction = [0, 1]
                            if event.key == pygame.K_LEFT and self.snake.direction != [1, 0]:
                                self.snake.direction = [-1, 0]
                            if event.key == pygame.K_RIGHT and self.snake.direction != [-1, 0]:
                                self.snake.direction = [1, 0]
                            
                            self.moved = True

    def draw(self):
        self.screen.fill(self.background_color)
        pygame.draw.rect(self.screen, self.settings.border_color, (self.settings.offset-5, self.settings.offset-5, self.settings.cell_size*self.settings.number_of_cells + 10, self.settings.cell_size*self.settings.number_of_cells + 10), 5)
        
        if self.state == 'MENU':
            self.return_button.draw()
            
            self.color1_botton.draw()
            self.color2_botton.draw()
            self.color3_botton.draw()

            self.easy_button.draw()
            self.normal_button.draw()
            self.hard_button.draw()

            self.small_button.draw()
            self.medium_button.draw()
            self.large_button.draw()
        
        else:
            self.title_surface = self.title_font.render("Snake Game", True, self.title_color)
            self.score_surface = self.score_font.render(f"Score: {self.score}", True, self.score_color)
            self.highscore_surface = self.highscore_font.render(f"Highscore: {self.highscore}", True, self.highscore_color)

            self.screen.blit(self.title_surface, (self.settings.offset, 10))
            self.screen.blit(self.score_surface, (self.settings.offset, self.settings.offset + self.settings.cell_size*self.settings.number_of_cells + 10))
            self.screen.blit(self.highscore_surface, (self.settings.offset + int((self.settings.cell_size*self.settings.number_of_cells)/2), self.settings.offset + self.settings.cell_size*self.settings.number_of_cells + 10))

            self.snake.draw()
            self.food.draw()

            if self.state == 'STOPPED':
                self.play_button.draw()
                self.menu_button.draw()

        pygame.display.update()

    def update(self):
        if self.state == 'RUNNING':
            self.snake.update()
            
            self.occupied_positions = self.snake.body
            
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
        if self.snake.head[0] < 0 or self.snake.head[0] >= self.settings.number_of_cells or self.snake.head[1] < 0 or self.snake.head[1] >= self.settings.number_of_cells:
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

    def _check_play_button(self, mouse_position):
        button_clicked = self.play_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self.state = 'RUNNING'
            self.clicked_button = True

    def _check_menu_button(self, mouse_position):
        button_clicked = self.menu_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self.state = 'MENU'
            self.clicked_button = True

    def _check_return_button(self, mouse_position):
        button_clicked = self.return_button.rect.collidepoint(mouse_position)
        if button_clicked:
            
            self.snake = Snake(self)
            self.food = Food(self)

            self.state = 'STOPPED'
            self.clicked_button = True
    
    def _check_color1_button(self, mouse_position):
        button_clicked = self.color1_botton.rect.collidepoint(mouse_position)
        if button_clicked:
            self.background_color = self.settings.color1
            self.clicked_button = True
        
    def _check_color2_button(self, mouse_position):
        button_clicked = self.color2_botton.rect.collidepoint(mouse_position)
        if button_clicked:
            self.background_color = self.settings.color2
            self.clicked_button = True

    def _check_color3_button(self, mouse_position):
        button_clicked = self.color3_botton.rect.collidepoint(mouse_position)
        if button_clicked:
            self.background_color = self.settings.color3
            self.clicked_button = True

    def _check_easy_button(self, mouse_position):
        button_clicked = self.easy_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self.settings.set_difficulty('EASY')
            self.clicked_button = True
    
    def _check_normal_button(self, mouse_position):
        button_clicked = self.normal_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self.settings.set_difficulty('NORMAL')
            self.clicked_button = True

    def _check_hard_button(self, mouse_position):
        button_clicked = self.hard_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self.settings.set_difficulty('HARD')
            self.clicked_button = True

    def _check_small_button(self, mouse_position):
        button_clicked = self.small_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self.settings.set_game_size('SMALL')
            self.clicked_button = True

    def _check_medium_button(self, mouse_position):
        button_clicked = self.medium_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self.settings.set_game_size('MEDIUM')
            self.clicked_button = True
    
    def _check_large_button(self, mouse_position):
        button_clicked = self.large_button.rect.collidepoint(mouse_position)
        if button_clicked:
            self.settings.set_game_size('LARGE')
            self.clicked_button = True

if __name__ == '__main__':
    main = Main()
    main.run_game()