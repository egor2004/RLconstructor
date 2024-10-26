import pygame as pg

class Field:
    def __init__(self, x = 50, y = 50, rect_size = 40, field_size_x=10, field_size_y=10, margin=3):
        self.screen = None
        self.x = x
        self.y = y
        self.rect_size = rect_size
        self.field_size_x = field_size_x
        self.field_size_y = field_size_y
        self.field = [[0] * self.field_size_x for i in range(self.field_size_y)]
        self.margin = margin
        self.x_end = self.x + self.rect_size * self.field_size_x + self.margin * (self.field_size_x + 1)
        self.y_end = self.y + self.rect_size * self.field_size_y + self.margin * (self.field_size_y + 1)

    def init_screen(self, screen):
        self.screen = screen

    def draw_field(self):
        color = "black"
        pg.draw.rect(self.screen, color, (self.x, self.y, self.x_end - self.x, self.y_end - self.y), border_radius=5)

        for row in range(self.field_size_x):
            for col in range(self.field_size_y):
                x = self.x + row * self.rect_size + (row + 1) * self.margin
                y = self.y + col * self.rect_size + (col + 1) * self.margin
                if self.field[col][row] == 0:
                    color = "white"
                elif self.field[col][row] == 1:
                    color = "black"
                elif self.field[col][row] == 2:
                    color = "gray"
                elif self.field[col][row] == 3:
                    color = "yellow"
                elif self.field[col][row] == 4:
                    color = "red"
                pg.draw.rect(self.screen, color, (x, y, self.rect_size, self.rect_size))

    def update_field(self, mouse_x, mouse_y, item=1):
        if (self.x <= mouse_x < self.x_end - self.margin and
            self.y <= mouse_y < self.y_end - self.margin):
            row = (mouse_x - self.x) // (self.rect_size + self.margin)
            col = (mouse_y - self.y) // (self.rect_size + self.margin)
            self.field[col][row] = item