import pygame as pg

class Button:
    def __init__(self, x, y, width, height, text, font, color, text_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)

    def render(self):
        # Отрисовка кнопки
        self.surface.fill((0, 0, 0, 0))  # Очистка поверхности
        button_rect = pg.Rect(0, 0, self.width, self.height)
        pg.draw.rect(self.surface, self.color, button_rect, border_radius=10)

        # Отрисовка текста
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x + self.width and
                self.y <= mouse_y <= self.y + self.height)