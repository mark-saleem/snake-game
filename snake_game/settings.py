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
        self.border_color = (20, 30, 90)
        self.food_color = (253, 21, 21)

        self.color1 = (250, 136, 60) # orange
        self.color2 = (120, 190, 255) # blue og color
        self.color3 = (175, 143, 233) # purple

        self.fps = 10
        self.difuculty = 'NORMAL'

        self.button_color = (180, 180, 180)


    def set_difficulty(self, difficulty: str):
        self.difuculty = difficulty
        if self.difuculty == 'EASY':
            self.fps = 7
        elif self.difuculty == 'NORMAL':
            self.fps = 10
        elif self.difuculty == 'HARD':
            self.fps = 20

    def set_game_size(self, size: str):
        if size == 'SMALL':
            self.number_of_cells = 10
        elif size == 'MEDIUM':
            self.number_of_cells = 15
        elif size == 'LARGE':
            self.number_of_cells = 25
        
        self.cell_size = int(500/self.number_of_cells)
        self.offset = int((600 - (self.cell_size*self.number_of_cells)) / 2) 

        self.screen_width = self.cell_size*self.number_of_cells + 2*self.offset
        self.screen_height = self.cell_size*self.number_of_cells + 2*self.offset
      