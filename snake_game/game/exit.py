import pygame

class Exit:
    def __init__(self, main, position):
        self.settings = main.settings
        self.screen = main.screen

        self.color = self.settings.exit_color
        self.position = position

    def draw(self):
        exit_rect = pygame.Rect(self.settings.offset +self.position[0] * self.settings.cell_size, self.settings.offset + self.position[1] * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
        pygame.draw.rect(self.screen, self.color, exit_rect, 0, self.settings.cell_size * 3 // 8) 
     