import pygame, random

class Food:
    def __init__(self, main):
        self.settings = main.settings
        self.screen = main.screen

        self.color = self.settings.food_color

        occupied_positions = main.occupied_positions
        self.position = self.generate_random_position(occupied_positions)

    def draw(self):
        food_rect = pygame.Rect(self.settings.offset +self.position[0] * self.settings.cell_size, self.settings.offset + self.position[1] * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
        pygame.draw.rect(self.screen, self.color, food_rect, 0, self.settings.cell_size * 3 // 8)  

    def generate_random_cell(self):
        x = random.randint(0, self.settings.number_of_cells - 1)
        y = random.randint(0, self.settings.number_of_cells - 1)
        return [x, y]
    
    def generate_random_position(self, occupied_positions):
        
        position = self.generate_random_cell()
        while position in occupied_positions:
            position = self.generate_random_cell()
        
        return position
