import pygame as pg
from src.ui.selector import Selector


class Renderer:
    def __init__(self, screen_width, screen_height, field):
        pg.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption("2D RL Environment Builder")

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.field = field
        self.selector = Selector(screen=self.screen)
        self.field.init_screen(self.screen)

    def render(self):
        self.screen.fill((200, 200, 200))
        self.selector.draw_selector()
        self.field.draw_field()
        pg.display.flip()

    def update(self):
        self.render()

    def close(self):
        pg.quit()
