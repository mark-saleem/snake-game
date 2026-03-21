import pygame

class Button:

    def __init__(self, main, message, position: list[int, int]):
        self.settings = main.settings
        self.screen = main.screen

        self.message = message
        self.position = position

        self.width, self.height = 100, 25

        self.button_color = self.settings.button_color
        self.text_color = self.settings.border_color

        self.font = pygame.font.SysFont(None, 24)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.position) 
        self._prepare_message()

    def _prepare_message(self,):
        self.message_image = self.font.render(self.message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
