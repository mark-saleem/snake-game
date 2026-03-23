import pygame, sys

from snake_game.settings import Settings
from snake_game.game.food import Food
from snake_game.game.snake import Snake
from snake_game.user_interface.button import Button
from snake_game.user_interface.text_input import TextInput
from snake_game.user_database.user import User

class SnakeGame:

    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.user = User()

        pygame.display.set_caption("Snake Game")

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        self.play_button = Button(self, "Play", [300, 300])
        self.menu_button = Button(self, "Menu", [300, 400])


        self.return_button = Button(self, "Return", [300, 400])

        self.color1_button = Button(self, "Orange", [150, 300])
        self.color2_button = Button(self, "Blue", [300, 300])
        self.color3_button = Button(self, "Purple", [450, 300])

        self.easy_button = Button(self, "Easy", [150, 250])
        self.normal_button = Button(self, "Normal", [300, 250])
        self.hard_button = Button(self, "Hard", [450, 250])

        self.small_button = Button(self, "Small", [150, 200])
        self.medium_button = Button(self, "Medium", [300, 200])
        self.large_button = Button(self, "Large", [450, 200])

        self.controls_button = Button(self, "Controls", [300, 350])

        self.login_username_input = TextInput(self, position=(300, 100), label='Username:',allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') #########################
        self.login_password_input = TextInput(self, position=(300, 150), label='Password:', hidden=True, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+/?.>,<[]') #########################
        self.login_button = Button(self, "Login", position=(300, 200))

        self.signup_username_input = TextInput(self, position=(300, 300), label='Username:',allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') #########################
        self.signup_password_input = TextInput(self, position=(300, 350), label='Password:', hidden=True, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+/?.>,<[]') #########################
        self.signup_button = Button(self, "Sign up", position=(300, 400))
        

        self.menu_button_actions = [
            (self.return_button,    lambda: self.set_state('STOPPED')),

            (self.easy_button,    lambda: self.settings.set_difficulty('EASY')),
            (self.normal_button,  lambda: self.settings.set_difficulty('NORMAL')),
            (self.hard_button,    lambda: self.settings.set_difficulty('HARD')),

            (self.color1_button,  lambda: self.settings.set_background_color(self.settings.color1_name)),
            (self.color2_button,  lambda: self.settings.set_background_color(self.settings.color2_name)),
            (self.color3_button,  lambda: self.settings.set_background_color(self.settings.color3_name)),

            (self.small_button,    lambda: self.settings.set_game_size('SMALL')),
            (self.medium_button,    lambda: self.settings.set_game_size('MEDIUM')),
            (self.large_button,    lambda: self.settings.set_game_size('LARGE')),

            (self.controls_button, lambda: self.settings.set_controls())
        ]

        self.stopped_button_actions = [
            (self.play_button,    lambda: self.start_round()),
            (self.menu_button,    lambda: self.set_state('MENU'))
        ]

        self.loggingin_button_actions = [
            (self.login_button,    lambda: self.user.login(self.login_username_input.get_text(), self.login_password_input.get_text())),
            (self.signup_button,    lambda: self.user.signup(self.signup_username_input.get_text(), self.signup_password_input.get_text())),
        ]

        self.loggingin_input_fields = [
            self.login_username_input, 
            self.login_password_input, 
            self.signup_username_input, 
            self.signup_password_input
        ]

        self.state = 'LOGGINGIN'
        self.score = 0
        self.highscore = 0

        self.id = 0

        self.clicked_button = False
        self.moved = False

        self.title_color = self.settings.border_color
        self.score_color = self.settings.border_color
        self.highscore_color = self.settings.border_color

        self.title_font = self.settings.h1
        self.score_font = self.settings.h2
        self.highscore_font = self.settings.h2
        self.game_settings_font = self.settings.h3

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
                self.user.update_highscore(self.id, self.highscore)
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.user.update_highscore(self.id, self.highscore)
                    pygame.quit()
                    sys.exit()

            if self.clicked_button == False:
                if self.state == 'LOGGINGIN':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        self.userinfo = self._check_buttons(self.loggingin_button_actions, mouse_position)
                        if self.userinfo:
                            self.id = self.userinfo[0]
                            self.highscore = self.userinfo[3]
                            self.state = 'STOPPED'
                            

                    for input_field in self.loggingin_input_fields:
                        input_field.handle_event(event)

            if self.clicked_button == False:
                if self.state == 'STOPPED':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        self._check_buttons(self.stopped_button_actions, mouse_position)

            if self.clicked_button == False:
                if self.state == 'MENU':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        self._check_buttons(self.menu_button_actions, mouse_position)

            if event.type == pygame.MOUSEBUTTONUP and self.clicked_button == True:
                self.clicked_button = False
            
            if self.state == 'RUNNING':
                if event.type == pygame.KEYDOWN:
                    if event.key == self.settings.binds[0] or event.key == self.settings.binds[1] or event.key == self.settings.binds[2] or event.key == self.settings.binds[3]:
                        if self.moved == False:
                            if event.key == self.settings.binds[0] and self.snake.direction != [0, 1]:
                                self.snake.direction = [0, -1]
                            if event.key == self.settings.binds[2] and self.snake.direction != [0, -1]:
                                self.snake.direction = [0, 1]
                            if event.key == self.settings.binds[1] and self.snake.direction != [1, 0]:
                                self.snake.direction = [-1, 0]
                            if event.key == self.settings.binds[3] and self.snake.direction != [-1, 0]:
                                self.snake.direction = [1, 0]
                            
                            self.moved = True

    def draw(self):
        self.screen.fill(self.settings.background_color)
        pygame.draw.rect(self.screen, self.settings.border_color, (self.settings.offset-5, self.settings.offset-5, self.settings.cell_size*self.settings.number_of_cells + 10, self.settings.cell_size*self.settings.number_of_cells + 10), 5)
        
        if self.state == 'LOGGINGIN':

            self.login_username_input.draw() 
            self.login_password_input.draw() 
            self.login_button.draw()

            self.signup_username_input.draw() 
            self.signup_password_input.draw() 
            self.signup_button.draw()

        if self.state == 'MENU':

            self.difficulty_surface = self.game_settings_font.render(f"Difficulty: {self.settings.difficulty}" , True, self.title_color)
            self.size_surface = self.game_settings_font.render(f"Game Size: {self.settings.size}", True, self.title_color)
            self.color_surface = self.game_settings_font.render(f"Background Color: {self.settings.background_color_name}", True, self.title_color)
            self.controls_surface = self.game_settings_font.render(f"Controls: {self.settings.controls}", True, self.title_color)

            self.screen.blit(self.difficulty_surface, (self.settings.offset + 10, self.settings.offset + 10))
            self.screen.blit(self.size_surface, (self.settings.offset + 10, self.settings.offset + 10 + (self.game_settings_font.get_height())*1.2))
            self.screen.blit(self.color_surface, (self.settings.offset + 10, self.settings.offset + 10 + (self.game_settings_font.get_height())*2.4))
            self.screen.blit(self.controls_surface, (self.settings.offset + 10, self.settings.offset + 10 + (self.game_settings_font.get_height())*3.6))
            
            self.return_button.draw()
            
            self.color1_button.draw()
            self.color2_button.draw()
            self.color3_button.draw()

            self.easy_button.draw()
            self.normal_button.draw()
            self.hard_button.draw()

            self.small_button.draw()
            self.medium_button.draw()
            self.large_button.draw()

            self.controls_button.draw()
        
        elif self.state == 'RUNNING':
            self.title_surface = self.title_font.render("Snake Game", True, self.title_color)
            self.score_surface = self.score_font.render(f"Score: {self.score}", True, self.score_color)
            self.highscore_surface = self.highscore_font.render(f"Highscore: {self.highscore}", True, self.highscore_color)

            self.screen.blit(self.title_surface, (self.settings.offset, 10))
            self.screen.blit(self.score_surface, (self.settings.offset, self.settings.offset + self.settings.cell_size*self.settings.number_of_cells + 10))
            self.screen.blit(self.highscore_surface, (self.settings.offset + int((self.settings.cell_size*self.settings.number_of_cells)/2), self.settings.offset + self.settings.cell_size*self.settings.number_of_cells + 10))

            self.snake.draw()
            self.food.draw()

        elif self.state == 'STOPPED':
            self.title_surface = self.title_font.render("Snake Game", True, self.title_color)
            self.score_surface = self.score_font.render(f"Score: {self.score}", True, self.score_color)
            self.highscore_surface = self.highscore_font.render(f"Highscore: {self.highscore}", True, self.highscore_color)

            self.screen.blit(self.title_surface, (self.settings.offset, 10))
            self.screen.blit(self.score_surface, (self.settings.offset, self.settings.offset + self.settings.cell_size*self.settings.number_of_cells + 10))
            self.screen.blit(self.highscore_surface, (self.settings.offset + int((self.settings.cell_size*self.settings.number_of_cells)/2), self.settings.offset + self.settings.cell_size*self.settings.number_of_cells + 10))
            
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

    def set_state(self, state):
        self.state = state

    def _check_buttons(self, button_actions, mouse_position):
        for button, action in button_actions:
            if button.rect.collidepoint(mouse_position):
                output = action()
                self.clicked_button = True
                return output

                
    def start_round(self):
        self.set_state('RUNNING')
        
        self.snake = Snake(self)
        self.occupied_positions = self.snake.body

        self.food = Food(self)

        
