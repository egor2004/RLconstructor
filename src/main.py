from ui.renderer import Renderer
from ui.field import Field
import pygame as pg

field = Field(y=130, field_size_x=5, field_size_y=5, rect_size=100)
renderer = Renderer(1024, 720, field)


def scene_constructor():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pg.mouse.get_pos()
                renderer.selector.update_selector(x_mouse, y_mouse)
                field.update_field(x_mouse, y_mouse, renderer.selector.selected_item)

        renderer.update()

scene_constructor()
renderer.close()