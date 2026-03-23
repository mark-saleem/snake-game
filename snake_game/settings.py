import pygame

#Game states RUNNING, STOPPED, MENU
# Game modes EASY, NORMAL, HARD
# Game sizes SMALL, MEDIUM, LARGE

class Settings:
    
    def __init__(self):

        self.number_of_cells = 25
        self.cell_size = 20
        self.offset = 50

        self.h1 = pygame.font.Font(None, 40)
        self.h2 = pygame.font.Font(None, 30)
        self.h3 = pygame.font.Font(None, 24)
        self.text = pygame.font.Font(None, 20)


        self.screen_width = self.cell_size*self.number_of_cells + 2*self.offset
        self.screen_height = self.cell_size*self.number_of_cells + 2*self.offset

        self.background_color = (120, 190, 255)
        self.background_color_name = 'BLUE'

        self.border_color = (20, 30, 90)
        self.food_color = (253, 21, 21)

        self.color1 = (250, 136, 60)
        self.color1_name = 'ORANGE'

        self.color2 = (120, 190, 255)
        self.color2_name = 'BLUE'

        self.color3 = (175, 143, 233) 
        self.color3_name = 'PURPLE'

        self.fps = 10
        self.difficulty = 'NORMAL'
        self.size = 'MEDIUM'

        self.button_color = (200, 200, 200)

        self.controls = 'WASD'
        self.binds = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]

    def set_difficulty(self, difficulty: str):
        self.difficulty = difficulty
        if self.difficulty == 'EASY':
            self.fps = 5
        elif self.difficulty == 'NORMAL':
            self.fps = 10
        elif self.difficulty == 'HARD':
            self.fps = 20

    def set_background_color(self, color_name: str):
        if color_name == self.color1_name:
            self.background_color = self.color1
            self.background_color_name = self.color1_name
        elif color_name == self.color2_name:
            self.background_color = self.color2
            self.background_color_name = self.color2_name
        elif color_name == self.color3_name:
            self.background_color = self.color3
            self.background_color_name = self.color3_name

    def set_game_size(self, size: str):
        self.size = size
        if self.size == 'SMALL':
            self.number_of_cells = 10
        elif self.size == 'MEDIUM':
            self.number_of_cells = 15
        elif self.size == 'LARGE':
            self.number_of_cells = 25
        
        self.cell_size = int(500/self.number_of_cells)
        self.offset = int((600 - (self.cell_size*self.number_of_cells)) / 2) 

        self.screen_width = self.cell_size*self.number_of_cells + 2*self.offset
        self.screen_height = self.cell_size*self.number_of_cells + 2*self.offset

    def set_controls(self):
        if self.controls == 'WASD':
            self.controls = 'ARROWS'
            self.binds = [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]
        elif self.controls == 'ARROWS':
            self.controls = 'WASD'
            self.binds = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
      