from ui.renderer import Renderer
from ui.field import Field
from ui.selector import Selector
import pygame as pg

field = Field(20, 40, 25)
selector = Selector()

surfaces = [
    {"surface": field, "position": (30, 120)},
    {"surface": selector, "position": (30, 20)}
]
renderer = Renderer(1024, 720, surfaces)

fps = 60
clock = pg.time.Clock()

def mouse_click():
    # Обработка нажатий на элементы игрового поля и селектора
    x, y = pg.mouse.get_pos()
    b1, b2, b3 = pg.mouse.get_pressed()

    if b1:
        loc_selector_x = x - surfaces[1]["position"][0]
        loc_selector_y = y - surfaces[1]["position"][1]
        if (0 <= loc_selector_x < selector.width and
            0 <= loc_selector_y < selector.height):
            selector.update(loc_selector_x, loc_selector_y)

        loc_field_x = x - surfaces[0]["position"][0]
        loc_field_y = y - surfaces[0]["position"][1]
        if (0 <= loc_field_x < field.width - field.margin and
            0 <= loc_field_y < field.height - field.margin):
            field.update(loc_field_x, loc_field_y, selector.selected_item)

def main_loop():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        mouse_click()
        renderer.update()
        clock.tick(fps)

    renderer.close()

if __name__ == "__main__":
    main_loop()