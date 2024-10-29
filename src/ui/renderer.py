import pygame as pg
from src.ui.selector import Selector


class Renderer:
    def __init__(self, width, height, surfaces):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption("2D RL Environment Builder")
        self.surfaces = surfaces

    def update(self):
        self.screen.fill((200, 200, 200))
        for surface in self.surfaces:
            obj, pos = surface["surface"], surface["position"]
            obj.draw()
            self.screen.blit(obj.surface, pos)
        pg.display.flip()

    def close(self):
        pg.quit()
