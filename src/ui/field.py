import pygame as pg

class Field:
    COLORS = {0: "white", 1: "black", 2: "gray", 3: "yellow", 4: "red"}

    def __init__(self, rect_size = 40, field_size_x=10, field_size_y=10, margin=3):
        self.rect_size = rect_size
        self.field_size_x = field_size_x
        self.field_size_y = field_size_y
        self.field = [[0] * self.field_size_x for i in range(self.field_size_y)]
        self.margin = margin
        self.width = self.rect_size * self.field_size_x + self.margin * (self.field_size_x + 1)
        self.height = self.rect_size * self.field_size_y + self.margin * (self.field_size_y + 1)
        self.surface = pg.Surface((self.width, self.height))

    def draw(self):
        color = "black"
        pg.draw.rect(self.surface, color, (0, 0, self.width, self.height), border_radius=5)

        for row in range(self.field_size_x):
            for col in range(self.field_size_y):
                color = self.COLORS.get(self.field[col][row], "white")
                x = row * self.rect_size + (row + 1) * self.margin
                y = col * self.rect_size + (col + 1) * self.margin
                pg.draw.rect(self.surface, color, (x, y, self.rect_size, self.rect_size))

    def update(self, mouse_x, mouse_y, item=0):
        row = mouse_x  // (self.rect_size + self.margin)
        col = mouse_y // (self.rect_size + self.margin)
        self.field[col][row] = item