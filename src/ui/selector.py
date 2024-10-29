import pygame as pg

class Selector:
    COLORS = ["white", "black", "gray", "yellow", "red"]

    def __init__(self):
        self.width = 400
        self.height = 80
        self.surface = pg.Surface((self.width, self.height))
        self.selected_item = 0

    def draw(self):
        pg.draw.rect(self.surface,"black", (0, 0, self.width, self. width), border_radius=10)
        pg.draw.rect(self.surface, "white", (5, 5, self.width - 10, self.height - 10), border_radius=10)
        for i, color in enumerate(self.COLORS):
            x = i * 82 + 10
            rect_color = "black" if i == self.selected_item else (100, 100, 100)
            pg.draw.rect(self.surface, rect_color, (x + 0, 10, 50, 50), border_radius=10)
            pg.draw.rect(self.surface, color, (x + 3, 13, 44, 44), border_radius=10)


    def update(self, mouse_x, mouse_y):
        for i in range(5):
            x1 = i * 82 + 10
            y1 = 10
            x2 = x1 + 50
            y2 = y1 + 50
            if (x1 <= mouse_x < x2 and
                y1 <= mouse_y < y2):
                self.selected_item = i

