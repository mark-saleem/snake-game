from unicodedata import name

import pygame, sys, json
from pathlib import Path


LEVELS_DIRECTORY = Path(__file__).parent / 'levels'

class LevelGenerator:
    def __init__(self, main):
        self.settings = main.settings
        self.screen = main.screen

        self.current_tool = 'ROCK'
        self.clear_level()

        self.drawing = False

    def set_tool(self, tool):
        self.current_tool = tool
    
    def _erase(self, cell):
        if cell is None:
            return
        if cell in self.rocks:
            self.rocks.remove(cell)
        if cell == self.snake_start:
            self.snake_start = None
        if cell == self.exit_pos:
            self.exit_pos = None

    def _place(self, cell):
        if cell is None:
            return
        if self.current_tool == 'ROCK':
            if cell not in self.rocks:
                self.rocks.append(cell)
        elif self.current_tool == 'SNAKE':
            self.snake_start = cell
        elif self.current_tool == 'EXIT':
            self.exit_pos = cell
        elif self.current_tool == 'ERASE':
            self._erase(cell)

    def clear_level(self):
        self.rocks = []
        self.snake_start = None
        self.exit_pos = None

    def pixel_to_cell(self, position):
        px, py = position
        column = (px - self.settings.offset) // self.settings.cell_size
        row = (py - self.settings.offset) // self.settings.cell_size
        if 0 <= column < self.settings.number_of_cells and 0 <= row < self.settings.number_of_cells:
            return [column, row]
        return None

    def save_level(self, name):
        if not self.snake_start:
            return
        if not self.exit_pos:
            return
        
        path = LEVELS_DIRECTORY / f'level_{name}.json'
        if path.exists():
            return

        data = {
            'name':        name,
            'grid_cells':  self.settings.number_of_cells,
            'snake_start': self.snake_start,
            'exit':        self.exit_pos,
            'rocks':       self.rocks,
        }

        path.write_text(json.dumps(data, indent=2))

        self.clear_level()

    def get_number_of_levels(self):
        if not LEVELS_DIRECTORY.exists():
            return 0
        return len(list(LEVELS_DIRECTORY.glob('*.json')))
    
    def draw_grid(self):
        for row in range(self.settings.number_of_cells):
            for column in range(self.settings.number_of_cells):
                
                x = column * self.settings.cell_size + self.settings.offset
                y = row * self.settings.cell_size + self.settings.offset

                rect = pygame.Rect(x, y, self.settings.cell_size, self.settings.cell_size)

                pygame.draw.rect(self.screen, self.settings.border_color, rect, 1)

                for position in self.rocks:
                    rock_rect = pygame.Rect(self.settings.offset + position[0] * self.settings.cell_size, self.settings.offset + position[1] * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
                    pygame.draw.rect(self.screen, self.settings.rock_color, rock_rect, 0, self.settings.cell_size * 3 // 8)

                if self.snake_start:
                    snake_rect = pygame.Rect(self.settings.offset + self.snake_start[0] * self.settings.cell_size, self.settings.offset + self.snake_start[1] * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
                    pygame.draw.rect(self.screen, self.settings.snake_color, snake_rect, 0, self.settings.cell_size * 3 // 8)

                if self.exit_pos:
                    exit_rect = pygame.Rect(self.settings.offset + self.exit_pos[0] * self.settings.cell_size, self.settings.offset + self.exit_pos[1] * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
                    pygame.draw.rect(self.screen, self.settings.exit_color, exit_rect, 0, self.settings.cell_size * 3 // 8)

    def load_level(self, number):
        files = sorted(LEVELS_DIRECTORY.glob('level_*.json'))

        with open(files[number], 'r') as file:
            data = json.load(file)

        self.clear_level()
        self.snake_start = data.get('snake_start')
        self.exit_pos = data.get('exit')
        self.rocks = data.get('rocks')