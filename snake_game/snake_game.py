import pygame, sys

from snake_game.settings import Settings
from snake_game.game.food import Food
from snake_game.game.snake import Snake
from snake_game.game.rock import Rock
from snake_game.user_interface.button import Button
from snake_game.user_interface.text_input import TextInput
from snake_game.user_database.user import User
from snake_game.game.exit import Exit
from snake_game.level_generator.level_generator import LevelGenerator

class SnakeGame:

    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.user = User()

        pygame.display.set_caption("Snake Game")

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        self.level_generator = LevelGenerator(self)

        self.play_button = Button(self, "Play", (300, 300))
        self.levels_button = Button(self, "Levels", (300, 350))
        self.menu_button = Button(self, "Menu", (300, 400))


        self.return_button = Button(self, "Return", (300, 400))

        self.color1_button = Button(self, "Orange", (150, 300))
        self.color2_button = Button(self, "Blue", (300, 300))
        self.color3_button = Button(self, "Purple", (450, 300))

        self.easy_button = Button(self, "Easy", (150, 250))
        self.normal_button = Button(self, "Normal", (300, 250))
        self.hard_button = Button(self, "Hard", (450, 250))

        self.small_button = Button(self, "Small", (150, 200))
        self.medium_button = Button(self, "Medium", (300, 200))
        self.large_button = Button(self, "Large", (450, 200))

        self.controls_button = Button(self, "Controls", (300, 350))

        self.login_username_input = TextInput(self, position=(300, 100), label='Username:',allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') #########################
        self.login_password_input = TextInput(self, position=(300, 150), label='Password:', hidden=True, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+/?.>,<[]') #########################
        self.login_button = Button(self, "Login", position=(300, 200))

        self.signup_username_input = TextInput(self, position=(300, 300), label='Username:',allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890') #########################
        self.signup_password_input = TextInput(self, position=(300, 350), label='Password:', hidden=True, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+/?.>,<[]') #########################
        self.signup_button = Button(self, "Sign up", position=(300, 400))
        
        self.level_buttons = [
            Button(self, f"{level+1}", (125 + level * 40, 300), size =(30, 30)) for level in range(self.level_generator.get_number_of_levels())
        ]

        self.level_generator_button = Button(self, "Generate Level", position=(300, 350), size=(150, 30))

        self.level_name_input = TextInput(self, position=(250, 20), size= (150, 30), label='Level Name:', allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_') #########################

        self.return_levels_button = Button(self, "Return", position=(620, 500))
        self.save_level_button = Button(self, "Save", position=(620, 450))
        self.clear_level_button = Button(self, "Clear", position=(620, 400))

        self.place_rock_button = Button(self, "Rock", position=(620, 100))
        self.place_snake_button = Button(self, "Snake", position=(620, 150))
        self.place_exit_button = Button(self, "Exit", position=(620, 200))
        self.erase_button = Button(self, "Erase", position=(620, 250))

        self.place_button_options = [
            (self.place_rock_button, "ROCK"),
            (self.place_snake_button, "SNAKE"),
            (self.place_exit_button, "EXIT"),
            (self.erase_button, "ERASE"),
        ]


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

            (self.controls_button, lambda: self.settings.set_controls()),
        ]

        self.stopped_button_actions = [
            (self.play_button,    lambda: self.start_round()),
            (self.menu_button,    lambda: self.set_state('MENU')),
            (self.levels_button,  lambda: self.set_state('LEVELS')),
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
        
        self.levels_button_actions = [
            (self.return_button,    lambda: self.set_state('STOPPED')),
            (self.level_generator_button, lambda: self.set_state('LEVEL_GENERATOR')),
        ] + [
            (self.level_buttons[level], lambda level=level: self.start_level(level)) for level in range(self.level_generator.get_number_of_levels())
        ]

        self.level_generator_actions = [
            (self.return_levels_button, lambda: self.set_state_levels()),
            (self.save_level_button, lambda: self.level_generator.save_level(self.level_name_input.get_text())),
            (self.clear_level_button, lambda: self.level_generator.clear_level()),

            (self.place_rock_button, lambda: self.level_generator.set_tool('ROCK')),
            (self.place_snake_button, lambda: self.level_generator.set_tool('SNAKE')),
            (self.place_exit_button, lambda: self.level_generator.set_tool('EXIT')),
            (self.erase_button, lambda: self.level_generator.set_tool('ERASE')),
        ]

        self.level_generator_input_fields = [
            self.level_name_input
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
                if self.state == 'LEVELS':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        self._check_buttons(self.levels_button_actions, mouse_position)

            if self.clicked_button == False:
                if self.state == 'LEVEL_GENERATOR':

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        self._check_buttons(self.level_generator_actions, mouse_position)
                        if self.level_generator.pixel_to_cell(mouse_position):
                            self.level_generator.drawing = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        self.level_generator.drawing = False
                    
                    if event.type == pygame.KEYDOWN:
                        if not any(field.active for field in self.level_generator_input_fields):
                            if event.key == pygame.K_r:
                                self.level_generator.set_tool('ROCK')
                            if event.key == pygame.K_s:
                                self.level_generator.set_tool('SNAKE')
                            if event.key == pygame.K_e:
                                self.level_generator.set_tool('EXIT')
                            if event.key == pygame.K_d:
                                self.level_generator.set_tool('ERASE')
                    
                    if self.level_generator.drawing:
                        mouse_position = pygame.mouse.get_pos()
                        cell = self.level_generator.pixel_to_cell(mouse_position)
                        self.level_generator._place(cell)
                    
                    for input_field in self.level_generator_input_fields:
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

                    if event.key == pygame.K_t:
                        self.snake.turn_around()

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

        elif self.state == 'MENU':

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
            for food in self.foods:
                food.draw()
            for rock in self.rocks:
                rock.draw()
            if self.exit:
                self.exit.draw()

        elif self.state == 'STOPPED':
            self.title_surface = self.title_font.render("Snake Game", True, self.title_color)
            self.score_surface = self.score_font.render(f"Score: {self.score}", True, self.score_color)
            self.highscore_surface = self.highscore_font.render(f"Highscore: {self.highscore}", True, self.highscore_color)

            self.screen.blit(self.title_surface, (self.settings.offset, 10))
            self.screen.blit(self.score_surface, (self.settings.offset, self.settings.offset + self.settings.cell_size*self.settings.number_of_cells + 10))
            self.screen.blit(self.highscore_surface, (self.settings.offset + int((self.settings.cell_size*self.settings.number_of_cells)/2), self.settings.offset + self.settings.cell_size*self.settings.number_of_cells + 10))
            
            self.play_button.draw()
            self.menu_button.draw()
            self.levels_button.draw()

        elif self.state == "LEVELS":
            self.return_button.draw()

            for level_button in self.level_buttons:
                level_button.draw()

            self.level_generator_button.draw()

        elif self.state == "LEVEL_GENERATOR":
            self.return_levels_button.draw()
            self.save_level_button.draw()
            self.clear_level_button.draw()

            self.place_rock_button.draw()
            self.place_snake_button.draw()
            self.place_exit_button.draw()
            self.erase_button.draw()

            self.level_name_input.draw()

            self.level_generator.draw_grid()

            
            
        pygame.display.update()

    def update(self):
        if self.state == 'RUNNING':
            self.snake.update()
            
            if self.foods:
                self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_self()
            self.check_collision_with_rock()
        
            if self.exit:
                self.check_collision_with_exit()

        if self.state == 'LEVEL_GENERATOR':
            self._check_on_button(self.place_button_options, self.level_generator.current_tool)

    def check_collision_with_food(self):
        for food in self.foods:
            if self.snake.body[0] == food.position:
                self.get_occupied_positions()
                food.relocate(self.occupied_positions)
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

    def check_collision_with_rock(self):
        for rock in self.rocks:
            if self.snake.head == rock.position:
                self.game_over()
    
    def check_collision_with_exit(self):
        if self.snake.head == self.exit.position:
            self.game_over()

    def game_over(self):
        self.snake.reset()

        for food in self.foods:
            self.get_occupied_positions()
            food.position = food.relocate(self.occupied_positions)
        self.state = 'STOPPED'
        self.score = 0

    def set_state(self, state):
        self.state = state

    def _check_buttons(self, button_actions, mouse_position):
        for button, action in button_actions:
            if button.rect.collidepoint(mouse_position):
                output = action()
                if button.on_off_switch:
                    button.toggle_on_off_color()
                self.clicked_button = True
                return output
    
    def _check_on_button(self, button_states, checker):
        for button, state in button_states:
            if checker == state:
                button._set_on_color()
            else:
                button._set_off_color()

    def start_round(self):
        self.set_state('RUNNING')
        
        self.snake = Snake(self)

        self.foods = []
        self.rocks = []
        for food in range(10):
            self.get_occupied_positions()
            self.foods.append(Food(self))
        self.exit = None

    def get_occupied_positions(self):
        self.occupied_positions = (
            self.snake.body +
            [rock.position for rock in self.rocks] +
            [food.position for food in self.foods]
        )

    def start_level(self, level):
        self.set_state('RUNNING')
        self.level_generator.load_level(level)
        self.snake = Snake(self, start_position=self.level_generator.snake_start)
        self.foods = []
        self.rocks = [Rock(self, position=rock_position) for rock_position in self.level_generator.rocks]
        self.exit = Exit(self, position=self.level_generator.exit_pos)

    def set_state_levels(self):
        self.set_state('LEVELS')
        self.set_level_buttons()

    def set_level_buttons(self):
        self.level_buttons = [
            Button(self, f"{level+1}", (125 + level * 40, 300), size =(30, 30)) for level in range(self.level_generator.get_number_of_levels())
        ]
        self.levels_button_actions = [
            (self.return_button,    lambda: self.set_state('STOPPED')),
            (self.level_generator_button, lambda: self.set_state('LEVEL_GENERATOR')),
        ] + [
            (self.level_buttons[level], lambda level=level: self.start_level(level)) for level in range(self.level_generator.get_number_of_levels())
        ]