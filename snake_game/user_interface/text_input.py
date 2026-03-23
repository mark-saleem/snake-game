import pygame

class TextInput:
    def __init__(self, main,
        position,
        label = "",
        width = 220,
        height = 40,
        max_length = 12,
        allowed_chars = None,
        label_gap = 10,
        hidden = False 
    ):
        
        self.screen = main.screen
        self.settings = main.settings

        self.font = pygame.font.SysFont(None, 26)

        # Label
        self.label = label
        self.label_surface = self.font.render(label, True, self.settings.border_color)
        self.label_gap = label_gap

        self.hidden = hidden

        # Input box rect (shifted right if label exists)
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = position
        if label:
            self.rect.x += self.label_surface.get_width() // 2 + label_gap

        self.text = ""
        self.max_length = max_length
        self.active = False
        self.allowed_chars = allowed_chars

        self.base_color = self.settings.button_color
        self.active_color = (
            min(self.base_color[0] + 40, 255),
            min(self.base_color[1] + 40, 255),
            min(self.base_color[2] + 40, 255)
        )
        self.border_color = self.settings.border_color

        display_text = self._get_display_text()
        self.text_surface = self.font.render(display_text, True, self.border_color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            else:
                char = event.unicode
                if (
                    len(self.text) < self.max_length
                    and char
                    and (self.allowed_chars is None or char in self.allowed_chars)
                ):
                    self.text += char
            
            display_text = self._get_display_text()
            self.text_surface = self.font.render(display_text, True, self.border_color)

        return None

    def get_text(self):
        if len(self.text) >= 1:
            return self.text
        return None

    def draw(self):
        # Label
        if self.label:
            label_x = self.rect.x - self.label_surface.get_width() - self.label_gap
            label_y = self.rect.centery - self.label_surface.get_height() // 2
            self.screen.blit(self.label_surface, (label_x, label_y))

        # Input box
        color = self.active_color if self.active else self.base_color
        pygame.draw.rect(self.screen, color, self.rect, border_radius=8)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2, border_radius=8)

        # Text
        self.screen.blit(
            self.text_surface,
            (
                self.rect.x + 10,
                self.rect.centery - self.text_surface.get_height() // 2
            )
        )

        # Cursor
        if self.active:
            cursor_x = self.rect.x + 10 + self.text_surface.get_width() + 2
            cursor_y = self.rect.y + 8
            cursor_h = self.rect.height - 16
            pygame.draw.line(
                self.screen,
                self.border_color,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_h),
                2
            )
            
    def _get_display_text(self):
        if self.hidden:
            return "*" * len(self.text)
        return self.text
