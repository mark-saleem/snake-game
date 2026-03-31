import pygame

class Button:
    def __init__(self, main, message, position, size = (110, 30), on_off_switch=False):
        self.settings = main.settings
        self.screen = main.screen

        self.message = message
        self.position = position

        self.width, self.height = size

        self.on_off_switch = on_off_switch
        self.on = False

        self.base_color = self.settings.button_color
        self._set_button_colors()

        self.text_color = self.settings.border_color

        self.font = pygame.font.SysFont(None, 26)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.position

        self.clicked = False
        self._prepare_message()

    def _prepare_message(self):
        self.message_image = self.font.render(self.message, True, self.text_color)
        self.message_image_rect = self.message_image.get_rect(center=self.rect.center)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        color = self.get_button_color()

        pygame.draw.rect(
            self.screen,
            color,
            self.rect,
            border_radius=8
        )

        pygame.draw.rect(
            self.screen,
            self.text_color,
            self.rect,
            2,
            border_radius=8
        )

        self.screen.blit(self.message_image, self.message_image_rect)

    def get_button_color(self):
        if not self.is_hovered():
            return self.base_color
        if not pygame.mouse.get_pressed()[0]:
            return self.hover_color
        return self.click_color
    
    def toggle_on_off_color(self):
        if self.on:
            self.base_color = self.settings.button_color
        else:
            self.base_color = self.settings.button_on_color
        self.on = not self.on
        self._set_button_colors()

    def _set_on_color(self):
        self.base_color = self.settings.button_on_color
        self._set_button_colors()
    
    def _set_off_color(self):
        self.base_color = self.settings.button_color
        self._set_button_colors()

    def _set_button_colors(self):
        self.hover_color = (min(self.base_color[0] + 30, 255), 
                            min(self.base_color[1] + 30, 255),
                            min(self.base_color[2] + 30, 255))
        self.click_color = (max(self.base_color[0] - 30, 0),
                            max(self.base_color[1] - 30, 0),
                            max(self.base_color[2] - 30, 0))
        