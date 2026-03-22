import pygame 

class Snake:
    def __init__(self, main):
        self.settings = main.settings
        self.screen = main.screen

        self.color = self.settings.border_color

        self.start_height = int(self.settings.number_of_cells/2)

        self.body = [[4, self.start_height], [3, self.start_height], [2, self.start_height]]
        self.head = self.body[0]
        self.direction = [1, 0]
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (self.settings.offset+ segment[0] * self.settings.cell_size, self.settings.offset + segment[1] * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
            pygame.draw.rect(self.screen, self.color, segment_rect, 0, 7)

    def update(self):
        self.head = add_2Dlists(self.body[0], self.direction)
        self.body.insert(0, self.head)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = [[4, self.start_height], [3, self.start_height], [2, self.start_height]]
        self.direction = [1, 0]

def add_2Dlists(list1, list2):
    return [list1[0] + list2[0], list1[1] + list2[1]]