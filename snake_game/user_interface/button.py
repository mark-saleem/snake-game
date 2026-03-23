import pygame

class Button:
    def __init__(self, main, message, position):
        self.settings = main.settings
        self.screen = main.screen

        self.message = message
        self.position = position

        self.width, self.height = 110, 30

        self.base_color = self.settings.button_color
        self.hover_color = (min(self.base_color[0] + 30, 255), 
                            min(self.base_color[1] + 30, 255),
                            min(self.base_color[2] + 30, 255))
        self.click_color = (max(self.base_color[0] - 30, 0),
                            max(self.base_color[1] - 30, 0),
                            max(self.base_color[2] - 30, 0))

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

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered():
                return True
        return False
