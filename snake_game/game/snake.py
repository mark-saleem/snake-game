import pygame 

class Snake:
    def __init__(self, main, start_position = None, start_direction = None):
        self.settings = main.settings
        self.screen = main.screen

        self.color = self.settings.snake_color
        
        self.start_direction = start_direction if start_direction else [1, 0]
        
        if start_position:
            self.start_body = [start_position,
                         add_2Dlists(start_position, negative_2Dlist(self.start_direction)),
                         add_2Dlists(add_2Dlists(start_position, negative_2Dlist(self.start_direction)), negative_2Dlist(self.start_direction))
                         ]
        else:
            start_height = int(self.settings.number_of_cells/2)
            self.start_body = [[4, start_height],
                         add_2Dlists([4, start_height], negative_2Dlist(self.start_direction)),
                         add_2Dlists(add_2Dlists([4, start_height], negative_2Dlist(self.start_direction)), negative_2Dlist(self.start_direction))
                         ]
        
        self.body = self.start_body
        self.direction = self.start_direction

        self.head = self.body[0]
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (self.settings.offset+ segment[0] * self.settings.cell_size, self.settings.offset + segment[1] * self.settings.cell_size, self.settings.cell_size, self.settings.cell_size)
            pygame.draw.rect(self.screen, self.color, segment_rect, 0, self.settings.cell_size * 3 // 8)


    def update(self):
        self.head = add_2Dlists(self.body[0], self.direction)
        self.body.insert(0, self.head)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = self.start_body
        self.direction = self.start_direction

    def turn_around(self):
        self.direction = add_2Dlists(self.body[-1], negative_2Dlist(self.body[-2]))
        self.body = self.body[::-1]
        self.head = self.body[0]

def add_2Dlists(list1, list2):
    return [list1[0] + list2[0], list1[1] + list2[1]]

def negative_2Dlist(list1):
    return [-list1[0], -list1[1]]
