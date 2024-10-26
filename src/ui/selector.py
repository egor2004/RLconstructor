import pygame as pg

class Selector:
    def __init__(self, x = 50, y = 20, screen = None):
        self.x = x
        self.y = y
        self.x_end = x + 400
        self.y_end = y + 80
        self.screen = screen
        # Состояние поля:
        # 0 - пустое
        # 1 - стена
        # 2 - агент
        # 3 - награда
        # 4 - наказание
        self.items = [0, 1, 2, 3, 4]
        self.selected_item = 0

    def draw_selector(self):

        pg.draw.rect(self.screen, "black", (self.x, self.y, self.x_end - self.x, self.y_end - self.y), border_radius=10)
        pg.draw.rect(self.screen, "white", (self.x + 5, self.y + 5, self.x_end - self.x - 10, self.y_end - self.y - 10), border_radius=10)
        colours = ["white", "black", "gray", "yellow", "red"]
        for i in range(5):
            x = self.x + i * 82 + 10
            if i == self.selected_item:
                pg.draw.rect(self.screen, "black", (x, self.y + 10, 50, 50),
                             border_radius=10)
            else:
                pg.draw.rect(self.screen, (100, 100, 100), (x, self.y + 10, 50, 50),
                             border_radius=10)

            pg.draw.rect(self.screen, colours[i], (x+3, self.y + 10 + 3, 50-6, 50-6),
                         border_radius=10)


    def update_selector(self, mouse_x, mouse_y):
        for i in range(5):
            x1 = self.x + i * 82 + 10
            y1 = self.y + 10
            x2 = x1 + 50
            y2 = y1 + 50
            if (x1 <= mouse_x < x2 and
                y1 <= mouse_y < y2):
                self.selected_item = i

