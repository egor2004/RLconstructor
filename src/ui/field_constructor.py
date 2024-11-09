import pygame as pg
from os import path

class FieldConstructor():
    COLORS = {0: "white", 1: "black", 2: "gray", 3: "yellow", 4: "red", 5: "purple"}

    def __init__(self, cell_size = 70, field_size_x=8, field_size_y=8, margin=1):
        self.cell_size = cell_size
        self.field_size_x = field_size_x
        self.field_size_y = field_size_y
        self.field = [[0] * self.field_size_x for i in range(self.field_size_y)]
        self.margin = margin
        self.width = self.cell_size * self.field_size_x + self.margin * (self.field_size_x + 1)
        self.height = self.cell_size * self.field_size_y + self.margin * (self.field_size_y + 1)
        self.surface = pg.Surface((self.width, self.height))

        self.agent_pos = [0, 0]
        self.field[0][0] = 2
        self.agent_img = None
        self.reward_img = None
        self.background_img = None

    def reset(self):
        self.field = [[0] * self.field_size_x for i in range(self.field_size_y)]
        self.agent_pos = [0, 0]
        self.field[0][0] = 2

    def render(self):
        if self.agent_img is None:
            file_name = path.join(path.dirname(__file__), "img/elf_down.png")
            self.agent_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))

        if self.reward_img is None:
            file_name = path.join(path.dirname(__file__), "img/cookie.png")
            self.reward_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))

        if self.background_img is None:
            file_name = path.join(path.dirname(__file__), "img/taxi_background.png")
            self.background_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))

        color = "black"
        pg.draw.rect(self.surface, color, (0, 0, self.width, self.height), border_radius=5)

        for row in range(self.field_size_x):
            for col in range(self.field_size_y):
                color = self.COLORS.get(self.field[col][row], "white")

                x = row * self.cell_size + (row + 1) * self.margin
                y = col * self.cell_size + (col + 1) * self.margin


                self.surface.blit(self.background_img, (x, y))
                if self.field[col][row] == 0:
                    self.surface.blit(self.background_img, (x, y))
                elif self.field[col][row] == 1:
                    pg.draw.rect(self.surface, color, (x, y, self.cell_size, self.cell_size))
                elif self.field[col][row] == 2:
                    self.surface.blit(self.agent_img, (x, y))
                elif self.field[col][row] == 3:
                    self.surface.blit(self.reward_img, (x, y))
                elif self.field[col][row] == 4:
                    pg.draw.rect(self.surface, color, (x, y, self.cell_size, self.cell_size))
                elif self.field[col][row] == 5:
                    pg.draw.rect(self.surface, color, (x, y, self.cell_size, self.cell_size))


    def update(self, mouse_x, mouse_y, item=0):
        row = mouse_x  // (self.cell_size + self.margin)
        col = mouse_y // (self.cell_size + self.margin)
        if item == 2:
            self.field[self.agent_pos[1]][self.agent_pos[0]] = 0
            self.agent_pos = (row, col)
        self.field[col][row] = item